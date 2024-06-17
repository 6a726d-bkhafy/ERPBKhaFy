"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os,sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/netsys/core')
sys.path.append('/var/www/netsys/venv/lib/python3.10/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

activate_this = '/var/www/netsys/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

application = get_wsgi_application()
