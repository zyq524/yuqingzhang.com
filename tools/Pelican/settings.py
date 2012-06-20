import os

AUTHOR = u'Qing'
SITENAME = u"Qing's Blogs"
SITEURL = 'http://www.yuqingzhang.com'
TIMEZONE = "Europe/Copenhagen"

#THEME = "/Users/zhangyuqing524/Dropbox/Public/Pelican/themes/yuqingzhang"
THEME = "themes/yuqingzhang"
DATE_FORMAT = {
    'en': '%d %b %Y'
}
OUTPUT_PATH = '../../src/main/posts/'

DISQUS_SITENAME = "yuqingzhang"
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True
#LOCALE = ""

DEFAULT_CATEGORY = 'my blog'

FEED_RSS = 'feeds/all.rss.xml'

DIRECT_TEMPLATES = ('index', 'tags', 'archives')

# global metadata to all the contents
#DEFAULT_METADATA = (('yeah', 'it is'),)

# static paths will be copied under the same name
STATIC_PATHS = ["images", ]

# A list of files to copy from the source to the destination
FILES_TO_COPY = (('extra/robots.txt', 'robots.txt'),)
