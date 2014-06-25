from juicebox import upload_images, update_config_xml, create_index_page
from pelicantool import call_pelican
from SitesToAzureBlob import SitesToAzureBlob

###################
# Create a folder called juicebox in the src folder.
# Modify update_config_xml 
# Modify create_index_page
# uplaad_images
# upload_files_to_blob
###################
def main(account_name = None, account_key = None, ):

    #update_config_xml(r'../src/main/footprints/2013-06-paris-france/config.xml',r'http://zhangyuqinglabs.blob.core.windows.net/gallery/', r'2013-06-paris-france');
    ##update_config_xml(r'../src/main/footprints/2013-01-milano-italy/config.xml',r'http://zhangyuqinginfo.blob.core.windows.net/gallery/', r'2013-01-milano-italy');

    #create_index_page('../src/main/footprints', '2013-06-paris-france', 'Paris, France')
    ##create_index_page('../src/main/footprints', '2013-01-milano-italy', 'Milano, Italy')
    #print 'Juciebox Processed...'
    
    #upload_images(account_name, account_key)
    
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

    stb = SitesToAzureBlob('../src/main', '../output', overwrite_output=False, account_name = account_name, account_key = account_key, container_name = 'site')
    stb.upload_files_to_blob()

if __name__ == "__main__":
    main(account_name='zhangyuqinglabs', account_key='mnQomACu6uYI1rJaLtR1ObumgxXdo6Fly3klTizyelefCAh1kZ+NNwodM8VGPs/mjnMiE9WfcPKZF0S5KgWM5Q==')