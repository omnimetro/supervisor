"""
Modèles pour la gestion des utilisateurs - SUPERVISOR V2.0

Ce module définit les modèles Profile, Module, Permission et Role
pour la gestion des utilisateurs et permissions de l'application.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Module(models.Model):
    """
    Modèle représentant un module de l'application.

    Les modules regroupent les permissions par fonctionnalité
    (ex: Déploiement, B2B, Stocks, etc.)
    """

    code = models.CharField(
        verbose_name=_('Code'),
        max_length=50,
        unique=True,
        help_text=_('Code unique du module (ex: deployment, b2b, inventory)')
    )
    nom = models.CharField(
        verbose_name=_('Nom'),
        max_length=100,
        help_text=_('Nom du module')
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        help_text=_('Description détaillée du module')
    )
    ordre = models.IntegerField(
        verbose_name=_('Ordre d\'affichage'),
        default=0,
        help_text=_('Ordre d\'affichage du module dans l\'interface')
    )

    class Meta:
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')
        ordering = ['ordre', 'nom']
        db_table = 'modules'

    def __str__(self):
        return self.nom


class Permission(models.Model):
    """
    Modèle représentant une permission granulaire.

    Les permissions définissent les actions autorisées sur les ressources
    (ex: chantier.create, chantier.view, chantier.edit, chantier.delete)
    """

    code = models.CharField(
        verbose_name=_('Code'),
        max_length=100,
        unique=True,
        help_text=_('Code unique de la permission (ex: chantier.create, b2b.view)')
    )
    nom = models.CharField(
        verbose_name=_('Nom'),
        max_length=100,
        help_text=_('Nom de la permission')
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        help_text=_('Description détaillée de la permission')
    )
    module = models.ForeignKey(
        Module,
        verbose_name=_('Module'),
        on_delete=models.CASCADE,
        related_name='permissions',
        help_text=_('Module auquel appartient cette permission')
    )
    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
        help_text=_('Indique si la permission est active')
    )

    class Meta:
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')
        ordering = ['module__ordre', 'code']
        db_table = 'permissions'
        indexes = [
            models.Index(fields=['code'], name='idx_permission_code'),
            models.Index(fields=['module'], name='idx_permission_module'),
        ]

    def __str__(self):
        return f"{self.module.code}.{self.code.split('.')[-1]}"


class Role(models.Model):
    """
    Modèle représentant un rôle avec ses permissions associées.

    Les rôles regroupent des ensembles de permissions
    qui peuvent être assignés aux utilisateurs.
    """

    code = models.CharField(
        verbose_name=_('Code'),
        max_length=50,
        unique=True,
        help_text=_('Code unique du rôle (ex: admin_deployment, superviseur_terrain)')
    )
    nom = models.CharField(
        verbose_name=_('Nom'),
        max_length=100,
        help_text=_('Nom du rôle')
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        help_text=_('Description détaillée du rôle')
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('Permissions'),
        related_name='roles',
        blank=True,
        help_text=_('Permissions associées à ce rôle')
    )

    class Meta:
        verbose_name = _('Rôle')
        verbose_name_plural = _('Rôles')
        ordering = ['nom']
        db_table = 'roles'

    def __str__(self):
        return self.nom

    def has_permission(self, permission_code):
        """
        Vérifie si le rôle possède une permission spécifique.

        Args:
            permission_code (str): Code de la permission à vérifier

        Returns:
            bool: True si le rôle possède la permission, False sinon
        """
        return self.permissions.filter(
            code=permission_code,
            is_active=True
        ).exists()

    def get_permissions_by_module(self):
        """
        Retourne les permissions du rôle regroupées par module.

        Returns:
            dict: Dictionnaire {module: [permissions]}
        """
        permissions_by_module = {}
        for permission in self.permissions.filter(is_active=True).select_related('module'):
            module_nom = permission.module.nom
            if module_nom not in permissions_by_module:
                permissions_by_module[module_nom] = []
            permissions_by_module[module_nom].append(permission)
        return permissions_by_module


class Profile(models.Model):
    """
    Modèle Profile pour SUPERVISOR V2.0

    Étend le modèle User de Django avec des informations métier spécifiques.
    Gère la hiérarchie des rôles et les permissions pour l'ensemble de l'application.
    """

    class RoleChoices(models.TextChoices):
        """Choix des rôles utilisateurs selon la hiérarchie"""
        SUPERADMIN = 'SUPERADMIN', _('Super Administrateur')
        ADMIN = 'ADMIN', _('Administrateur')
        COORDONNATEUR = 'COORDONNATEUR', _('Coordonnateur')
        STOCKMAN = 'STOCKMAN', _('Gestionnaire de Stock')
        SUPERVISEUR = 'SUPERVISEUR', _('Superviseur')

    class FonctionChoices(models.TextChoices):
        """Choix des fonctions pour les administrateurs"""
        DG = 'DG', _('Directeur Général')
        DT = 'DT', _('Directeur Technique')
        CHEF_PROJET = 'CHEF_PROJET', _('Chef de Projet')
        AUTRE = 'AUTRE', _('Autre')

    # Lien avec le modèle User de Django
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('Utilisateur'),
        help_text=_('Compte utilisateur Django associé')
    )

    # Champs d'identification
    code = models.CharField(
        verbose_name=_('Code utilisateur'),
        max_length=20,
        unique=True,
        help_text=_('Code unique de l\'utilisateur (ex: AIV001)')
    )

    # Informations personnelles
    nom = models.CharField(
        verbose_name=_('Nom'),
        max_length=100,
        help_text=_('Nom de famille')
    )
    prenoms = models.CharField(
        verbose_name=_('Prénoms'),
        max_length=100,
        help_text=_('Prénom(s)')
    )
    telephone = models.CharField(
        verbose_name=_('Téléphone'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('Numéro de téléphone (format: +225XXXXXXXXXX)')
    )
    photo = models.ImageField(
        verbose_name=_('Photo de profil'),
        upload_to='users/photos/%Y/%m/',
        blank=True,
        null=True,
        help_text=_('Photo de profil de l\'utilisateur')
    )

    # Rôle et hiérarchie
    role = models.CharField(
        verbose_name=_('Rôle'),
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.SUPERVISEUR,
        help_text=_('Rôle de l\'utilisateur dans l\'application')
    )
    fonction = models.CharField(
        verbose_name=_('Fonction'),
        max_length=20,
        choices=FonctionChoices.choices,
        blank=True,
        null=True,
        help_text=_('Fonction (pour les administrateurs)')
    )
    superieur_hierarchique = models.ForeignKey(
        'self',
        verbose_name=_('Supérieur hiérarchique'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordonnés',
        help_text=_('Supérieur hiérarchique direct')
    )
    custom_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('Permissions personnalisées'),
        related_name='profiles',
        blank=True,
        help_text=_('Permissions additionnelles spécifiques à cet utilisateur')
    )

    class Meta:
        verbose_name = _('Profil Utilisateur')
        verbose_name_plural = _('Profils Utilisateurs')
        ordering = ['nom', 'prenoms']
        db_table = 'profiles'
        indexes = [
            models.Index(fields=['code'], name='idx_profile_code'),
            models.Index(fields=['role'], name='idx_profile_role'),
        ]

    def __str__(self):
        """
        Représentation textuelle du profil.

        Returns:
            str: Nom complet de l'utilisateur
        """
        return self.get_full_name()

    def get_full_name(self):
        """
        Retourne le nom complet de l'utilisateur.

        Returns:
            str: Nom complet (format: "NOM Prénoms")
        """
        return f"{self.nom.upper()} {self.prenoms.title()}"

    def get_short_name(self):
        """
        Retourne le nom court de l'utilisateur.

        Returns:
            str: Prénoms de l'utilisateur
        """
        return self.prenoms

    def get_role_display_custom(self):
        """
        Retourne une représentation détaillée du rôle.

        Returns:
            str: Rôle avec fonction si applicable
        """
        role_display = self.get_role_display()
        if self.role == self.RoleChoices.ADMIN and self.fonction:
            return f"{role_display} ({self.get_fonction_display()})"
        return role_display

    @property
    def est_superadmin(self):
        """Vérifie si l'utilisateur est super administrateur"""
        return self.role == self.RoleChoices.SUPERADMIN

    @property
    def est_admin(self):
        """Vérifie si l'utilisateur est administrateur"""
        return self.role == self.RoleChoices.ADMIN

    @property
    def est_coordonnateur(self):
        """Vérifie si l'utilisateur est coordonnateur"""
        return self.role == self.RoleChoices.COORDONNATEUR

    @property
    def est_stockman(self):
        """Vérifie si l'utilisateur est gestionnaire de stock"""
        return self.role == self.RoleChoices.STOCKMAN

    @property
    def est_superviseur(self):
        """Vérifie si l'utilisateur est superviseur"""
        return self.role == self.RoleChoices.SUPERVISEUR

    def has_custom_permission(self, permission_code):
        """
        Vérifie si l'utilisateur possède une permission personnalisée spécifique.

        Args:
            permission_code (str): Code de la permission à vérifier

        Returns:
            bool: True si l'utilisateur possède la permission, False sinon
        """
        return self.custom_permissions.filter(
            code=permission_code,
            is_active=True
        ).exists()

    def get_all_permissions_codes(self):
        """
        Retourne tous les codes de permissions de l'utilisateur.

        Returns:
            list: Liste des codes de permissions actives
        """
        return list(
            self.custom_permissions.filter(is_active=True).values_list('code', flat=True)
        )
