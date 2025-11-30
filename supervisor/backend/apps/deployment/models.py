"""
Modèles de données pour l'application deployment.

Ce fichier contient tous les modèles pour la gestion des chantiers de déploiement :
- Operator : Opérateurs télécom (Orange, Moov)
- BOQCategory : Catégories de travaux du BOQ
- BOQItem : Éléments du BOQ avec prix unitaires
- TaskDefinition : Tâches AIV pour chaque travail
- Subcontractor : Entreprises sous-traitantes
- Technician : Techniciens AIV (sans compte utilisateur)
- Project : Chantiers de déploiement
- ProjectPlanning : Planning prévisionnel des travaux
- TaskPlanning : Planning prévisionnel des tâches
- DailyReport : Rapports quotidiens d'exécution
- CartographyPoint : Points GPS pour la cartographie
- DeliveryPhase : Phases de livraison
- Correction : Corrections effectuées pendant la livraison
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta


# ============================================
# CHOIX POUR LES CHAMPS
# ============================================

UNITE_CHOICES = [
    ('ml', 'Mètre linéaire'),
    ('u', 'Unité'),
    ('m2', 'Mètre carré'),
    ('m3', 'Mètre cube'),
    ('kg', 'Kilogramme'),
    ('l', 'Litre'),
    ('jour', 'Jour'),
    ('forfait', 'Forfait'),
]

TYPE_PROJET_CHOICES = [
    ('backbone', 'Backbone'),
    ('transport', 'Réseau de transport'),
    ('distribution', 'Réseau de distribution'),
]

STATUT_PROJECT_CHOICES = [
    ('planifie', 'Planifié'),
    ('en_cours', 'En cours'),
    ('en_livraison', 'En livraison'),
    ('livre', 'Livré'),
    ('annule', 'Annulé'),
]

STATUT_TACHE_CHOICES = [
    ('non_commence', 'Non commencé'),
    ('en_cours', 'En cours'),
    ('termine', 'Terminé'),
    ('suspendu', 'Suspendu'),
]

NIVEAU_CHOICES = [
    ('junior', 'Junior'),
    ('confirme', 'Confirmé'),
    ('senior', 'Senior'),
    ('expert', 'Expert'),
]

TYPE_INFRA_CHOICES = [
    ('poteau_beton', 'Poteau béton'),
    ('poteau_metallique', 'Poteau métallique'),
    ('pco', 'PCO - Point de Concentration Optique'),
    ('pec', 'PEC - Point d\'Éclatement de Câble'),
    ('pep', 'PEP - Point d\'Éclatement de Prise'),
    ('jdv', 'JDV - Jarretière de Viabilisation'),
    ('chambre', 'Chambre'),
    ('gc', 'Génie Civil'),
    ('autre', 'Autre'),
]

PHASE_LIVRAISON_CHOICES = [
    ('environnement', 'Environnement et contrôle interne'),
    ('rfc', 'Rédaction RFC (Rapport Fin de Chantier)'),
    ('visite_technique', 'Visite technique opérateur'),
]

STATUT_PHASE_CHOICES = [
    ('non_commence', 'Non commencé'),
    ('en_cours', 'En cours'),
    ('termine', 'Terminé'),
]

STATUT_CORRECTION_CHOICES = [
    ('ok', 'OK'),
    ('non_ok', 'Non OK'),
]


# ============================================
# MODÈLES DE RÉFÉRENCE
# ============================================

class Operator(models.Model):
    """
    Opérateur télécom (Orange, Moov, etc.).

    Représente les opérateurs télécoms pour lesquels AIV réalise des chantiers.
    Chaque opérateur possède son propre BOQ (Bordereau de Quantité).
    """
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code opérateur",
        help_text="Code unique de l'opérateur (ex: ORA, MOV)"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom de l'opérateur"
    )
    logo = models.ImageField(
        upload_to='operators/logos/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )
    couleur = models.CharField(
        max_length=7,
        default='#000000',
        verbose_name="Couleur de marque",
        help_text="Code couleur hexadécimal (ex: #FF5733)"
    )
    contact_nom = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nom du contact"
    )
    contact_email = models.EmailField(
        blank=True,
        verbose_name="Email du contact"
    )
    contact_telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone du contact"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Opérateur"
        verbose_name_plural = "Opérateurs"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_active_projects_count(self):
        """Retourne le nombre de chantiers actifs pour cet opérateur."""
        return self.projects.filter(
            statut__in=['planifie', 'en_cours', 'en_livraison']
        ).count()


class BOQCategory(models.Model):
    """
    Catégorie de travaux du BOQ (Bordereau de Quantité).

    Les travaux sont regroupés par catégories :
    - Travaux GC (Génie Civil)
    - Travaux de réseau
    - Travaux FO (Fibre Optique)
    """
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code catégorie"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom de la catégorie"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Catégorie BOQ"
        verbose_name_plural = "Catégories BOQ"
        ordering = ['nom']

    def __str__(self):
        return f"{self.code} - {self.nom}"


class BOQItem(models.Model):
    """
    Élément du BOQ (Bordereau de Quantité).

    Contient la nomenclature des travaux avec les prix unitaires
    définis par chaque opérateur.
    """
    operator = models.ForeignKey(
        Operator,
        on_delete=models.CASCADE,
        related_name='boq_items',
        verbose_name="Opérateur"
    )
    category = models.ForeignKey(
        BOQCategory,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Catégorie"
    )
    code = models.CharField(
        max_length=50,
        verbose_name="Code du travail"
    )
    libelle = models.CharField(
        max_length=255,
        verbose_name="Libellé du travail"
    )
    unite = models.CharField(
        max_length=20,
        choices=UNITE_CHOICES,
        verbose_name="Unité de mesure"
    )
    prix_unitaire = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Prix unitaire"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Élément BOQ"
        verbose_name_plural = "Éléments BOQ"
        unique_together = ('operator', 'code')
        ordering = ['operator', 'category', 'code']
        indexes = [
            models.Index(fields=['operator', 'category']),
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.code} - {self.libelle}"


class TaskDefinition(models.Model):
    """
    Définition de tâche AIV.

    Une tâche peut être utilisée pour plusieurs travaux du BOQ.
    Chaque tâche a un KPI (quantité par jour) qui définit la productivité attendue.
    """
    boq_items = models.ManyToManyField(
        BOQItem,
        related_name='tasks',
        blank=True,
        verbose_name="Articles BOQ"
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code de la tâche"
    )
    libelle = models.CharField(
        max_length=255,
        verbose_name="Libellé de la tâche"
    )
    unite = models.CharField(
        max_length=20,
        choices=UNITE_CHOICES,
        verbose_name="Unité de mesure"
    )
    kpi = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="KPI (quantité/jour)",
        help_text="Quantité réalisable par jour"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Définition de tâche"
        verbose_name_plural = "Définitions de tâches"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.libelle}"


class Subcontractor(models.Model):
    """
    Entreprise sous-traitante.

    Entreprises externes auxquelles AIV confie une partie des travaux.
    """
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code entreprise",
        help_text="Code unique (ex: ST001)"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom de l'entreprise"
    )
    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse"
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )
    contact_principal_nom = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nom du contact principal"
    )
    contact_principal_telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone du contact"
    )
    specialites = models.TextField(
        blank=True,
        verbose_name="Spécialités",
        help_text="Domaines d'expertise de l'entreprise"
    )
    numero_registre_commerce = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Numéro de registre de commerce"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    date_debut_collaboration = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de début de collaboration"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Entreprise sous-traitante"
        verbose_name_plural = "Entreprises sous-traitantes"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_active_projects_count(self):
        """Retourne le nombre de chantiers actifs pour ce sous-traitant."""
        return self.daily_reports.filter(
            task_planning__project_planning__project__statut__in=['en_cours']
        ).values('task_planning__project_planning__project').distinct().count()


# ============================================
# MODÈLE RESSOURCES HUMAINES
# ============================================

class Specialite(models.Model):
    """
    Spécialité technique.

    Spécialités des techniciens AIV (Génie Civil, Fibre Optique, etc.).
    Permet une gestion dynamique des spécialités plutôt qu'une liste fixe.
    """
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code spécialité",
        help_text="Code unique de la spécialité (ex: GC, FO, SOUD)"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom de la spécialité"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    couleur = models.CharField(
        max_length=7,
        default='#000000',
        verbose_name="Couleur d'identification",
        help_text="Code couleur hexadécimal (ex: #FF5733)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    def get_technicians_count(self):
        """Retourne le nombre de techniciens ayant cette spécialité."""
        return self.technicians.filter(is_active=True).count()


class Technician(models.Model):
    """
    Technicien AIV (sans compte utilisateur).

    Techniciens de terrain d'AI Venture qui n'ont pas de compte
    dans l'application. Seuls les superviseurs ont des comptes.
    """
    matricule = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Matricule",
        help_text="Matricule unique du technicien"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom de famille"
    )
    prenoms = models.CharField(
        max_length=100,
        verbose_name="Prénoms"
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )
    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse"
    )
    specialite = models.ForeignKey(
        Specialite,
        on_delete=models.PROTECT,
        related_name='technicians',
        verbose_name="Spécialité",
        null=True,
        blank=True
    )
    niveau_competence = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default='junior',
        verbose_name="Niveau de compétence"
    )
    date_embauche = models.DateField(
        verbose_name="Date d'embauche"
    )
    date_naissance = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de naissance"
    )
    numero_cni = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Numéro CNI",
        help_text="Carte Nationale d'Identité"
    )
    est_chef_chantier = models.BooleanField(
        default=False,
        verbose_name="Chef de chantier"
    )
    certifications = models.TextField(
        blank=True,
        verbose_name="Certifications",
        help_text="Liste des certifications professionnelles"
    )
    equipements_attribues = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Équipements attribués",
        help_text="Liste des équipements affectés au technicien"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    photo = models.ImageField(
        upload_to='techniciens/',
        blank=True,
        null=True,
        verbose_name="Photo"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Technicien AIV"
        verbose_name_plural = "Techniciens AIV"
        ordering = ['matricule']

    def __str__(self):
        return f"{self.matricule} - {self.get_full_name()}"

    def get_full_name(self):
        """Retourne le nom complet du technicien."""
        return f"{self.prenoms} {self.nom.upper()}"

    def get_age(self):
        """Calcule l'âge du technicien si date de naissance renseignée."""
        if self.date_naissance:
            today = date.today()
            return today.year - self.date_naissance.year - (
                (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
            )
        return None

    def get_anciennete(self):
        """Calcule l'ancienneté en années."""
        today = date.today()
        anciennete = today.year - self.date_embauche.year
        if (today.month, today.day) < (self.date_embauche.month, self.date_embauche.day):
            anciennete -= 1
        return anciennete


# ============================================
# MODÈLES DE GESTION DE PROJET
# ============================================

class Project(models.Model):
    """
    Chantier de déploiement.

    Représente un chantier de déploiement de réseau fibre optique
    (backbone, transport ou distribution).
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code du chantier"
    )
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom/Site du chantier"
    )
    operator = models.ForeignKey(
        Operator,
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name="Opérateur"
    )
    type_projet = models.CharField(
        max_length=20,
        choices=TYPE_PROJET_CHOICES,
        verbose_name="Type de projet"
    )
    zone_geographique = models.CharField(
        max_length=100,
        verbose_name="Zone géographique"
    )
    date_debut = models.DateField(
        verbose_name="Date de début"
    )
    date_fin_prevue = models.DateField(
        verbose_name="Date de fin prévue"
    )
    date_fin_reelle = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin réelle"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_PROJECT_CHOICES,
        default='planifie',
        verbose_name="Statut"
    )
    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Budget"
    )
    superviseur_aiv = models.ForeignKey(
        'users.Profile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='supervised_projects',
        verbose_name="Superviseur AIV"
    )
    superviseur_operateur = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Superviseur opérateur"
    )
    travaux_ok = models.BooleanField(
        default=False,
        verbose_name="Travaux OK"
    )
    environnement_ok = models.BooleanField(
        default=False,
        verbose_name="Environnement OK"
    )
    vt_ok = models.BooleanField(
        default=False,
        verbose_name="Visite Technique OK"
    )
    pv_ok = models.BooleanField(
        default=False,
        verbose_name="Procès-Verbal OK"
    )
    date_livraison = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de livraison"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Chantier"
        verbose_name_plural = "Chantiers"
        ordering = ['-date_debut']
        indexes = [
            models.Index(fields=['operator', 'statut']),
            models.Index(fields=['date_debut']),
        ]

    def __str__(self):
        return f"{self.code} - {self.nom}"

    def get_progression_percentage(self):
        """Calcule le pourcentage d'avancement du chantier."""
        total_tasks = self.get_total_tasks()
        if total_tasks == 0:
            return 0
        completed_tasks = self.get_completed_tasks()
        return round((completed_tasks / total_tasks) * 100, 2)

    def get_total_tasks(self):
        """Retourne le nombre total de tâches planifiées."""
        return TaskPlanning.objects.filter(
            project_planning__project=self
        ).count()

    def get_completed_tasks(self):
        """Retourne le nombre de tâches terminées."""
        return TaskPlanning.objects.filter(
            project_planning__project=self,
            statut='termine'
        ).count()

    def is_delayed(self):
        """Vérifie si le projet est en retard."""
        if self.statut in ['livre', 'annule']:
            return False
        today = date.today()
        return today > self.date_fin_prevue


class TypeDocument(models.Model):
    """
    Type de document pour les projets.

    Types de documents pouvant être associés aux projets
    (BOM, MAP, SYNOPTIQUE, AUTRES).
    """
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code du type",
        help_text="Code unique (ex: BOM, MAP, SYNOPTIQUE, AUTRES)"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom du type de document"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Type de document"
        verbose_name_plural = "Types de documents"
        ordering = ['code']

    def __str__(self):
        return self.nom


class ProjectDocument(models.Model):
    """
    Document associé à un projet.

    Documents uploadés pour un projet (BOM, MAP, SYNOPTIQUE, etc.).
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="Projet"
    )
    type_document = models.ForeignKey(
        TypeDocument,
        on_delete=models.PROTECT,
        related_name='documents',
        verbose_name="Type de document"
    )
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du document"
    )
    fichier = models.FileField(
        upload_to='projects/documents/%Y/%m/',
        verbose_name="Fichier"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    version = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Version",
        help_text="Version du document (ex: v1.0, v2.1)"
    )
    date_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'upload"
    )
    uploaded_by_profil = models.ForeignKey(
        'users.Profile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name="Uploadé par"
    )
    taille_fichier = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Taille du fichier (octets)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Document de projet"
        verbose_name_plural = "Documents de projets"
        ordering = ['-date_upload']

    def __str__(self):
        return f"{self.nom} - {self.project.code}"

    def save(self, *args, **kwargs):
        """Sauvegarde la taille du fichier automatiquement."""
        if self.fichier:
            self.taille_fichier = self.fichier.size
        super().save(*args, **kwargs)


class ProjectPlanning(models.Model):
    """
    Planning prévisionnel des travaux.

    Planning prévisionnel associant les travaux du BOQ à un chantier
    avec les quantités prévues et délais.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='work_planning',
        verbose_name="Chantier"
    )
    boq_item = models.ForeignKey(
        BOQItem,
        on_delete=models.PROTECT,
        related_name='project_plannings',
        verbose_name="Travail BOQ"
    )
    valeur_unite = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Valeur de l'unité",
        help_text="Valeur numérique de l'unité (ex: 1 pour unité simple, 100 pour centaine)"
    )
    quantite_prevue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Quantité prévue"
    )
    delai_jours = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Délai (jours)",
        help_text="Délai de réalisation en nombre de jours"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'exécution"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Planning prévisionnel travaux"
        verbose_name_plural = "Plannings prévisionnels travaux"
        unique_together = ('project', 'boq_item')
        ordering = ['project', 'ordre']

    def __str__(self):
        return f"{self.project.code} - {self.boq_item.libelle}"

    def get_quantite_realisee(self):
        """Retourne la quantité réalisée via les rapports quotidiens."""
        from django.db.models import Sum
        result = DailyReport.objects.filter(
            task_planning__project_planning=self
        ).aggregate(total=Sum('quantite_jour'))
        return result['total'] or Decimal('0.00')

    def get_progression_percentage(self):
        """Calcule le pourcentage de progression."""
        quantite_realisee = self.get_quantite_realisee()
        if self.quantite_prevue == 0:
            return 0
        return round((quantite_realisee / self.quantite_prevue) * 100, 2)

    def get_montant_total(self):
        """Calcule le montant total prévu (quantité × prix unitaire)."""
        return self.quantite_prevue * self.boq_item.prix_unitaire


