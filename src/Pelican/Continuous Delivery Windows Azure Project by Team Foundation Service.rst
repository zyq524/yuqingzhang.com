Continuous Delivery Windows Azure Project by Team Foundation Service
=======================================================================

:date: 2012-11-02
:tags: Windows Azure, Team Foundation Service

In my recent Windows Azure project, I’m using the Team Foundation Service http://tfs.visualstudio.com/en-us/ for the project planning, source code control, etc. It is also possible to deploy the project continuously to Windows Azure .http://www.windowsazure.com/en-us/develop/net/common-tasks/publishing-with-tfs/

Pretty cool. However, I have a Staging configuration and a Prod configuration in my project. Both need to be deployed to Windows Azure, and each has its own cscfg and csdef file(for different storage connection strings, certificates, etc). My goal is that to make the build script be able to pick the cscfg and csdef for the corresponding configuration.

I added the cscfg files followed by Joel’s post http://blog.slalom.com/2011/08/19/building-and-deploying-windows-azure-projects-using-msbuild-and-tfs-2010/ and changed my build process as below for staging for instance.

  .. image:: images/continuous-delivery-windows-azure-project-by-team-foundation-service-1.png
  
The Team Foundation Service picked the staging.cscfg file correctly, but it failed to use the staging.csdef. I followed the steps Joel mentioned in his post for the definition file, but TFS always used the csdef file which I defined in the ItemGroup which includes the cscfg files. 

To solve this, I added a pre-build event for the Windows Azure project: 

.. code-block:: console

	copy /Y "$(ProjectDir)ServiceDefinition.$(ConfigurationName).csdef" "$(ProjectDir)ServiceDefinition.csdef". 

But there is another problem. If the ServiceDefiniton has already been in the TFS build folder, the access to replace this file may be denied. So what I did was that I removed ServiceDefiniton.csdef from the source control and that solved the problem. 

Now, I can happily deploy my project to the staging and prod environment with different cscfg and csdef files. 