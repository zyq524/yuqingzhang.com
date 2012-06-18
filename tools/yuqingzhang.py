from juicebox import upload_images, update_config_xml, update_backgroundColor
from pelicantool import call_pelican
from SitesToAzureBlob import SitesToAzureBlob

def main(account_name = None, account_key = None, ):
    #update_config_xml(r'..\src\main\gallery\2011-09-edinburgh-scotland\config.xml', '2011-09-edinburgh-scotland')
    #update_config_xml(r'..\src\main\gallery\2011-09-highlands-scotland\config.xml', '2011-09-highlands-scotland')
    #update_config_xml(r'..\src\main\gallery\2012-05-stavanger-norway\config.xml', '2012-05-stavanger-norway')
    #update_config_xml(r'../src/main/gallery/2011-09-london-england/config.xml', '2011-09-london-england')
    
    #update_backgroundColor(r'../src/main/gallery/2011-09-london-england/2011-09-london-england.html')
    print 'Juciebox Processed...'
    
    upload_images(account_name, account_key)
    
    try:
        call_pelican('Pelican/settings.py', '../src/Pelican') 
    except Exception, e:
        if e[0] ==5 and e[1] == 'Access is denied':
            try:
                call_pelican('Pelican/settings.py', '../src/Pelican') 

            except Exception, e:
                if e[0] ==5 and e[1] == 'Access is denied':
                    try:
                        call_pelican('Pelican/settings.py', '../src/Pelican') 

                    except Exception, e:
                        raise
    
    print 'Pelican Processed...'

    stb = SitesToAzureBlob('../src/main', '../output', overwrite_output=False, account_name = account_name, account_key = account_key,
                         container_name = 'site')
    stb.upload_files_to_blob()

if __name__ == "__main__":
    main()