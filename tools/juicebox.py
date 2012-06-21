from SitesToAzureBlob import SitesToAzureBlob
from xml.dom.minidom import parse
import os

def upload_images(account_name, account_key):
    stb = SitesToAzureBlob('../src/juicebox/', 
                           '../output/gallery/', overwrite_output = False,
                           account_name = account_name, account_key = account_key,
                           container_name = 'gallery')

    stb.upload_files_to_blob()
def create_index_page(dst_folder, albumn_name, page_title):
    index_page_path = os.path.abspath(os.path.join(dst_folder, albumn_name, albumn_name + '.html'))
    #if not os.path.exists(index_page_path):
    content = '''<!DOCTYPE html>
    <html lang="en">
        <head>
            <title>'''
    content = content + page_title
    content = content +'''</title>
            <meta charset="utf-8" />
            <meta name="apple-mobile-web-app-capable" content="yes" />
			<meta name="description" content="YuQing Zhang's footprints">
			<meta name="keywords" content="YuQing Zhang, Yuqing Zhang, Qing Zhang, Qing">
			<meta name="author" content="YuQing Zhang">
            <style type="text/css">
                body {
                    margin: 0px;
                }
            </style>
            <link rel="shortcut icon" href="../../static/imgs/favicon.ico">
        </head>
        <body>
            <!--START JUICEBOX EMBED-->
            <script src="../jbcore/juicebox.js"></script>
            <script>
                new juicebox({
                    containerId : 'juicebox-container',
                    galleryWidth: '100%',
                    galleryHeight: '100%',
                    backgroundColor: 'white'
                });
            </script>
            <div id="juicebox-container"></div>
            <!--END JUICEBOX EMBED-->
        </body>
    </html>'''
    f = open(index_page_path, 'w')
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

if __name__ == "__main__":
    create_index_page('../src/main/footprints', '2011-09-london-england', 'London, England')