class TaskPlanning(models.Model):
    """
    Planning prévisionnel des tâches.

    Planning détaillé des tâches à effectuer pour chaque travail
    d'un chantier.
    """
    project_planning = models.ForeignKey(
        ProjectPlanning,
        on_delete=models.CASCADE,
        related_name='task_planning',
        verbose_name="Planning travaux"
    )
    task_definition = models.ForeignKey(
        TaskDefinition,
        on_delete=models.PROTECT,
        related_name='task_plannings',
        verbose_name="Tâche"
    )
    valeur_unite = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Valeur de l'unité",
        help_text="Valeur numérique de l'unité (ex: 1 pour unité simple, 100 pour centaine)"
    )
    quantite_prevue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Quantité prévue"
    )
    delai_jours = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Délai (jours)"
    )
    date_debut_prevue = models.DateField(
        verbose_name="Date de début prévue"
    )
    date_fin_prevue = models.DateField(
        verbose_name="Date de fin prévue"
    )
    date_debut_reelle = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de début réelle"
    )
    date_fin_reelle = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin réelle"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_TACHE_CHOICES,
        default='non_commence',
        verbose_name="Statut"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'exécution"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Planning prévisionnel tâche"
        verbose_name_plural = "Plannings prévisionnels tâches"
        ordering = ['project_planning', 'ordre']

    def __str__(self):
        return f"{self.project_planning.project.code} - {self.task_definition.libelle}"

    def get_quantite_realisee(self):
        """Retourne la quantité réalisée via les rapports quotidiens."""
        from django.db.models import Sum
        result = self.daily_reports.aggregate(total=Sum('quantite_jour'))
        return result['total'] or Decimal('0.00')

    def get_progression_percentage(self):
        """Calcule le pourcentage de progression."""
        quantite_realisee = self.get_quantite_realisee()
        if self.quantite_prevue == 0:
            return 0
        return round((quantite_realisee / self.quantite_prevue) * 100, 2)

    def is_delayed(self):
        """Vérifie si la tâche est en retard."""
        if self.statut == 'termine':
            return False
        today = date.today()
        return today > self.date_fin_prevue


