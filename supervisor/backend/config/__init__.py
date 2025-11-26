"""
Configuration du projet SUPERVISOR V2.0
"""

# Ceci garantira que l'application Celery est toujours importée
# quand Django démarre, afin que shared_task utilise cette application.
from .celery import app as celery_app

__all__ = ('celery_app',)
