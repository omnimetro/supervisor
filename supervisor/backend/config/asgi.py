"""
Configuration ASGI pour SUPERVISOR V2.0

Expose le callable ASGI comme variable au niveau du module nommée ``application``.

Pour plus d'informations sur ce fichier, voir :
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