class DailyReport(models.Model):
    """
    Rapport quotidien d'exécution.

    Reporting quotidien des tâches effectuées sur le chantier.
    Le superviseur AIV crée un rapport par jour et par tâche,
    en indiquant si le travail a été fait par AIV (subcontractor=NULL)
    ou par un sous-traitant (subcontractor=FK).
    """
    task_planning = models.ForeignKey(
        TaskPlanning,
        on_delete=models.CASCADE,
        related_name='daily_reports',
        verbose_name="Tâche planifiée"
    )
    date = models.DateField(
        verbose_name="Date"
    )
    valeur_unite = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Valeur de l'unité",
        help_text="Valeur numérique de l'unité (ex: 1 pour unité simple, 100 pour centaine)"
    )
    quantite_jour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Quantité du jour"
    )
    subcontractor = models.ForeignKey(
        Subcontractor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='daily_reports',
        verbose_name="Sous-traitant",
        help_text="Laisser vide si travaux effectués par techniciens AIV"
    )
    referent = models.ForeignKey(
        'users.Profile',
        on_delete=models.PROTECT,
        related_name='authored_reports',
        verbose_name="Référent",
        help_text="Superviseur AIV qui crée le rapport"
    )
    observations = models.TextField(
        blank=True,
        verbose_name="Observations"
    )
    photos = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Photos NoteCam",
        help_text="Liste des URLs des photos NoteCam"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Rapport quotidien"
        verbose_name_plural = "Rapports quotidiens"
        unique_together = ('task_planning', 'date', 'subcontractor')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['subcontractor']),
        ]

    def __str__(self):
        return f"{self.task_planning.project_planning.project.code} - {self.date}"

    def is_aiv_work(self):
        """Retourne True si le travail a été effectué par AIV."""
        return self.subcontractor is None

    def get_executor_name(self):
        """Retourne le nom de l'exécutant (AIV ou nom du sous-traitant)."""
        if self.is_aiv_work():
            return "AI Venture"
        return self.subcontractor.nom

    def get_photos_count(self):
        """Retourne le nombre de photos."""
        if isinstance(self.photos, list):
            return len(self.photos)
        return 0


