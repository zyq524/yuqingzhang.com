Lessons Learned from VSTO2010 Development
===========================================

:date: 2012-08-24
:tags: .NET, VSTO2010

In the last few months, I have been involving in a project which uses Excel Add-in (VSTO 2010) as the user interface. 

Basically, there is no vast difference between VSTO development and WinForm development. However, there were some tricks/tips that I learned.

Deployment
-----------

I deployed the project using Windows Installer, which followed this article: 
http://msdn.microsoft.com/en-us/library/ff937654.aspx


App.config
-----------


Not like WinForm, all the VSTO2010 Add-in uses the app.config which comes with Microsoft Office. Take my project for instance, I created an app.config for the Excel Add-in and it worked perfectly in the development environment. But it failed to read that app.config after it was installed by the .msi package. 


To fix this, right click the installer project, choose View->Registry. Under the User/Machine Hive, find the Manifest of your application and add file:/// to the value.


The incorrect form: [TARGETDIR]Addin.vsto|vstolocal .

The correct form: file:/// [TARGETDIR]Addin.vsto|vstolocal

Installation
-------------

Typically, user needs to install .NET 4 Client Profile and VSTO Runtime before installing the Add-in. 


But I received several installation failure feedbacks from our customers. They are all using Office 2007 sp2 and it turns out that if you are using that version of Office, besides the two standard perquisites, an additional hotfix is also needed.  http://support.microsoft.com/kb/976477/