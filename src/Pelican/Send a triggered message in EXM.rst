Send a triggered message in EXM
=======================================================================

:date: 2015-06-23
:tags: Sitecore, Sitecore 8, Email Experience Manager

The biggest change in Sitecore Email Experience Manager (EXM) module was that it introduced using the contact in xDB instead of the Sitecore User to represent the recipient. This gives a lot flexibility, but also means that we need to change our existing code.

One of the common tasks by using EXM is sending a triggered message that could be triggered by user filling out a form, etc. We can use the Sitecore API to send the message. In ECM, basically we passed the Sitecore User to the SendStandardMessage by querying the username. 

This is no long valid in EXM. In EXM, we need to create or query a contact from the xDB, and then pass the contact to the SendStandardMessage.

For example, if a client fills out a form, which includes his first name, last name, email address. A triggered message (a welcome message, etc) should be sent to him.

To achieve this, we create a contact if it doesn't exist and get its contact Id. Otherwise, we find the contact Id in xDB by using the identifier of the contact. In this case, let's assume that the identifier is the email address.

Then we can use the following code to send the triggered message to that contact.

.. code-block:: c#

	public void SendTriggeredMessage(Guid messageId, Guid contactId, bool usePreferredLanguage = false,
		IDictionary<string, object> customPersonTokens = null)
	{
		Assert.ArgumentNotNull(messageId, "messageId");
		Assert.ArgumentNotNull(contactId, "contactId");

		RecipientId recipientId = RecipientRepository.GetDefaultInstance().ResolveRecipientId("xdb:" + contactId);

		Sitecore.Modules.EmailCampaign.Application.Application.Instance.EmailDispatch.SendTriggered(messageId, recipientId, usePreferredLanguage, customPersonTokens);
	}
