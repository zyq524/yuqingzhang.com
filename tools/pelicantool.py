from pelican import Pelican
from pelican.settings import read_settings
import os

def call_pelican(settings_path, content_path):
    settings_path = os.path.abspath(settings_path)
    content_path = os.path.abspath(content_path)
    
    settings = read_settings(settings_path)
    settings_dir = os.path.split(settings_path)[0]
    curdir=os.getcwd()
    os.chdir(settings_dir)
    settings['THEME'] = os.path.abspath(settings['THEME'])
    os.chdir(curdir)
    p = Pelican(settings = settings)
    p.run()