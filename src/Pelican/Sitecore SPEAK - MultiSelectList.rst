Sitecore SPEAK - MultiSelectList
========================================

:date: 2014-07-05
:tags: Sitecore, SPEAK

In Sitecore SPEAK, I use ListControl to bind a data source and display items in that data source. The ListControl has selectedItem and selectedItemId attributes so that I can easily access the selected item/row in the list. 

Last week I was asked to create a list that user can select multiple items/rows. I looked into `Sitecore SPEAK Component Reference <http://sdn.sitecore.net/upload/sitecore7/72/speak_component_reference_sc72_a4.pdf>`_ and discovered that there is a control called MultiSelectList. However, the reference doesn't say too much about how to use this control. All I know is that a MultiSelectList is a Behavior control instead of a "real" list control. 

After some investigation and getting help from SPEAK team, I figured out that a Behavior control extends the functionality of a component. In order to add a MultiSelectList Behavior into a ListControl, I need to do the following steps:

- Add a MultiSelectList rendering into the page. It is important that even if the ListControl is on a subpage, the
  MutlitSelectList should still be added on the main page.

 .. image:: static/images/sitecore-speak-multiselectlist-1.png

- In the ListControl, add MultiSelectList into the Behaviors property. No matter what the Id of the MultiSelectList is,
  it only needs to put the name of the control into the Behaviors property. Thus, only one MultiSelectList control is needed on a page and it can be reused by several ListControl controls on that page.

 .. image:: static/images/sitecore-speak-multiselectlist-2.png

That’s it. When I open the page in my browser, I can see the check box in the first column of each row. 

  .. image:: static/images/sitecore-speak-multiselectlist-3.png

There are two more attributes i.e. checkedItems and checkedItemIds been added into the ListCotrol’s attributes.

  .. image:: static/images/sitecore-speak-multiselectlist-4.png

The only issue I have found so far is that in Sitecore 7.2, it seems that I cannot deselect all the selected rows.