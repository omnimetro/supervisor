"""
Configuration de l'interface d'administration Django pour deployment.

Ce fichier configure l'affichage des modèles dans l'admin Django :
- OperatorAdmin : Opérateurs télécom
- BOQCategoryAdmin : Catégories de travaux du BOQ
- BOQItemAdmin : Éléments du BOQ avec prix
- TaskDefinitionAdmin : Définitions de tâches AIV
- SubcontractorAdmin : Entreprises sous-traitantes
- TechnicianAdmin : Techniciens AIV
- ProjectAdmin : Chantiers de déploiement
- ProjectPlanningAdmin : Planning prévisionnel travaux
- TaskPlanningAdmin : Planning prévisionnel tâches
- DailyReportAdmin : Rapports quotidiens
- CartographyPointAdmin : Points cartographiques
- DeliveryPhaseAdmin : Phases de livraison
- CorrectionAdmin : Corrections
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum
from .models import (
    Operator, BOQCategory, BOQItem, TaskDefinition,
    Subcontractor, Technician, Project, ProjectPlanning,
    TaskPlanning, DailyReport, CartographyPoint,
    DeliveryPhase, Correction
)


# ============================================
# MODÈLES DE RÉFÉRENCE
# ============================================

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Operator."""

    list_display = (
        'code', 'nom', 'display_logo', 'display_couleur',
        'contact_nom', 'contact_telephone', 'is_active',
        'display_projects_count', 'created_at'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'nom', 'contact_nom', 'contact_email')
    ordering = ('nom',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom', 'logo', 'couleur', 'is_active')
        }),
        ('Contact', {
            'fields': ('contact_nom', 'contact_email', 'contact_telephone')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_logo(self, obj):
        """Affiche le logo de l'opérateur."""
        if obj.logo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: contain;" />',
                obj.logo.url
            )
        return '-'
    display_logo.short_description = 'Logo'

    def display_couleur(self, obj):
        """Affiche la couleur de marque."""
        return format_html(
            '<div style="width: 50px; height: 25px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.couleur
        )
    display_couleur.short_description = 'Couleur'

    def display_projects_count(self, obj):
        """Affiche le nombre de chantiers actifs."""
        count = obj.get_active_projects_count()
        return format_html('<strong>{}</strong>', count)
    display_projects_count.short_description = 'Chantiers actifs'


class BOQItemInline(admin.TabularInline):
    """Inline pour afficher les éléments BOQ dans une catégorie."""
    model = BOQItem
    extra = 0
    fields = ('code', 'libelle', 'unite', 'prix_unitaire', 'is_active')
    show_change_link = True


@admin.register(BOQCategory)
class BOQCategoryAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle BOQCategory."""

    list_display = (
        'code', 'nom', 'display_items_count',
        'is_active', 'created_at'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'nom', 'description')
    ordering = ('nom',)
    readonly_fields = ('created_at',)
    inlines = [BOQItemInline]

    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom', 'is_active')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def display_items_count(self, obj):
        """Affiche le nombre d'éléments dans la catégorie."""
        count = obj.items.count()
        return format_html('<strong>{}</strong>', count)
    display_items_count.short_description = 'Nombre d\'éléments'


@admin.register(BOQItem)
class BOQItemAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle BOQItem."""

    list_display = (
        'code', 'libelle', 'operator', 'category', 'unite',
        'display_prix_unitaire', 'is_active', 'display_tasks_count'
    )
    list_filter = ('operator', 'category', 'unite', 'is_active', 'created_at')
    search_fields = ('code', 'libelle', 'description')
    ordering = ('operator', 'category', 'code')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informations principales', {
            'fields': ('operator', 'category', 'code', 'libelle', 'is_active')
        }),
        ('Détails techniques', {
            'fields': ('unite', 'prix_unitaire', 'description')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_prix_unitaire(self, obj):
        """Affiche le prix unitaire formaté."""
        return format_html('<strong>{:,.0f} FCFA</strong>', obj.prix_unitaire)
    display_prix_unitaire.short_description = 'Prix unitaire'

    def display_tasks_count(self, obj):
        """Affiche le nombre de tâches définies."""
        count = obj.tasks.count()
        return format_html('<strong>{}</strong>', count)
    display_tasks_count.short_description = 'Tâches'


@admin.register(TaskDefinition)
class TaskDefinitionAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle TaskDefinition."""

    list_display = (
        'code', 'libelle', 'display_boq_items_count', 'unite',
        'kpi', 'is_active', 'created_at'
    )
    list_filter = ('unite', 'is_active', 'created_at')
    search_fields = ('code', 'libelle', 'description')
    ordering = ('code',)
    readonly_fields = ('created_at',)
    filter_horizontal = ('boq_items',)

    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'libelle', 'is_active')
        }),
        ('Articles BOQ', {
            'fields': ('boq_items',)
        }),
        ('Détails techniques', {
            'fields': ('unite', 'kpi', 'description')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def display_boq_items_count(self, obj):
        """Affiche le nombre d'articles BOQ associés."""
        count = obj.boq_items.count()
        return format_html('<strong>{}</strong>', count)
    display_boq_items_count.short_description = 'Nb articles BOQ'


@admin.register(Subcontractor)
class SubcontractorAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Subcontractor."""

    list_display = (
        'code', 'nom', 'telephone', 'email',
        'contact_principal_nom', 'is_active',
        'date_debut_collaboration', 'display_projects_count'
    )
    list_filter = ('is_active', 'date_debut_collaboration', 'created_at')
    search_fields = (
        'code', 'nom', 'adresse', 'telephone', 'email',
        'contact_principal_nom', 'numero_registre_commerce'
    )
    ordering = ('nom',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom', 'is_active', 'date_debut_collaboration')
        }),
        ('Coordonnées', {
            'fields': ('adresse', 'telephone', 'email')
        }),
        ('Contact principal', {
            'fields': ('contact_principal_nom', 'contact_principal_telephone')
        }),
        ('Détails', {
            'fields': ('specialites', 'numero_registre_commerce', 'notes')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_projects_count(self, obj):
        """Affiche le nombre de chantiers actifs."""
        count = obj.get_active_projects_count()
        return format_html('<strong>{}</strong>', count)
    display_projects_count.short_description = 'Chantiers actifs'


# ============================================
# RESSOURCES HUMAINES
# ============================================

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Technician."""

    list_display = (
        'matricule', 'display_full_name', 'telephone',
        'specialite', 'niveau_competence', 'display_anciennete',
        'est_chef_chantier', 'is_active'
    )
    list_filter = (
        'specialite', 'niveau_competence', 'est_chef_chantier',
        'is_active', 'date_embauche'
    )
    search_fields = (
        'matricule', 'nom', 'prenoms', 'telephone',
        'email', 'numero_cni'
    )
    ordering = ('matricule',)
    readonly_fields = ('created_at', 'updated_at', 'display_age', 'display_anciennete')

    fieldsets = (
        ('Informations personnelles', {
            'fields': (
                'matricule', 'nom', 'prenoms', 'date_naissance',
                'numero_cni', 'photo', 'is_active'
            )
        }),
        ('Coordonnées', {
            'fields': ('telephone', 'email', 'adresse')
        }),
        ('Compétences professionnelles', {
            'fields': (
                'specialite', 'niveau_competence', 'date_embauche',
                'est_chef_chantier', 'certifications'
            )
        }),
        ('Équipements', {
            'fields': ('equipements_attribues',),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('display_age', 'display_anciennete', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_full_name(self, obj):
        """Affiche le nom complet."""
        return obj.get_full_name()
    display_full_name.short_description = 'Nom complet'

    def display_age(self, obj):
        """Affiche l'âge du technicien."""
        age = obj.get_age()
        return f"{age} ans" if age else '-'
    display_age.short_description = 'Âge'

    def display_anciennete(self, obj):
        """Affiche l'ancienneté."""
        anciennete = obj.get_anciennete()
        return f"{anciennete} an(s)" if anciennete else '-'
    display_anciennete.short_description = 'Ancienneté'


# ============================================
# GESTION DE PROJET
# ============================================

class ProjectPlanningInline(admin.TabularInline):
    """Inline pour le planning des travaux d'un projet."""
    model = ProjectPlanning
    extra = 0
    fields = ('boq_item', 'quantite_prevue', 'delai_jours', 'ordre')
    show_change_link = True


class DeliveryPhaseInline(admin.TabularInline):
    """Inline pour les phases de livraison d'un projet."""
    model = DeliveryPhase
    extra = 0
    fields = ('phase', 'date_debut', 'date_fin', 'statut', 'responsable')
    show_change_link = True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Project."""

    list_display = (
        'code', 'nom', 'operator', 'type_projet',
        'zone_geographique', 'display_superviseur',
        'date_debut', 'date_fin_prevue', 'display_statut',
        'display_progression', 'display_delayed'
    )
    list_filter = (
        'operator', 'type_projet', 'statut', 'date_debut',
        'travaux_ok', 'environnement_ok', 'vt_ok', 'pv_ok'
    )
    search_fields = (
        'code', 'nom', 'zone_geographique',
        'superviseur_operateur', 'description'
    )
    ordering = ('-date_debut',)
    readonly_fields = ('created_at', 'updated_at', 'display_progression', 'display_delayed')
    inlines = [ProjectPlanningInline, DeliveryPhaseInline]

    fieldsets = (
        ('Informations principales', {
            'fields': (
                'code', 'nom', 'operator', 'type_projet',
                'zone_geographique', 'statut'
            )
        }),
        ('Dates', {
            'fields': (
                'date_debut', 'date_fin_prevue', 'date_fin_reelle',
                'date_livraison'
            )
        }),
        ('Équipe de gestion', {
            'fields': (
                'coordonnateur', 'superviseur_aiv', 'superviseur_operateur'
            )
        }),
        ('État d\'avancement', {
            'fields': (
                'travaux_ok', 'environnement_ok', 'vt_ok', 'pv_ok'
            )
        }),
        ('Budget', {
            'fields': ('budget',),
            'classes': ('collapse',)
        }),
        ('Documents', {
            'fields': ('plan_synoptique', 'plan_map', 'bom'),
            'classes': ('collapse',)
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('display_progression', 'display_delayed', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_superviseur(self, obj):
        """Affiche le superviseur AIV."""
        if obj.superviseur_aiv:
            return obj.superviseur_aiv.get_full_name()
        return '-'
    display_superviseur.short_description = 'Superviseur AIV'

    def display_statut(self, obj):
        """Affiche le statut avec couleur."""
        colors = {
            'planifie': '#FFA500',
            'en_cours': '#007BFF',
            'en_livraison': '#28A745',
            'livre': '#6C757D',
            'annule': '#DC3545',
        }
        color = colors.get(obj.statut, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_statut_display()
        )
    display_statut.short_description = 'Statut'

    def display_progression(self, obj):
        """Affiche la progression en pourcentage."""
        progression = obj.get_progression_percentage()
        return format_html('<strong>{}%</strong>', progression)
    display_progression.short_description = 'Progression'

    def display_delayed(self, obj):
        """Affiche si le projet est en retard."""
        if obj.is_delayed():
            return format_html('<span style="color: red;">⚠ EN RETARD</span>')
        return format_html('<span style="color: green;">✓ À jour</span>')
    display_delayed.short_description = 'Retard'


class TaskPlanningInline(admin.TabularInline):
    """Inline pour le planning des tâches d'un travail."""
    model = TaskPlanning
    extra = 0
    fields = (
        'task_definition', 'quantite_prevue', 'date_debut_prevue',
        'date_fin_prevue', 'statut'
    )
    show_change_link = True


@admin.register(ProjectPlanning)
class ProjectPlanningAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle ProjectPlanning."""

    list_display = (
        'display_project', 'display_boq_item', 'valeur_unite', 'quantite_prevue',
        'delai_jours', 'display_montant', 'display_progression', 'ordre'
    )
    list_filter = ('project__operator', 'project__statut', 'boq_item__category')
    search_fields = (
        'project__code', 'project__nom',
        'boq_item__code', 'boq_item__libelle'
    )
    ordering = ('project', 'ordre')
    readonly_fields = ('created_at', 'updated_at', 'display_progression', 'display_montant')
    inlines = [TaskPlanningInline]

    fieldsets = (
        ('Projet et travail', {
            'fields': ('project', 'boq_item', 'ordre')
        }),
        ('Planning', {
            'fields': ('valeur_unite', 'quantite_prevue', 'delai_jours')
        }),
        ('Statistiques', {
            'fields': ('display_progression', 'display_montant'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_project(self, obj):
        """Affiche le projet."""
        return f"{obj.project.code} - {obj.project.nom}"
    display_project.short_description = 'Projet'

    def display_boq_item(self, obj):
        """Affiche l'élément BOQ."""
        return f"{obj.boq_item.code} - {obj.boq_item.libelle}"
    display_boq_item.short_description = 'Travail BOQ'

    def display_montant(self, obj):
        """Affiche le montant total."""
        montant = obj.get_montant_total()
        return format_html('<strong>{:,.0f} FCFA</strong>', montant)
    display_montant.short_description = 'Montant total'

    def display_progression(self, obj):
        """Affiche la progression."""
        progression = obj.get_progression_percentage()
        return format_html('<strong>{}%</strong>', progression)
    display_progression.short_description = 'Progression'


class DailyReportInline(admin.TabularInline):
    """Inline pour les rapports quotidiens d'une tâche."""
    model = DailyReport
    extra = 0
    fields = ('date', 'quantite_jour', 'subcontractor', 'referent')
    show_change_link = True


@admin.register(TaskPlanning)
class TaskPlanningAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle TaskPlanning."""

    list_display = (
        'display_project', 'display_task', 'valeur_unite', 'quantite_prevue',
        'date_debut_prevue', 'date_fin_prevue', 'display_statut',
        'display_progression', 'display_delayed'
    )
    list_filter = (
        'statut', 'project_planning__project__operator',
        'date_debut_prevue', 'date_fin_prevue'
    )
    search_fields = (
        'project_planning__project__code',
        'project_planning__project__nom',
        'task_definition__code', 'task_definition__libelle'
    )
    ordering = ('project_planning', 'ordre')
    readonly_fields = ('created_at', 'updated_at', 'display_progression', 'display_delayed')
    inlines = [DailyReportInline]

    fieldsets = (
        ('Projet et tâche', {
            'fields': ('project_planning', 'task_definition', 'ordre')
        }),
        ('Planning prévisionnel', {
            'fields': (
                'valeur_unite', 'quantite_prevue', 'delai_jours',
                'date_debut_prevue', 'date_fin_prevue'
            )
        }),
        ('Réalisation', {
            'fields': (
                'date_debut_reelle', 'date_fin_reelle', 'statut'
            )
        }),
        ('Statistiques', {
            'fields': ('display_progression', 'display_delayed'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_project(self, obj):
        """Affiche le projet."""
        return obj.project_planning.project.code
    display_project.short_description = 'Projet'

    def display_task(self, obj):
        """Affiche la tâche."""
        return f"{obj.task_definition.code} - {obj.task_definition.libelle}"
    display_task.short_description = 'Tâche'

    def display_statut(self, obj):
        """Affiche le statut avec couleur."""
        colors = {
            'non_commence': '#6C757D',
            'en_cours': '#007BFF',
            'termine': '#28A745',
            'suspendu': '#FFC107',
        }
        color = colors.get(obj.statut, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_statut_display()
        )
    display_statut.short_description = 'Statut'

    def display_progression(self, obj):
        """Affiche la progression."""
        progression = obj.get_progression_percentage()
        return format_html('<strong>{}%</strong>', progression)
    display_progression.short_description = 'Progression'

    def display_delayed(self, obj):
        """Affiche si la tâche est en retard."""
        if obj.is_delayed():
            return format_html('<span style="color: red;">⚠ EN RETARD</span>')
        return format_html('<span style="color: green;">✓ À jour</span>')
    display_delayed.short_description = 'Retard'


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle DailyReport."""

    list_display = (
        'display_project', 'date', 'display_task',
        'valeur_unite', 'quantite_jour', 'display_executor', 'display_referent',
        'display_photos_count'
    )
    list_filter = (
        'date', 'subcontractor',
        'task_planning__project_planning__project__operator'
    )
    search_fields = (
        'task_planning__project_planning__project__code',
        'task_planning__task_definition__libelle',
        'referent__nom', 'referent__prenoms',
        'observations'
    )
    ordering = ('-date',)
    readonly_fields = ('created_at', 'updated_at', 'display_executor', 'display_photos_count')

    fieldsets = (
        ('Tâche et date', {
            'fields': ('task_planning', 'date')
        }),
        ('Quantité et exécution', {
            'fields': ('valeur_unite', 'quantite_jour', 'subcontractor', 'referent')
        }),
        ('Observations', {
            'fields': ('observations',)
        }),
        ('Photos', {
            'fields': ('photos', 'display_photos_count'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('display_executor', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_project(self, obj):
        """Affiche le projet."""
        return obj.task_planning.project_planning.project.code
    display_project.short_description = 'Projet'

    def display_task(self, obj):
        """Affiche la tâche."""
        return obj.task_planning.task_definition.libelle
    display_task.short_description = 'Tâche'

    def display_executor(self, obj):
        """Affiche l'exécutant."""
        name = obj.get_executor_name()
        if obj.is_aiv_work():
            return format_html('<strong style="color: #007BFF;">{}</strong>', name)
        return format_html('<span style="color: #6C757D;">{}</span>', name)
    display_executor.short_description = 'Exécutant'

    def display_referent(self, obj):
        """Affiche le référent."""
        return obj.referent.get_full_name()
    display_referent.short_description = 'Référent'

    def display_photos_count(self, obj):
        """Affiche le nombre de photos."""
        count = obj.get_photos_count()
        return format_html('<strong>{}</strong> photo(s)', count)
    display_photos_count.short_description = 'Photos'


@admin.register(CartographyPoint)
class CartographyPointAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle CartographyPoint."""

    list_display = (
        'display_project', 'date', 'localite',
        'type_infrastructure', 'latitude', 'longitude',
        'display_created_by'
    )
    list_filter = ('type_infrastructure', 'project__operator', 'date')
    search_fields = (
        'project__code', 'project__nom', 'localite',
        'description'
    )
    ordering = ('project', '-date')
    readonly_fields = ('created_at', 'display_map_link')

    fieldsets = (
        ('Projet et localisation', {
            'fields': ('project', 'date', 'localite', 'type_infrastructure')
        }),
        ('Coordonnées GPS', {
            'fields': ('latitude', 'longitude', 'display_map_link')
        }),
        ('Détails', {
            'fields': ('description', 'photo', 'created_by')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def display_project(self, obj):
        """Affiche le projet."""
        return f"{obj.project.code} - {obj.project.nom}"
    display_project.short_description = 'Projet'

    def display_created_by(self, obj):
        """Affiche le créateur."""
        if obj.created_by:
            return obj.created_by.get_full_name()
        return '-'
    display_created_by.short_description = 'Créé par'

    def display_map_link(self, obj):
        """Affiche un lien vers Google Maps."""
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html(
                '<a href="{}" target="_blank">Voir sur Google Maps</a>',
                url
            )
        return '-'
    display_map_link.short_description = 'Carte'


# ============================================
# LIVRAISON
# ============================================

class CorrectionInline(admin.TabularInline):
    """Inline pour les corrections d'une phase de livraison."""
    model = Correction
    extra = 0
    fields = ('date', 'boq_item', 'statut', 'correcteur')
    show_change_link = True


@admin.register(DeliveryPhase)
class DeliveryPhaseAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle DeliveryPhase."""

    list_display = (
        'display_project', 'display_phase', 'date_debut',
        'date_fin', 'display_statut', 'display_responsable',
        'display_corrections_count'
    )
    list_filter = ('phase', 'statut', 'project__operator', 'date_debut')
    search_fields = (
        'project__code', 'project__nom',
        'responsable__nom', 'responsable__prenoms',
        'observations'
    )
    ordering = ('project', 'date_debut')
    readonly_fields = ('created_at', 'updated_at', 'display_corrections_count')
    inlines = [CorrectionInline]

    fieldsets = (
        ('Projet et phase', {
            'fields': ('project', 'phase', 'statut')
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Responsable', {
            'fields': ('responsable',)
        }),
        ('Observations', {
            'fields': ('observations',)
        }),
        ('Documents', {
            'fields': ('documents',),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('display_corrections_count',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_project(self, obj):
        """Affiche le projet."""
        return f"{obj.project.code} - {obj.project.nom}"
    display_project.short_description = 'Projet'

    def display_phase(self, obj):
        """Affiche la phase."""
        return obj.get_phase_display()
    display_phase.short_description = 'Phase'

    def display_statut(self, obj):
        """Affiche le statut avec couleur."""
        colors = {
            'non_commence': '#6C757D',
            'en_cours': '#007BFF',
            'termine': '#28A745',
        }
        color = colors.get(obj.statut, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_statut_display()
        )
    display_statut.short_description = 'Statut'

    def display_responsable(self, obj):
        """Affiche le responsable."""
        if obj.responsable:
            return obj.responsable.get_full_name()
        return '-'
    display_responsable.short_description = 'Responsable'

    def display_corrections_count(self, obj):
        """Affiche le nombre de corrections."""
        count = obj.corrections.count()
        return format_html('<strong>{}</strong>', count)
    display_corrections_count.short_description = 'Corrections'


@admin.register(Correction)
class CorrectionAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Correction."""

    list_display = (
        'display_project', 'date', 'display_phase',
        'display_boq_item', 'display_statut',
        'display_correcteur', 'display_photos_count'
    )
    list_filter = (
        'statut', 'delivery_phase__phase',
        'delivery_phase__project__operator', 'date'
    )
    search_fields = (
        'delivery_phase__project__code',
        'boq_item__code', 'boq_item__libelle',
        'task_definition__libelle', 'observations'
    )
    ordering = ('delivery_phase', '-date')
    readonly_fields = ('created_at', 'display_photos_count')

    fieldsets = (
        ('Phase et date', {
            'fields': ('delivery_phase', 'date')
        }),
        ('Travail et tâche', {
            'fields': ('boq_item', 'task_definition', 'statut')
        }),
        ('Observations', {
            'fields': ('observations',)
        }),
        ('Photos et correcteur', {
            'fields': ('photos', 'correcteur', 'display_photos_count')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def display_project(self, obj):
        """Affiche le projet."""
        return obj.delivery_phase.project.code
    display_project.short_description = 'Projet'

    def display_phase(self, obj):
        """Affiche la phase de livraison."""
        return obj.delivery_phase.get_phase_display()
    display_phase.short_description = 'Phase'

    def display_boq_item(self, obj):
        """Affiche l'élément BOQ."""
        return f"{obj.boq_item.code} - {obj.boq_item.libelle}"
    display_boq_item.short_description = 'Travail BOQ'

    def display_statut(self, obj):
        """Affiche le statut avec couleur."""
        colors = {
            'ok': '#28A745',
            'non_ok': '#DC3545',
        }
        color = colors.get(obj.statut, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_statut_display()
        )
    display_statut.short_description = 'Statut'

    def display_correcteur(self, obj):
        """Affiche le correcteur."""
        if obj.correcteur:
            return obj.correcteur.get_full_name()
        return '-'
    display_correcteur.short_description = 'Correcteur'

    def display_photos_count(self, obj):
        """Affiche le nombre de photos."""
        if isinstance(obj.photos, list):
            count = len(obj.photos)
            return format_html('<strong>{}</strong> photo(s)', count)
        return '0 photo(s)'
    display_photos_count.short_description = 'Photos'
