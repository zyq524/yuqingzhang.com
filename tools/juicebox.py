from SitesToAzureBlob import SitesToAzureBlob
from xml.dom.minidom import parse
import os

def upload_images(account_name, account_key):
    stb = SitesToAzureBlob('../src/juicebox/', 
                           '../output/gallery/', overwrite_output = False,
                           account_name = account_name, account_key = account_key,
                           container_name = 'gallery')

    stb.upload_files_to_blob()

def update_backgroundColor(index_page_path):
    content = open(os.path.abspath(index_page_path), 'r').read()
    content = content.replace('backgroundColor: \'#222222\'', 'backgroundColor: \'white\'')
    f = open(os.path.abspath(index_page_path), 'w')
    f.write(content)
    f.close()
    
def update_config_xml(config_xml_path, gallery_name):
    image_container = 'http://zhangyuqinglabs.blob.core.windows.net/gallery/'
    dom = parse(os.path.abspath(config_xml_path))
    images = dom.getElementsByTagName('image')
    for image in images:
        if not image.attributes['linkURL'].value.startswith(image_container):
            image.attributes['linkURL'].value = (image_container + gallery_name + '/' + image.attributes['linkURL'].value).lower()
            image.attributes['thumbURL'].value = (image_container+ gallery_name + '/' + image.attributes['thumbURL'].value).lower()
            image.attributes['imageURL'].value = (image_container + gallery_name + '/' + image.attributes['imageURL'].value).lower()
    f = open(os.path.abspath(config_xml_path), 'w')
    dom.writexml(f)
    f.close()

