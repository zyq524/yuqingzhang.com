Tips on Hosting WCF 4 on IIS6
===========================================

:date: 2012-09-07
:tags: .NET, WCF, IIS

In my last project, I had to host a WCF 4 project on IIS6. It was not as straightforward as on IIS7.So I took some notes for my own sake.


Application Pool
------------------------

On my test/prod servers, a default website using .NET 2 has already been hosted. So I created a new virtual directory under the root of that website and put the new WCF web services in that virtual directory. 

The trick was the virtual directory should not use the same application pool as the default website. This is because it is not able to run two different .NET versions in the same application pool. 

The solution was to create a new Application Pool which is only for the application using .NET4 and pointing the WCF services to the new application pool.


Privilege Issues
-----------------------------

I experienced several issues regarding to privilege during the hosting. Basically there are several steps that need to be done.

- Enable .NET 4 aspnet_isapi 

  Execute the following command.
  
  .. image:: static/images/tips-on-hosting-wcf4-on-iis6-1.jpg
  
  
  If you see the status of .NET4 aspnet_isapi.dll is 0, you need to enable it.

  .. image:: static/images/tips-on-hosting-wcf4-on-iis6-2.jpg


  
- Add read permission for NETWORK_SERVICE to your virtual directory.

- If the WCF services need the access to X.509 certificate, you should following the steps described in this post:  http://msdn.microsoft.com/en-us/library/aa702621.aspx


A Custom ServiceHostFactory
---------------------------------------

When I fixed all those privilege issues, I was able to see the service page in the browser. However, the web services URL was using my machine name instead of the IP address. This made it impossible to call the web services from the client side.  

The solution is to create a custom ServiceHostFactory and force the web services to use the address which you have specified. 

Here is the code snippet.
 
.. code-block:: c#

    public class MyServiceFactory : ServiceHostFactory
    {
        protected override ServiceHost CreateServiceHost(Type serviceType, Uri[] baseAddresses)
        {
            var host = new MyServiceHost(serviceType, baseAddresses);
            return host;
        }
    }

    class MyServiceHost : ServiceHost
    {
        public GSTRServiceHost(Type serviceType, params Uri[] baseAddresses)
            : base(serviceType, GetBaseAddresses())
        { }

        protected override void ApplyConfiguration()
        {
            base.ApplyConfiguration();
        }

        // read base addresses from AppSettings in config   
        private static Uri[] GetBaseAddresses()
        {
            List<Uri> addresses = new List<Uri>();
            AddBaseAddress(addresses, "BaseAddress");
            return addresses.ToArray();
        }
        private static void AddBaseAddress(List<Uri> addresses, string key)
        {
            string address = ConfigurationManager.AppSettings[key];
            if (null != address)
            {
                addresses.Add(new Uri(address));
            }
        }
    }

In the above example, I defined the BaseAddress in my web.config file. 

In the .svc file, we point the factory to the custom factory.

.. code-block:: rest

	<%@ ServiceHost Language="C#" Debug="true" Service="Service.MyService" Factory="Service.MyServiceFactory"  %>
	

By doing this, you are able to change the BaseAddress easily.
