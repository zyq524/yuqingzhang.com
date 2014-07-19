Sitecore SPEAK - Could not select row in ListControl
=====================================================

:date: 2014-07-19
:tags: Sitecore, SPEAK

I use ListControl from SPEAK a lot in my current project and much of the time I use self-defined datasource components for ListControl's items. 

This week, I bind a ListControl to a new data source as usual. Just an example, the data source is a JSON object array. 

 .. image:: static/images/sitecore-speak-could-not-select-row-in-listcontrol-1.png

I bind a ListControl to this datasource.

 .. image:: static/images/sitecore-speak-could-not-select-row-in-listcontrol-2.png

The control displays the items as expected, so far so good. 

 .. image:: static/images/sitecore-speak-could-not-select-row-in-listcontrol-3.png

However, I could not select any row in this list. 

The reason is that the "selectedItem" or "selectedItemId" attribute of a ListControl requires an default "itemId" property from the datasource and the items in my JSON object array do not have "itemId" field. When I add the "itemId" into each object in my JSON object array, I can select the row again.

  .. image:: static/images/sitecore-speak-could-not-select-row-in-listcontrol-4.png

  .. image:: static/images/sitecore-speak-could-not-select-row-in-listcontrol-5.png

In sum, when we define a datasource component for ListControl, we need to make sure that we include the "itemId" for each item in the datasource.