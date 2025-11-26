"""
Configuration de l'application deployment.
"""

from django.apps import AppConfig


class DeploymentConfig(AppConfig):
    """Configuration de l'application Deployment."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.deployment'
    verbose_name = 'Gestion des Chantiers de Déploiement'

    def ready(self):
        """
        Méthode appelée lorsque l'application est prête.
        Utilisée pour enregistrer les signals, etc.
        """
        # Import des signals si nécessaire
        # import apps.deployment.signals
        pass
