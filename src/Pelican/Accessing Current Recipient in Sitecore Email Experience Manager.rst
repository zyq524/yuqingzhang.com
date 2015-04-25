Accessing Current Recipient in Sitecore Email Experience Manager
=======================================================================

:date: 2015-04-25
:tags: Sitecore, Sitecore 8, Email Experience Manager

I was working on a project that uses the latest Sitecore Email Experience Manager (EXM 3.0 rev150223), but I think this blog should also apply to the earlier releases of EXM 3.0. The project was about to be able to send an email whose content is based on each recipient's interested topics. 

This is a not unusual email personalization scenario. The idea is that on the sublayout that renders the customized content, it gets the recipient context so that it can query the recipient's profile and render the sublayout according to his topics.

In the old ECM 2, we can achieve this fairly easy by using the **ec_recipient** query string.

.. code-block:: c#

	var recipient = Sitecore.Security.Accounts.User.FromName(Request["ec_recipient"]);

I tried this in the EXM project, the query string just returned nothing! Then I realized that this was because the **ec_recipient** worked only with the Sitecore User(SQL Server Membership) and the new EXM's biggest change is that it only supports Contacts in the MongoDB, not Membership User. So we can't use **ec_recipient** to get the current recipient in EXM anymore.

After reading the Sitecore.EmailCampaign.config settings, I found another query string **ec_contact_id**. This looked very promising and it does return a GUID when the sublayout is rendering. However, this contact id is an encrypted contact Id and in order to use it to query the MongoDB we need to decrypt it first!

EXM's encryption uses the private key defined in the Sitecore.EmailCampaign.config settings and the IV is the message Id. So in order to decrypt the contact Id, we also need to find out the current message Id. There is a silver lining that EXM exposes a **sc_itemid** query string which is the Message Root item of the current email. By using this we can get the message Id.


Put all these together, I figured out the following code that helped me solving this issue.

.. code-block:: c#

    public static ID GetDecryptedContactId()
    {
      var encryptedContactIdValue = WebUtil.GetQueryString("ec_contact_id");

      if (string.IsNullOrEmpty(encryptedContactIdValue))
      {
        return ID.Null;
      }

      var messageRootItemId = WebUtil.GetQueryString("sc_itemid");
      var db = WebUtil.GetQueryString("ec_database");

      if (string.IsNullOrEmpty(messageRootItemId) || string.IsNullOrEmpty(db))
      {
        return ID.Null;
      }

      var messageRootItem = Database.GetDatabase(db).GetItem(ID.Parse(messageRootItemId));
      if (messageRootItem == null)
      {
        return ID.Null;
      }

      var messageIdValue = messageRootItem.ParentID.ToString();

      ShortID messageShortId = ShortID.Parse(messageIdValue);
      ShortID encryptedContactShortId = ShortID.Parse(encryptedContactIdValue);

      Guid contactId;

      using (var provder = new GuidCryptoServiceProvider(Encoding.UTF8.GetBytes(GlobalSettings.PrivateKey), messageShortId.Guid.ToByteArray()))
      {
        contactId = provder.Decrypt(encryptedContactShortId.Guid);
      }
      return ID.Parse(contactId);
    }

This, indeed, looks crazy. 

I've talked to the people from the Sitecore EXM team. They have noticed this and hopefully in the next EXM release, we will be able to get the Contact Id much easier. 
