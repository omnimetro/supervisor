"""
Serializers DRF pour l'application deployment.

Ce fichier contient tous les serializers pour l'API REST :
- OperatorSerializer : Opérateurs télécom
- BOQCategorySerializer : Catégories de travaux du BOQ
- BOQItemSerializer : Éléments du BOQ avec prix
- TaskDefinitionSerializer : Définitions de tâches AIV
- SubcontractorSerializer : Entreprises sous-traitantes
- SpecialiteSerializer : Spécialités techniques
- TechnicianSerializer : Techniciens AIV
- ProjectSerializer : Chantiers de déploiement
- ProjectPlanningSerializer : Planning prévisionnel travaux
- TaskPlanningSerializer : Planning prévisionnel tâches
- DailyReportSerializer : Rapports quotidiens
- CartographyPointSerializer : Points cartographiques
- DeliveryPhaseSerializer : Phases de livraison
- CorrectionSerializer : Corrections
- TypeDocumentSerializer : Types de documents
- ProjectDocumentSerializer : Documents de projet
"""

from rest_framework import serializers
from .models import (
    Operator, BOQCategory, BOQItem, TaskDefinition,
    Subcontractor, Specialite, Technician, Project, ProjectPlanning,
    TaskPlanning, DailyReport, CartographyPoint,
    DeliveryPhase, Correction, TypeDocument, ProjectDocument
)


# ============================================
# SERIALIZERS DE RÉFÉRENCE
# ============================================

class OperatorSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Operator."""

    active_projects_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Operator
        fields = [
            'id', 'code', 'nom', 'logo', 'couleur',
            'contact_nom', 'contact_email', 'contact_telephone',
            'is_active', 'active_projects_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_active_projects_count(self, obj):
        """Retourne le nombre de chantiers actifs."""
        return obj.get_active_projects_count()


class BOQCategorySerializer(serializers.ModelSerializer):
    """Serializer pour le modèle BOQCategory."""

    items_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BOQCategory
        fields = [
            'id', 'code', 'nom', 'description',
            'is_active', 'items_count', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_items_count(self, obj):
        """Retourne le nombre d'éléments dans la catégorie."""
        return obj.items.count()


class TaskDefinitionSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle TaskDefinition."""

    boq_items_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TaskDefinition
        fields = [
            'id', 'boq_items', 'boq_items_count',
            'code', 'libelle', 'unite', 'kpi', 'description',
            'is_active', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_boq_items_count(self, obj):
        """Retourne le nombre d'articles BOQ associés."""
        return obj.boq_items.count()


class BOQItemSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle BOQItem."""

    operator_nom = serializers.CharField(source='operator.nom', read_only=True)
    category_nom = serializers.CharField(source='category.nom', read_only=True)
    tasks = TaskDefinitionSerializer(many=True, read_only=True)
    tasks_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BOQItem
        fields = [
            'id', 'operator', 'operator_nom', 'category', 'category_nom',
            'code', 'libelle', 'unite', 'prix_unitaire', 'description',
            'is_active', 'tasks', 'tasks_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_tasks_count(self, obj):
        """Retourne le nombre de tâches définies."""
        return obj.tasks.count()


class BOQItemListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour les listes de BOQItem (sans tasks nested)."""

    operator_nom = serializers.CharField(source='operator.nom', read_only=True)
    category_nom = serializers.CharField(source='category.nom', read_only=True)
    tasks_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BOQItem
        fields = [
            'id', 'operator', 'operator_nom', 'category', 'category_nom',
            'code', 'libelle', 'unite', 'prix_unitaire',
            'is_active', 'tasks_count'
        ]

    def get_tasks_count(self, obj):
        """Retourne le nombre de tâches définies."""
        return obj.tasks.count()


class SubcontractorSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Subcontractor."""

    active_projects_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subcontractor
        fields = [
            'id', 'code', 'nom', 'adresse', 'telephone', 'email',
            'contact_principal_nom', 'contact_principal_telephone',
            'specialites', 'numero_registre_commerce', 'is_active',
            'date_debut_collaboration', 'notes', 'active_projects_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_active_projects_count(self, obj):
        """Retourne le nombre de chantiers actifs."""
        return obj.get_active_projects_count()


# ============================================
# SERIALIZERS RESSOURCES HUMAINES
# ============================================

class SpecialiteSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Specialite."""

    technicians_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Specialite
        fields = [
            'id', 'code', 'nom', 'description', 'couleur',
            'is_active', 'ordre', 'technicians_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_technicians_count(self, obj):
        """Retourne le nombre de techniciens."""
        return obj.get_technicians_count()


class TechnicianSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Technician."""

    specialite_nom = serializers.CharField(source='specialite.nom', read_only=True)
    specialite_couleur = serializers.CharField(source='specialite.couleur', read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)
    anciennete = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Technician
        fields = [
            'id', 'matricule', 'nom', 'prenoms', 'full_name',
            'telephone', 'email', 'adresse',
            'specialite', 'specialite_nom', 'specialite_couleur',
            'niveau_competence', 'date_embauche', 'date_naissance',
            'numero_cni', 'est_chef_chantier', 'certifications',
            'equipements_attribues', 'is_active', 'notes', 'photo',
            'age', 'anciennete',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_full_name(self, obj):
        """Retourne le nom complet."""
        return obj.get_full_name()

    def get_age(self, obj):
        """Retourne l'âge."""
        return obj.get_age()

    def get_anciennete(self, obj):
        """Retourne l'ancienneté."""
        return obj.get_anciennete()


# ============================================
# SERIALIZERS GESTION DE PROJET
# ============================================

class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour les listes de projets."""

    operator_nom = serializers.CharField(source='operator.nom', read_only=True)
    superviseur_aiv_nom = serializers.SerializerMethodField(read_only=True)
    progression_percentage = serializers.SerializerMethodField(read_only=True)
    is_delayed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'code', 'nom', 'operator', 'operator_nom',
            'type_projet', 'zone_geographique', 'date_debut',
            'date_fin_prevue', 'date_fin_reelle', 'statut',
            'superviseur_aiv', 'superviseur_aiv_nom',
            'progression_percentage', 'is_delayed'
        ]

    def get_superviseur_aiv_nom(self, obj):
        """Retourne le nom du superviseur AIV."""
        if obj.superviseur_aiv:
            return obj.superviseur_aiv.get_full_name()
        return None

    def get_progression_percentage(self, obj):
        """Retourne le pourcentage de progression."""
        return obj.get_progression_percentage()

    def get_is_delayed(self, obj):
        """Retourne si le projet est en retard."""
        return obj.is_delayed()


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour le modèle Project."""

    operator_nom = serializers.CharField(source='operator.nom', read_only=True)
    superviseur_aiv_nom = serializers.SerializerMethodField(read_only=True)
    progression_percentage = serializers.SerializerMethodField(read_only=True)
    total_tasks = serializers.SerializerMethodField(read_only=True)
    completed_tasks = serializers.SerializerMethodField(read_only=True)
    is_delayed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'code', 'nom', 'operator', 'operator_nom',
            'type_projet', 'zone_geographique', 'date_debut',
            'date_fin_prevue', 'date_fin_reelle', 'statut', 'budget',
            'superviseur_aiv', 'superviseur_aiv_nom',
            'superviseur_operateur', 'travaux_ok', 'environnement_ok',
            'vt_ok', 'pv_ok', 'date_livraison', 'description',
            'progression_percentage', 'total_tasks', 'completed_tasks',
            'is_delayed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_superviseur_aiv_nom(self, obj):
        """Retourne le nom du superviseur AIV."""
        if obj.superviseur_aiv:
            return obj.superviseur_aiv.get_full_name()
        return None

    def get_progression_percentage(self, obj):
        """Retourne le pourcentage de progression."""
        return obj.get_progression_percentage()

    def get_total_tasks(self, obj):
        """Retourne le nombre total de tâches."""
        return obj.get_total_tasks()

    def get_completed_tasks(self, obj):
        """Retourne le nombre de tâches complétées."""
        return obj.get_completed_tasks()

    def get_is_delayed(self, obj):
        """Retourne si le projet est en retard."""
        return obj.is_delayed()


class ProjectPlanningSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle ProjectPlanning."""

    project_code = serializers.CharField(source='project.code', read_only=True)
    project_nom = serializers.CharField(source='project.nom', read_only=True)
    boq_item_code = serializers.CharField(source='boq_item.code', read_only=True)
    boq_item_libelle = serializers.CharField(source='boq_item.libelle', read_only=True)
    boq_item_unite = serializers.CharField(source='boq_item.unite', read_only=True)
    quantite_realisee = serializers.SerializerMethodField(read_only=True)
    progression_percentage = serializers.SerializerMethodField(read_only=True)
    montant_total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProjectPlanning
        fields = [
            'id', 'project', 'project_code', 'project_nom',
            'boq_item', 'boq_item_code', 'boq_item_libelle', 'boq_item_unite',
            'valeur_unite', 'quantite_prevue', 'delai_jours', 'ordre',
            'quantite_realisee', 'progression_percentage', 'montant_total',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_quantite_realisee(self, obj):
        """Retourne la quantité réalisée."""
        return float(obj.get_quantite_realisee())

    def get_progression_percentage(self, obj):
        """Retourne le pourcentage de progression."""
        return obj.get_progression_percentage()

    def get_montant_total(self, obj):
        """Retourne le montant total."""
        return float(obj.get_montant_total())


class TaskPlanningSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle TaskPlanning."""

    project_code = serializers.CharField(
        source='project_planning.project.code', read_only=True
    )
    task_code = serializers.CharField(source='task_definition.code', read_only=True)
    task_libelle = serializers.CharField(source='task_definition.libelle', read_only=True)
    task_unite = serializers.CharField(source='task_definition.unite', read_only=True)
    quantite_realisee = serializers.SerializerMethodField(read_only=True)
    progression_percentage = serializers.SerializerMethodField(read_only=True)
    is_delayed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TaskPlanning
        fields = [
            'id', 'project_planning', 'project_code',
            'task_definition', 'task_code', 'task_libelle', 'task_unite',
            'valeur_unite', 'quantite_prevue', 'delai_jours',
            'date_debut_prevue', 'date_fin_prevue',
            'date_debut_reelle', 'date_fin_reelle',
            'statut', 'ordre',
            'quantite_realisee', 'progression_percentage', 'is_delayed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_quantite_realisee(self, obj):
        """Retourne la quantité réalisée."""
        return float(obj.get_quantite_realisee())

    def get_progression_percentage(self, obj):
        """Retourne le pourcentage de progression."""
        return obj.get_progression_percentage()

    def get_is_delayed(self, obj):
        """Retourne si la tâche est en retard."""
        return obj.is_delayed()


class DailyReportSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle DailyReport."""

    project_code = serializers.CharField(
        source='task_planning.project_planning.project.code', read_only=True
    )
    task_libelle = serializers.CharField(
        source='task_planning.task_definition.libelle', read_only=True
    )
    subcontractor_nom = serializers.CharField(
        source='subcontractor.nom', read_only=True, allow_null=True
    )
    referent_nom = serializers.SerializerMethodField(read_only=True)
    executor_name = serializers.SerializerMethodField(read_only=True)
    is_aiv_work = serializers.SerializerMethodField(read_only=True)
    photos_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DailyReport
        fields = [
            'id', 'task_planning', 'project_code', 'task_libelle',
            'date', 'valeur_unite', 'quantite_jour',
            'subcontractor', 'subcontractor_nom',
            'referent', 'referent_nom',
            'observations', 'photos',
            'executor_name', 'is_aiv_work', 'photos_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_referent_nom(self, obj):
        """Retourne le nom du référent."""
        if obj.referent:
            return obj.referent.get_full_name()
        return None

    def get_executor_name(self, obj):
        """Retourne le nom de l'exécutant."""
        return obj.get_executor_name()

    def get_is_aiv_work(self, obj):
        """Retourne si c'est un travail AIV."""
        return obj.is_aiv_work()

    def get_photos_count(self, obj):
        """Retourne le nombre de photos."""
        return obj.get_photos_count()


class CartographyPointSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle CartographyPoint."""

    project_code = serializers.CharField(source='project.code', read_only=True)
    project_nom = serializers.CharField(source='project.nom', read_only=True)
    created_by_nom = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartographyPoint
        fields = [
            'id', 'project', 'project_code', 'project_nom',
            'date', 'localite', 'type_infrastructure',
            'latitude', 'longitude', 'description', 'photo',
            'created_by', 'created_by_nom',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def get_created_by_nom(self, obj):
        """Retourne le nom du créateur."""
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None


# ============================================
# SERIALIZERS LIVRAISON
# ============================================

class CorrectionSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Correction."""

    project_code = serializers.CharField(
        source='delivery_phase.project.code', read_only=True
    )
    phase_libelle = serializers.CharField(
        source='delivery_phase.get_phase_display', read_only=True
    )
    boq_item_code = serializers.CharField(source='boq_item.code', read_only=True)
    boq_item_libelle = serializers.CharField(source='boq_item.libelle', read_only=True)
    correcteur_nom = serializers.SerializerMethodField(read_only=True)
    photos_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Correction
        fields = [
            'id', 'delivery_phase', 'project_code', 'phase_libelle',
            'date', 'boq_item', 'boq_item_code', 'boq_item_libelle',
            'task_definition', 'statut', 'observations', 'photos',
            'correcteur', 'correcteur_nom', 'photos_count',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def get_correcteur_nom(self, obj):
        """Retourne le nom du correcteur."""
        if obj.correcteur:
            return obj.correcteur.get_full_name()
        return None

    def get_photos_count(self, obj):
        """Retourne le nombre de photos."""
        if isinstance(obj.photos, list):
            return len(obj.photos)
        return 0


class DeliveryPhaseSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle DeliveryPhase."""

    project_code = serializers.CharField(source='project.code', read_only=True)
    project_nom = serializers.CharField(source='project.nom', read_only=True)
    phase_libelle = serializers.CharField(source='get_phase_display', read_only=True)
    responsable_nom = serializers.SerializerMethodField(read_only=True)
    corrections = CorrectionSerializer(many=True, read_only=True)
    corrections_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DeliveryPhase
        fields = [
            'id', 'project', 'project_code', 'project_nom',
            'phase', 'phase_libelle', 'date_debut', 'date_fin',
            'statut', 'responsable', 'responsable_nom',
            'observations', 'documents',
            'corrections', 'corrections_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_responsable_nom(self, obj):
        """Retourne le nom du responsable."""
        if obj.responsable:
            return obj.responsable.get_full_name()
        return None

    def get_corrections_count(self, obj):
        """Retourne le nombre de corrections."""
        return obj.corrections.count()


class DeliveryPhaseListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour les listes de phases de livraison."""

    project_code = serializers.CharField(source='project.code', read_only=True)
    project_nom = serializers.CharField(source='project.nom', read_only=True)
    phase_libelle = serializers.CharField(source='get_phase_display', read_only=True)
    responsable_nom = serializers.SerializerMethodField(read_only=True)
    corrections_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DeliveryPhase
        fields = [
            'id', 'project', 'project_code', 'project_nom',
            'phase', 'phase_libelle', 'date_debut', 'date_fin',
            'statut', 'responsable', 'responsable_nom',
            'corrections_count'
        ]

    def get_responsable_nom(self, obj):
        """Retourne le nom du responsable."""
        if obj.responsable:
            return obj.responsable.get_full_name()
        return None

    def get_corrections_count(self, obj):
        """Retourne le nombre de corrections."""
        return obj.corrections.count()


# ============================================
# SERIALIZERS GESTION DOCUMENTAIRE
# ============================================

class TypeDocumentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle TypeDocument."""

    documents_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TypeDocument
        fields = [
            'id', 'code', 'nom', 'description', 'is_active',
            'documents_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_documents_count(self, obj):
        """Retourne le nombre de documents associés."""
        return obj.documents.count()


class ProjectDocumentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle ProjectDocument."""

    project_code = serializers.CharField(source='project.code', read_only=True)
    project_nom = serializers.CharField(source='project.nom', read_only=True)
    type_document_code = serializers.CharField(source='type_document.code', read_only=True)
    type_document_nom = serializers.CharField(source='type_document.nom', read_only=True)
    uploaded_by_profil_nom = serializers.SerializerMethodField(read_only=True)
    taille_fichier_formatted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProjectDocument
        fields = [
            'id', 'project', 'project_code', 'project_nom',
            'type_document', 'type_document_code', 'type_document_nom',
            'nom', 'fichier', 'description', 'version',
            'date_upload', 'uploaded_by_profil', 'uploaded_by_profil_nom',
            'taille_fichier', 'taille_fichier_formatted',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'date_upload', 'taille_fichier']

    def get_uploaded_by_profil_nom(self, obj):
        """Retourne le nom de l'utilisateur qui a uploadé le document."""
        if obj.uploaded_by_profil:
            return obj.uploaded_by_profil.get_full_name()
        return None

    def get_taille_fichier_formatted(self, obj):
        """Retourne la taille du fichier formatée (ex: 2.5 MB)."""
        if obj.taille_fichier:
            size = obj.taille_fichier
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size / (1024 * 1024):.1f} MB"
            else:
                return f"{size / (1024 * 1024 * 1024):.1f} GB"
        return None


class ProjectDocumentListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour les listes de documents projet."""

    project_code = serializers.CharField(source='project.code', read_only=True)
    type_document_nom = serializers.CharField(source='type_document.nom', read_only=True)
    uploaded_by_profil_nom = serializers.SerializerMethodField(read_only=True)
    taille_fichier_formatted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProjectDocument
        fields = [
            'id', 'project', 'project_code',
            'type_document', 'type_document_nom',
            'nom', 'fichier', 'version', 'date_upload',
            'uploaded_by_profil', 'uploaded_by_profil_nom',
            'taille_fichier_formatted'
        ]

    def get_uploaded_by_profil_nom(self, obj):
        """Retourne le nom de l'utilisateur qui a uploadé le document."""
        if obj.uploaded_by_profil:
            return obj.uploaded_by_profil.get_full_name()
        return None

    def get_taille_fichier_formatted(self, obj):
        """Retourne la taille du fichier formatée (ex: 2.5 MB)."""
        if obj.taille_fichier:
            size = obj.taille_fichier
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size / (1024 * 1024):.1f} MB"
            else:
                return f"{size / (1024 * 1024 * 1024):.1f} GB"
        return None
