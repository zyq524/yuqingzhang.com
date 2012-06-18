from SitesToAzureBlob import SitesToAzureBlob
from xml.dom.minidom import parse, parseString
import os, filecmp

def upload_images():
    stb = SitesToAzureBlob('../src/juicebox/gallery/', 
                           '../output/gallery/', overwrite_output = False,
                           account_name = 'zhangyuqinglabs', account_key = 'aQLXzo4soX+dK1TYqTeG9dxkdgGpDi8dEbODL8uha5P3bG1WvuczRJDpopO1JKLba6Y9AqX0yEwq/s8Zbo+60Q==',
                           container_name = 'gallery')

    stb.upload_files_to_blob()

def update_config_xml(config_xml_path, gallery_name):
    image_container = 'http://zhangyuqinglabs.blob.core.windows.net/garllery/'
    dom = parse(os.path.abspath(config_xml_path))
    images = dom.getElementsByTagName('image')
    for image in images:
        if not image.image.attributes['linkURL'].value.startswith(image_container):
            image.attributes['linkURL'].value = (image_container + gallery_name + '/' + image.attributes['linkURL'].value).lower()
            image.attributes['thumbURL'].value = (image_container+ gallery_name + '/' + image.attributes['thumbURL'].value).lower()
            image.attributes['imageURL'].value = (image_container + gallery_name + '/' + image.attributes['imageURL'].value).lower()
    f = open(os.path.abspath(config_xml_path), 'w')
    dom.writexml(f)
    f.close()

