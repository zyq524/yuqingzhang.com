Sitecore SPEAK - Repeater
========================================

:date: 2014-11-11
:tags: Sitecore, SPEAK

I've used dozens of Sitecore SPEAK components from Sitecore 7.2 in the last half year, and I have to say the most confusing one for me is the Repeater component. 

After reading the documentation, I know that the Repeater component doesn't render items by itself, which means that renderings are not added to the Repeater component directly. 

Instead, I need to define a template for the items that I want to render and add all the renderings to that template’s standard values. Afterwards I create items from that template and the Repeater component only needs to bind to them.

I am going to create a page that has a Repeater component on it. The Repeater component can display the football match results. Each match result is an item of the Repeater component.

First things first, I create a MatchResult template in my Playground application’s template folder. The template has four fields. 

 .. image:: static/images/sitecore-speak-repeater-1.png

I also create the standard values for this template. Open the Design Layout of _Standard Values, I add the SPEAK components that are needed to render one match result. It is important not to forget to select a layout, I use Speak-EmptyLayout here. 

 .. image:: static/images/sitecore-speak-repeater-2.png

This is how I bind the field data to the Text component.

 .. image:: static/images/sitecore-speak-repeater-3.png

Since I have a template, I can start to create the items. I created two items based on MatchResult template.

 .. image:: static/images/sitecore-speak-repeater-4.png

Now I switch to my Playground page’s layout and add a Repeater component to it. In the Items property I need to assign that two match results items. In order to achieve this, I create a SearchDataSource that can find the two items and binding the DataSource.Items to the Items property of the Repeater component.

 .. image:: static/images/sitecore-speak-repeater-5.png

 .. image:: static/images/sitecore-speak-repeater-6.png

I open my browser and go to my playground page, two match results have been rendered correctly.

 .. image:: static/images/sitecore-speak-repeater-7.png
 
So far so good. The issue caught me out is that I need to create item for each match result in the core database. This is a bit weird. Because what if the match results have already been saved in the master database? Why should I keep another copy in the core database? 

Maybe SPEAK’s idea is that the items in the master database are kind of models for the backend and those items in the core database are ViewModels in the frontend, but it is truly overloaded to keep all these items in the core database.

The way I can figure out is to create these items as temporary items on the fly by using Sitecore Item Web API and delete them right after it has been rendered in the Repeater. 

All the rendered items of the Repeater can be accessed through MatchResultReapter.RenderedItems. When the “add” event of the RenderedItems is triggered, I can call item.toModel().destroy(); to delete the item just created.

I know this is nasty. My wish is that in the future it would be possible to use JSON objects as data instead items in the core database. 

Last thing, to access the rendering components of each MatchResult item in the MatchResultRepeater, I use the “app” attribute. For example, to access the components of the first match result:

 .. image:: static/images/sitecore-speak-repeater-8.png