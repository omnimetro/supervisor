"""
Configuration WSGI pour SUPERVISOR V2.0

Expose le callable WSGI comme variable au niveau du module nommée ``application``.

Pour plus d'informations sur ce fichier, voir :
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
