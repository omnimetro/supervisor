"""
Configuration Celery pour SUPERVISOR V2.0

Pour plus d'informations sur Celery avec Django :
https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""

import os
from celery import Celery

# Définir le module de paramètres Django par défaut pour le programme 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('supervisor')

# Utiliser une chaîne ici signifie que le worker n'a pas besoin de
# sérialiser l'objet de configuration aux processus enfants.
# - namespace='CELERY' signifie que tous les paramètres liés à celery
#   devraient avoir un préfixe `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger automatiquement les tâches de toutes les applications enregistrées.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tâche de debug pour tester Celery"""
    print(f'Request: {self.request!r}')
