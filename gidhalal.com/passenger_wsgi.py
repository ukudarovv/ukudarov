# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1584479/data/www/gidhalal.com/halal')
sys.path.insert(1, '/var/www/u1584479/data/env/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'halal.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