class CartographyPoint(models.Model):
    """
    Point cartographique.

    Points GPS pour la cartographie des infrastructures installées
    sur le chantier (poteaux, équipements, chambres, etc.).
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='cartography_points',
        verbose_name="Chantier"
    )
    date = models.DateField(
        verbose_name="Date"
    )
    localite = models.CharField(
        max_length=100,
        verbose_name="Localité"
    )
    type_infrastructure = models.CharField(
        max_length=50,
        choices=TYPE_INFRA_CHOICES,
        verbose_name="Type d'infrastructure"
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name="Longitude"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    photo = models.ImageField(
        upload_to='cartography/',
        blank=True,
        null=True,
        verbose_name="Photo"
    )
    created_by = models.ForeignKey(
        'users.Profile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_cartography_points',
        verbose_name="Créé par"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Point cartographique"
        verbose_name_plural = "Points cartographiques"
        ordering = ['project', '-date']
        indexes = [
            models.Index(fields=['project', 'type_infrastructure']),
            models.Index(fields=['latitude', 'longitude']),
        ]

    def __str__(self):
        return f"{self.project.code} - {self.get_type_infrastructure_display()} - {self.localite}"


# ============================================
# MODÈLES DE LIVRAISON
# ============================================

class DeliveryPhase(models.Model):
    """
    Phase de livraison.

    Suivi des phases de livraison d'un chantier :
    - Environnement et contrôle interne
    - Rédaction RFC (Rapport Fin de Chantier)
    - Visite technique opérateur
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='delivery_phases',
        verbose_name="Chantier"
    )
    phase = models.CharField(
        max_length=30,
        choices=PHASE_LIVRAISON_CHOICES,
        verbose_name="Phase"
    )
    date_debut = models.DateField(
        verbose_name="Date de début"
    )
    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_PHASE_CHOICES,
        default='en_cours',
        verbose_name="Statut"
    )
    responsable = models.ForeignKey(
        'users.Profile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_delivery_phases',
        verbose_name="Responsable"
    )
    observations = models.TextField(
        blank=True,
        verbose_name="Observations"
    )
    documents = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Documents",
        help_text="URLs des documents (RFC PowerPoint, etc.)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Phase de livraison"
        verbose_name_plural = "Phases de livraison"
        unique_together = ('project', 'phase')
        ordering = ['project', 'date_debut']

    def __str__(self):
        return f"{self.project.code} - {self.get_phase_display()}"


class Correction(models.Model):
    """
    Correction.

    Corrections effectuées pendant les phases de livraison
    (environnement, contrôle interne, visite technique).
    """
    delivery_phase = models.ForeignKey(
        DeliveryPhase,
        on_delete=models.CASCADE,
        related_name='corrections',
        verbose_name="Phase de livraison"
    )
    date = models.DateField(
        verbose_name="Date"
    )
    boq_item = models.ForeignKey(
        BOQItem,
        on_delete=models.PROTECT,
        related_name='corrections',
        verbose_name="Travail BOQ"
    )
    task_definition = models.ForeignKey(
        TaskDefinition,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='corrections',
        verbose_name="Tâche"
    )
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CORRECTION_CHOICES,
        verbose_name="Statut"
    )
    observations = models.TextField(
        verbose_name="Observations"
    )
    photos = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Photos NoteCam",
        help_text="URLs des photos NoteCam"
    )
    correcteur = models.ForeignKey(
        'users.Profile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='corrections',
        verbose_name="Correcteur"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Correction"
        verbose_name_plural = "Corrections"
        ordering = ['delivery_phase', '-date']

    def __str__(self):
        return f"{self.delivery_phase.project.code} - {self.date} - {self.get_statut_display()}"
