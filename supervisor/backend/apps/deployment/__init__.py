"""
Application Django pour la gestion des chantiers de déploiement.

Cette application gère :
- Les opérateurs télécom (Orange, Moov)
- Les BOQ (Bordereau de Quantité) avec nomenclature des travaux
- Les chantiers de déploiement (backbone, transport, distribution)
- Le planning prévisionnel des travaux et tâches
- Les rapports quotidiens d'exécution
- La cartographie des infrastructures
- Les phases de livraison et corrections
"""

default_app_config = 'apps.deployment.apps.DeploymentConfig'
