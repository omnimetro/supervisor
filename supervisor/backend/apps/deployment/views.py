"""
Vues et ViewSets pour l'application deployment.

Ce fichier contient tous les ViewSets pour l'API REST :
- OperatorViewSet : Opérateurs télécom
- BOQCategoryViewSet : Catégories de travaux du BOQ
- BOQItemViewSet : Éléments du BOQ avec prix
- TaskDefinitionViewSet : Définitions de tâches AIV
- SubcontractorViewSet : Entreprises sous-traitantes
- SpecialiteViewSet : Spécialités techniques
- TechnicianViewSet : Techniciens AIV
- ProjectViewSet : Chantiers de déploiement
- ProjectPlanningViewSet : Planning prévisionnel travaux
- TaskPlanningViewSet : Planning prévisionnel tâches
- DailyReportViewSet : Rapports quotidiens
- CartographyPointViewSet : Points cartographiques
- DeliveryPhaseViewSet : Phases de livraison
- CorrectionViewSet : Corrections
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Q

from .models import (
    Operator, BOQCategory, BOQItem, TaskDefinition,
    Subcontractor, Specialite, Technician, Project, ProjectPlanning,
    TaskPlanning, DailyReport, CartographyPoint,
    DeliveryPhase, Correction
)
from .serializers import (
    OperatorSerializer, BOQCategorySerializer,
    BOQItemSerializer, BOQItemListSerializer,
    TaskDefinitionSerializer, SubcontractorSerializer,
    SpecialiteSerializer, TechnicianSerializer,
    ProjectSerializer, ProjectListSerializer,
    ProjectPlanningSerializer, TaskPlanningSerializer,
    DailyReportSerializer, CartographyPointSerializer,
    DeliveryPhaseSerializer, DeliveryPhaseListSerializer,
    CorrectionSerializer
)


# ============================================
# VIEWSETS DE RÉFÉRENCE
# ============================================

class OperatorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des opérateurs télécom.

    Endpoints:
    - GET /api/deployment/operators/ : Liste des opérateurs
    - POST /api/deployment/operators/ : Créer un opérateur
    - GET /api/deployment/operators/{id}/ : Détail d'un opérateur
    - PUT /api/deployment/operators/{id}/ : Modifier un opérateur
    - PATCH /api/deployment/operators/{id}/ : Modification partielle
    - DELETE /api/deployment/operators/{id}/ : Supprimer un opérateur
    - GET /api/deployment/operators/active/ : Liste des opérateurs actifs
    """

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'code']
    search_fields = ['code', 'nom', 'contact_nom', 'contact_email']
    ordering_fields = ['nom', 'code', 'created_at']
    ordering = ['nom']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne uniquement les opérateurs actifs."""
        active_operators = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_operators, many=True)
        return Response(serializer.data)


class BOQCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des catégories BOQ.

    Endpoints:
    - GET /api/deployment/boq-categories/ : Liste des catégories
    - POST /api/deployment/boq-categories/ : Créer une catégorie
    - GET /api/deployment/boq-categories/{id}/ : Détail d'une catégorie
    - PUT /api/deployment/boq-categories/{id}/ : Modifier
    - DELETE /api/deployment/boq-categories/{id}/ : Supprimer
    """

    queryset = BOQCategory.objects.all()
    serializer_class = BOQCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['code', 'nom', 'description']
    ordering_fields = ['nom', 'code', 'created_at']
    ordering = ['nom']


class BOQItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des éléments BOQ.

    Endpoints:
    - GET /api/deployment/boq-items/ : Liste des éléments BOQ
    - POST /api/deployment/boq-items/ : Créer un élément
    - GET /api/deployment/boq-items/{id}/ : Détail d'un élément
    - PUT /api/deployment/boq-items/{id}/ : Modifier
    - DELETE /api/deployment/boq-items/{id}/ : Supprimer
    """

    queryset = BOQItem.objects.select_related(
        'operator', 'category'
    ).prefetch_related('tasks').all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['operator', 'category', 'unite', 'is_active']
    search_fields = ['code', 'libelle', 'description']
    ordering_fields = ['code', 'libelle', 'prix_unitaire', 'created_at']
    ordering = ['operator', 'category', 'code']

    def get_serializer_class(self):
        """Utilise un serializer simplifié pour les listes."""
        if self.action == 'list':
            return BOQItemListSerializer
        return BOQItemSerializer


class TaskDefinitionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des définitions de tâches AIV.

    Endpoints:
    - GET /api/deployment/task-definitions/ : Liste des tâches
    - POST /api/deployment/task-definitions/ : Créer une tâche
    - GET /api/deployment/task-definitions/{id}/ : Détail
    - PUT /api/deployment/task-definitions/{id}/ : Modifier
    - DELETE /api/deployment/task-definitions/{id}/ : Supprimer
    """

    queryset = TaskDefinition.objects.prefetch_related('boq_items').all()
    serializer_class = TaskDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unite', 'is_active']
    search_fields = ['code', 'libelle', 'description']
    ordering_fields = ['code', 'libelle', 'kpi', 'created_at']
    ordering = ['code']


class SubcontractorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des sous-traitants.

    Endpoints:
    - GET /api/deployment/subcontractors/ : Liste des sous-traitants
    - POST /api/deployment/subcontractors/ : Créer un sous-traitant
    - GET /api/deployment/subcontractors/{id}/ : Détail
    - PUT /api/deployment/subcontractors/{id}/ : Modifier
    - DELETE /api/deployment/subcontractors/{id}/ : Supprimer
    - GET /api/deployment/subcontractors/active/ : Sous-traitants actifs
    """

    queryset = Subcontractor.objects.all()
    serializer_class = SubcontractorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'code']
    search_fields = ['code', 'nom', 'telephone', 'email', 'contact_principal_nom']
    ordering_fields = ['nom', 'code', 'date_debut_collaboration', 'created_at']
    ordering = ['nom']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne uniquement les sous-traitants actifs."""
        active_subcontractors = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_subcontractors, many=True)
        return Response(serializer.data)


# ============================================
# VIEWSETS RESSOURCES HUMAINES
# ============================================

class SpecialiteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des spécialités techniques.

    Endpoints:
    - GET /api/deployment/specialites/ : Liste des spécialités
    - POST /api/deployment/specialites/ : Créer une spécialité
    - GET /api/deployment/specialites/{id}/ : Détail d'une spécialité
    - PUT /api/deployment/specialites/{id}/ : Modifier
    - PATCH /api/deployment/specialites/{id}/ : Modification partielle
    - DELETE /api/deployment/specialites/{id}/ : Supprimer
    - GET /api/deployment/specialites/active/ : Spécialités actives
    """

    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'code']
    search_fields = ['code', 'nom', 'description']
    ordering_fields = ['ordre', 'nom', 'code', 'created_at']
    ordering = ['ordre', 'nom']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne uniquement les spécialités actives."""
        active_specialites = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_specialites, many=True)
        return Response(serializer.data)


class TechnicianViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des techniciens AIV.

    Endpoints:
    - GET /api/deployment/technicians/ : Liste des techniciens
    - POST /api/deployment/technicians/ : Créer un technicien
    - GET /api/deployment/technicians/{id}/ : Détail
    - PUT /api/deployment/technicians/{id}/ : Modifier
    - DELETE /api/deployment/technicians/{id}/ : Supprimer
    - GET /api/deployment/technicians/active/ : Techniciens actifs
    - GET /api/deployment/technicians/by-specialite/ : Par spécialité
    """

    queryset = Technician.objects.select_related('specialite').all()
    serializer_class = TechnicianSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'specialite', 'niveau_competence', 'est_chef_chantier', 'is_active'
    ]
    search_fields = ['matricule', 'nom', 'prenoms', 'telephone', 'email']
    ordering_fields = ['matricule', 'nom', 'date_embauche', 'created_at']
    ordering = ['matricule']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne uniquement les techniciens actifs."""
        active_technicians = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_technicians, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_specialite(self, request):
        """Retourne les techniciens groupés par spécialité."""
        specialite = request.query_params.get('specialite')
        if not specialite:
            return Response(
                {'error': 'Le paramètre "specialite" est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        technicians = self.queryset.filter(specialite=specialite, is_active=True)
        serializer = self.get_serializer(technicians, many=True)
        return Response(serializer.data)


# ============================================
# VIEWSETS GESTION DE PROJET
# ============================================

class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets/chantiers.

    Endpoints:
    - GET /api/deployment/projects/ : Liste des projets
    - POST /api/deployment/projects/ : Créer un projet
    - GET /api/deployment/projects/{id}/ : Détail d'un projet
    - PUT /api/deployment/projects/{id}/ : Modifier
    - DELETE /api/deployment/projects/{id}/ : Supprimer
    - GET /api/deployment/projects/active/ : Projets actifs
    - GET /api/deployment/projects/delayed/ : Projets en retard
    - GET /api/deployment/projects/{id}/statistics/ : Statistiques du projet
    """

    queryset = Project.objects.select_related(
        'operator', 'superviseur_aiv'
    ).all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'operator', 'type_projet', 'statut', 'zone_geographique',
        'superviseur_aiv'
    ]
    search_fields = ['code', 'nom', 'zone_geographique', 'description']
    ordering_fields = ['code', 'nom', 'date_debut', 'date_fin_prevue', 'created_at']
    ordering = ['-date_debut']

    def get_serializer_class(self):
        """Utilise un serializer simplifié pour les listes."""
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retourne les projets en cours."""
        active_projects = self.queryset.filter(
            statut__in=['planifie', 'en_cours', 'en_livraison']
        )
        serializer = self.get_serializer(active_projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def delayed(self, request):
        """Retourne les projets en retard."""
        from datetime import date
        delayed_projects = self.queryset.filter(
            statut__in=['planifie', 'en_cours', 'en_livraison'],
            date_fin_prevue__lt=date.today()
        )
        serializer = self.get_serializer(delayed_projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Retourne des statistiques détaillées sur le projet."""
        project = self.get_object()

        stats = {
            'code': project.code,
            'nom': project.nom,
            'progression_percentage': project.get_progression_percentage(),
            'total_tasks': project.get_total_tasks(),
            'completed_tasks': project.get_completed_tasks(),
            'is_delayed': project.is_delayed(),
            'travaux_ok': project.travaux_ok,
            'environnement_ok': project.environnement_ok,
            'vt_ok': project.vt_ok,
            'pv_ok': project.pv_ok,
        }

        return Response(stats)


class ProjectPlanningViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion du planning prévisionnel des travaux.

    Endpoints:
    - GET /api/deployment/project-plannings/ : Liste des plannings
    - POST /api/deployment/project-plannings/ : Créer un planning
    - GET /api/deployment/project-plannings/{id}/ : Détail
    - PUT /api/deployment/project-plannings/{id}/ : Modifier
    - DELETE /api/deployment/project-plannings/{id}/ : Supprimer
    """

    queryset = ProjectPlanning.objects.select_related(
        'project', 'project__operator', 'boq_item', 'boq_item__category'
    ).all()
    serializer_class = ProjectPlanningSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'project__operator', 'boq_item', 'boq_item__category']
    search_fields = ['project__code', 'project__nom', 'boq_item__code', 'boq_item__libelle']
    ordering_fields = ['project', 'ordre', 'quantite_prevue', 'created_at']
    ordering = ['project', 'ordre']


class TaskPlanningViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion du planning prévisionnel des tâches.

    Endpoints:
    - GET /api/deployment/task-plannings/ : Liste des tâches planifiées
    - POST /api/deployment/task-plannings/ : Créer une tâche
    - GET /api/deployment/task-plannings/{id}/ : Détail
    - PUT /api/deployment/task-plannings/{id}/ : Modifier
    - DELETE /api/deployment/task-plannings/{id}/ : Supprimer
    - GET /api/deployment/task-plannings/delayed/ : Tâches en retard
    """

    queryset = TaskPlanning.objects.select_related(
        'project_planning', 'project_planning__project',
        'task_definition'
    ).prefetch_related('task_definition__boq_items').all()
    serializer_class = TaskPlanningSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'project_planning', 'project_planning__project',
        'task_definition', 'statut'
    ]
    search_fields = [
        'project_planning__project__code',
        'task_definition__code', 'task_definition__libelle'
    ]
    ordering_fields = ['date_debut_prevue', 'date_fin_prevue', 'statut', 'created_at']
    ordering = ['project_planning', 'ordre']

    @action(detail=False, methods=['get'])
    def delayed(self, request):
        """Retourne les tâches en retard."""
        from datetime import date
        delayed_tasks = self.queryset.filter(
            statut__in=['non_commence', 'en_cours'],
            date_fin_prevue__lt=date.today()
        )
        serializer = self.get_serializer(delayed_tasks, many=True)
        return Response(serializer.data)


class DailyReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des rapports quotidiens.

    Endpoints:
    - GET /api/deployment/daily-reports/ : Liste des rapports
    - POST /api/deployment/daily-reports/ : Créer un rapport
    - GET /api/deployment/daily-reports/{id}/ : Détail
    - PUT /api/deployment/daily-reports/{id}/ : Modifier
    - DELETE /api/deployment/daily-reports/{id}/ : Supprimer
    - GET /api/deployment/daily-reports/by-project/ : Par projet
    - GET /api/deployment/daily-reports/by-date/ : Par date
    """

    queryset = DailyReport.objects.select_related(
        'task_planning', 'task_planning__project_planning__project',
        'task_planning__task_definition',
        'subcontractor', 'referent'
    ).all()
    serializer_class = DailyReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'task_planning', 'task_planning__project_planning__project',
        'date', 'subcontractor', 'referent'
    ]
    search_fields = [
        'task_planning__project_planning__project__code',
        'task_planning__task_definition__libelle',
        'observations'
    ]
    ordering_fields = ['date', 'quantite_jour', 'created_at']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def by_project(self, request):
        """Retourne les rapports pour un projet donné."""
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response(
                {'error': 'Le paramètre "project_id" est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reports = self.queryset.filter(
            task_planning__project_planning__project_id=project_id
        )
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_date(self, request):
        """Retourne les rapports pour une date donnée."""
        date = request.query_params.get('date')
        if not date:
            return Response(
                {'error': 'Le paramètre "date" est requis (format: YYYY-MM-DD)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reports = self.queryset.filter(date=date)
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)


class CartographyPointViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des points cartographiques.

    Endpoints:
    - GET /api/deployment/cartography-points/ : Liste des points
    - POST /api/deployment/cartography-points/ : Créer un point
    - GET /api/deployment/cartography-points/{id}/ : Détail
    - PUT /api/deployment/cartography-points/{id}/ : Modifier
    - DELETE /api/deployment/cartography-points/{id}/ : Supprimer
    - GET /api/deployment/cartography-points/by-project/ : Par projet
    """

    queryset = CartographyPoint.objects.select_related(
        'project', 'project__operator', 'created_by'
    ).all()
    serializer_class = CartographyPointSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'type_infrastructure', 'date']
    search_fields = ['project__code', 'project__nom', 'localite', 'description']
    ordering_fields = ['date', 'localite', 'created_at']
    ordering = ['project', '-date']

    @action(detail=False, methods=['get'])
    def by_project(self, request):
        """Retourne les points cartographiques pour un projet donné."""
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response(
                {'error': 'Le paramètre "project_id" est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        points = self.queryset.filter(project_id=project_id)
        serializer = self.get_serializer(points, many=True)
        return Response(serializer.data)


# ============================================
# VIEWSETS LIVRAISON
# ============================================

class DeliveryPhaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des phases de livraison.

    Endpoints:
    - GET /api/deployment/delivery-phases/ : Liste des phases
    - POST /api/deployment/delivery-phases/ : Créer une phase
    - GET /api/deployment/delivery-phases/{id}/ : Détail
    - PUT /api/deployment/delivery-phases/{id}/ : Modifier
    - DELETE /api/deployment/delivery-phases/{id}/ : Supprimer
    """

    queryset = DeliveryPhase.objects.select_related(
        'project', 'project__operator', 'responsable'
    ).prefetch_related('corrections').all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'phase', 'statut', 'responsable']
    search_fields = ['project__code', 'project__nom', 'observations']
    ordering_fields = ['project', 'date_debut', 'date_fin', 'created_at']
    ordering = ['project', 'date_debut']

    def get_serializer_class(self):
        """Utilise un serializer simplifié pour les listes."""
        if self.action == 'list':
            return DeliveryPhaseListSerializer
        return DeliveryPhaseSerializer


class CorrectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des corrections.

    Endpoints:
    - GET /api/deployment/corrections/ : Liste des corrections
    - POST /api/deployment/corrections/ : Créer une correction
    - GET /api/deployment/corrections/{id}/ : Détail
    - PUT /api/deployment/corrections/{id}/ : Modifier
    - DELETE /api/deployment/corrections/{id}/ : Supprimer
    """

    queryset = Correction.objects.select_related(
        'delivery_phase', 'delivery_phase__project',
        'boq_item', 'task_definition', 'correcteur'
    ).all()
    serializer_class = CorrectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'delivery_phase', 'delivery_phase__project',
        'boq_item', 'statut', 'correcteur', 'date'
    ]
    search_fields = [
        'delivery_phase__project__code',
        'boq_item__code', 'boq_item__libelle',
        'observations'
    ]
    ordering_fields = ['date', 'statut', 'created_at']
    ordering = ['delivery_phase', '-date']
