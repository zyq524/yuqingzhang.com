How To User WCF Username Authentication
========================================

:date: 2012-04-25
:tags: .NET, WCF 

This document describes the steps to use WCF username authentication.

The goal
---------


The goal is to make the WCF services authenticate the client based on the username and password. Here, we assume that the usernames and passwords are saved in a database created by ASP.NET membership provider.


To achieve the goal, we need to configure both the server side and the client side.


Server Side
------------


We host the WCF services by ASP.NET/IIS7. All the WCF configurations are defined in Web.config file.


The <services /> part in Web.config file is like:



.. code-block:: xml

	<services>
	<service behaviorConfiguration="CustomValidator"
	   name="GSTR.ServiceLib.SecurityClasses.Compression">

	<endpoint address="" binding="wsHttpBinding"
	   bindingConfiguration="wsHttpWithMessageSecurity"
		   contract="GSTR.ServiceLib.Contracts.ICompression" />
		
		<endpoint address="mex" binding="mexHttpBinding" contract="IMetadataExchange" />
	 </service>
	</services>

	
	
The root endpoint address is the root of the IIS site in which it was hosted. To use username authentication we need to use wsHttpBinding. The bindingConfiguration indicates that there is a binding named wsHttpMessageSecurity, which is like:



.. code-block:: xml

	<bindings>
	  <wsHttpBinding>
		<binding name="wsHttpWithMessageSecurity">
		  <security mode="Message">
			<message clientCredentialType="UserName" />
		  </security>
		</binding>
	  </wsHttpBinding>
	</bindings>

	
	
We can see that the security mode is Message (so we don’t need https, https is necessary for Transport), and the clientCrentialtype is UserName.


The service section in Web.config file also mentioned a behaviorConfiguration called CustomValidator. The definition is like:



.. code-block:: xml

	<behaviors>
	  <serviceBehaviors>
		<behavior name="CustomValidator">
		  <serviceMetadata httpGetEnabled="true"/>
		  <serviceCredentials>
			<serviceCertificate
			  findValue="19 00 fd 20 78 fd 2c 2d c5 83 16 50 28 c2 67 e5 ff dc d4 77"
			  x509FindType="FindByThumbprint"
			  storeLocation="LocalMachine" storeName="My" />
			<userNameAuthentication userNamePasswordValidationMode ="MembershipProvider"
					membershipProviderName ="AspNetSqlMembershipProvider"/>
		  </serviceCredentials>
		</behavior>
	  </serviceBehaviors>
	</behaviors>

	
	
The interesting part is the <serviceCertificate />. It points to an X.509 certificate installed on the server, the certificate can be found on Local Computer\Personal\Certificates by its thumbprint.


WCF insists that the services must use an X.509 certificate to encrypt the username and password to the services and the certificate must contain a private key. During the development phase, we use a temporary certificate.  In order to create and install the certificate, we need to the steps described here: http://msdn.microsoft.com/en-us/library/ff647171.aspx


One thing that needs to be noticed is that IIS7/IIS7.5 using ApplicationPoolIdentity instead of NetworkService as the Identity. We can start the IIS manager, click Application Pools and find DefaultAppPool, on the right panel, click Advanced Settings…, find Process Model, and then change the Identity to NetworkService.


When debug the application, we may need to add the following section into <behavior /> and check the error in Event Viewer.



.. code-block:: xml

	<serviceSecurityAudit auditLogLocation="Application"
	  serviceAuthorizationAuditLevel="Failure" messageAuthenticationAuditLevel="Failure"
	  suppressAuditFailure="true" />

	  
Refer to http://devworkexperience.com/tag/servicesecurityaudit/


We can also add a custom validate for the username. Create a new .cs file in the Asp.net project. Add a new class inherits from UserNamePasswordValidator and overrides the Validate method.



.. code-block:: c#

    public class CustomValidator : UserNamePasswordValidator
    {
        public override void Validate(string userName, string password)
        {
            // peform
            if (null == userName || null == password)
            {
                throw new ArgumentNullException();
            }

            if (!Membership.ValidateUser(userName, password))
            {
                throw new SecurityTokenException("Unknown Username or Incorrect Password");
            }
        

		
We then replace the userNameAuthentication section with:



.. code-block:: xml

	<userNameAuthentication userNamePasswordValidationMode="Custom" customUserNamePasswordValidatorType="GSTR.ServiceSite.Authentication.CustomValidator,GSTR.ServiceSite" />


	
Besides, we need to specify the membership provider to use Forms authentication mode instead of Windows.



.. code-block:: xml

	<authentication mode="Forms" />


	
Now the server side is ready.



The Client
-----------


We add a service reference to the client application. Basically it takes care of the configurations automatically and nicely.


Here is an example:



.. code-block:: c#


	ServiceClient client = new ServiceClient();
	string url = ConfigurationManager.AppSettings["GSTRWebServiceUrl"].ToString();
	string dns = ConfigurationManager.AppSettings["IdentityDNS"].ToString();

	if (!string.IsNullOrEmpty(url))
	{
		client.Endpoint.Address = new EndpointAddress(new Uri(ConfigurationManager.AppSettings["GSTRWebServiceUrl"].ToString()),
			DnsEndpointIdentity.CreateDnsIdentity(ConfigurationManager.AppSettings["IdentityDNS"].ToString()));
	}

	client.ClientCredentials.UserName.UserName = "test";
	client.ClientCredentials.UserName.Password = "test123";

	
	
This is all. 