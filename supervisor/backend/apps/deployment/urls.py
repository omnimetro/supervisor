"""
Configuration des URLs pour l'application deployment.

Routes API REST pour tous les endpoints de l'application.

Endpoints disponibles :
- /api/deployment/operators/ : Gestion des opérateurs télécoms
- /api/deployment/boq-categories/ : Catégories du bordereau de quantités
- /api/deployment/boq-items/ : Articles du bordereau de quantités
- /api/deployment/task-definitions/ : Définitions des types de tâches
- /api/deployment/subcontractors/ : Gestion des sous-traitants
- /api/deployment/technicians/ : Gestion des techniciens
- /api/deployment/projects/ : Gestion des projets/chantiers
- /api/deployment/project-plannings/ : Plannings des projets
- /api/deployment/task-plannings/ : Plannings des tâches
- /api/deployment/daily-reports/ : Rapports journaliers
- /api/deployment/cartography-points/ : Points de cartographie
- /api/deployment/delivery-phases/ : Phases de livraison
- /api/deployment/corrections/ : Corrections demandées
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    OperatorViewSet,
    BOQCategoryViewSet,
    BOQItemViewSet,
    TaskDefinitionViewSet,
    SubcontractorViewSet,
    TechnicianViewSet,
    ProjectViewSet,
    ProjectPlanningViewSet,
    TaskPlanningViewSet,
    DailyReportViewSet,
    CartographyPointViewSet,
    DeliveryPhaseViewSet,
    CorrectionViewSet,
)


# Configuration du router DRF
router = DefaultRouter()

# ============================================
# Enregistrement de tous les ViewSets
# ============================================

# Gestion des opérateurs et BOQ
router.register(r'operators', OperatorViewSet, basename='operator')
router.register(r'boq-categories', BOQCategoryViewSet, basename='boqcategory')
router.register(r'boq-items', BOQItemViewSet, basename='boqitem')
router.register(r'task-definitions', TaskDefinitionViewSet, basename='taskdefinition')

# Gestion des ressources humaines
router.register(r'subcontractors', SubcontractorViewSet, basename='subcontractor')
router.register(r'technicians', TechnicianViewSet, basename='technician')

# Gestion des projets et plannings
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-plannings', ProjectPlanningViewSet, basename='projectplanning')
router.register(r'task-plannings', TaskPlanningViewSet, basename='taskplanning')

# Suivi terrain
router.register(r'daily-reports', DailyReportViewSet, basename='dailyreport')
router.register(r'cartography-points', CartographyPointViewSet, basename='cartographypoint')

# Livraison et corrections
router.register(r'delivery-phases', DeliveryPhaseViewSet, basename='deliveryphase')
router.register(r'corrections', CorrectionViewSet, basename='correction')

app_name = 'deployment'

urlpatterns = [
    path('', include(router.urls)),
]
