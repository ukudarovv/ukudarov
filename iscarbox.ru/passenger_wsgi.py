import os, sys
sys.path.insert(0, '/var/www/u1164392/data/www/iscarbox.ru/iscarbox')
sys.path.insert(1, '/var/www/u1164392/data/djangoenv/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'iscarbox.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()