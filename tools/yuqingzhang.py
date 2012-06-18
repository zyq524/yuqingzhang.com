from juicebox import upload_images, update_config_xml
from pelicantool import call_pelican
from SitesToAzureBlob import SitesToAzureBlob

def main():
    #update_config_xml(r'..\src\main\gallery\2011-09-edinburgh-scotland\config.xml', '2011-09-edinburgh-scotland')
    #update_config_xml(r'..\src\main\gallery\2011-09-highlands-scotland\config.xml', '2011-09-highlands-scotland')
    #update_config_xml(r'..\src\main\gallery\2012-05-stavanger-norway\config.xml', '2012-05-stavanger-norway')

    #upload_images()
    
    print 'Juciebox Processed...'
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

    stb = SitesToAzureBlob('../src/main', '../output', overwrite_output = False, account_name = 'zhangyuqinglabs', account_key = 'aQLXzo4soX+dK1TYqTeG9dxkdgGpDi8dEbODL8uha5P3bG1WvuczRJDpopO1JKLba6Y9AqX0yEwq/s8Zbo+60Q==',
                         container_name = 'site')
    stb.upload_files_to_blob()

if __name__ == "__main__":
    main()