# -*- coding: utf-8 -*-
"""
Configuration de l'administration Django pour l'application users - SUPERVISOR V2.0

Configure l'interface d'administration pour :
- Profile (utilisateurs)
- Module
- Permission
- Role
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from .models import Module, Permission, Role, Profile


# ============================================
# Inlines pour ProfileAdmin
# ============================================

class SubordonnesInline(admin.TabularInline):
    """
    Inline pour afficher les subordonnes directs d'un profil
    """
    model = Profile
    fk_name = 'superieur_hierarchique'
    extra = 0
    fields = ('code', 'nom', 'prenoms', 'role', 'fonction', 'telephone')
    readonly_fields = ('code', 'nom', 'prenoms', 'role', 'fonction', 'telephone')
    can_delete = False
    show_change_link = True
    verbose_name = "Subordonne"
    verbose_name_plural = "Subordonnes directs"

    def has_add_permission(self, request, obj=None):
        return False


# ============================================
# Admin pour Module
# ============================================

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modele Module
    """
    list_display = ('code', 'nom', 'ordre', 'permissions_count')
    list_filter = ('ordre',)
    search_fields = ('code', 'nom', 'description')
    ordering = ('ordre', 'nom')

    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom', 'description')
        }),
        ('Configuration', {
            'fields': ('ordre',)
        }),
    )

    readonly_fields = ()

    def permissions_count(self, obj):
        """Affiche le nombre de permissions dans ce module"""
        count = obj.permissions.count()
        url = reverse('admin:users_permission_changelist') + f'?module__id__exact={obj.id}'
        return format_html('<a href="{}">{} permission(s)</a>', url, count)
    permissions_count.short_description = 'Permissions'

    def get_readonly_fields(self, request, obj=None):
        """Rend le code readonly apres creation"""
        if obj:  # Edition
            return self.readonly_fields + ('code',)
        return self.readonly_fields


# ============================================
# Admin pour Permission
# ============================================

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modele Permission
    """
    list_display = ('code', 'nom', 'module_link', 'is_active', 'roles_count', 'profiles_count')
    list_filter = ('is_active', 'module')
    search_fields = ('code', 'nom', 'description', 'module__nom')
    ordering = ('module__ordre', 'code')

    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom', 'description')
        }),
        ('Configuration', {
            'fields': ('module', 'is_active')
        }),
    )

    readonly_fields = ()

    def module_link(self, obj):
        """Lien vers le module parent"""
        url = reverse('admin:users_module_change', args=[obj.module.id])
        return format_html('<a href="{}">{}</a>', url, obj.module.nom)
    module_link.short_description = 'Module'

    def roles_count(self, obj):
        """Nombre de roles utilisant cette permission"""
        count = obj.roles.count()
        return f'{count} role(s)'
    roles_count.short_description = 'Roles'

    def profiles_count(self, obj):
        """Nombre de profils ayant cette permission personnalisee"""
        count = obj.profiles.count()
        return f'{count} profil(s)'
    profiles_count.short_description = 'Profils'

    def get_readonly_fields(self, request, obj=None):
        """Rend le code readonly apres creation"""
        if obj:  # Edition
            return self.readonly_fields + ('code',)
        return self.readonly_fields


# ============================================
# Admin pour Role
# ============================================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modele Role
    """
    list_display = ('code', 'nom', 'permissions_count', 'description_short')
    list_filter = ('permissions__module',)
    search_fields = ('code', 'nom', 'description')
    filter_horizontal = ('permissions',)
    ordering = ('nom',)

    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom', 'description')
        }),
        ('Permissions', {
            'fields': ('permissions',),
            'description': 'Selectionnez les permissions associees a ce role'
        }),
    )

    def permissions_count(self, obj):
        """Nombre de permissions dans ce role"""
        count = obj.permissions.count()
        return f'{count} permission(s)'
    permissions_count.short_description = 'Permissions'

    def description_short(self, obj):
        """Description tronquee"""
        if obj.description and len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description or '-'
    description_short.short_description = 'Description'

    def get_readonly_fields(self, request, obj=None):
        """Rend le code readonly apres creation"""
        if obj:  # Edition
            return ('code',)
        return ()


# ============================================
# Admin pour Profile (Utilisateurs)
# ============================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modele Profile (utilisateurs)

    Fonctionnalites :
    - Affichage liste avec informations principales
    - Filtres par role, fonction, statut actif
    - Recherche multi-champs
    - Edition avec fieldsets organises
    - Protection contre suppression du super admin
    - Affichage des subordonnes directs
    """
    list_display = (
        'code',
        'nom_complet',
        'username',
        'email',
        'role_badge',
        'fonction',
        'superieur_link',
        'subordonnes_count',
        'is_active_badge',
        'last_login'
    )

    list_filter = (
        'role',
        'fonction',
        'user__is_active',
        'user__is_staff',
        'user__is_superuser',
        'superieur_hierarchique',
    )

    search_fields = (
        'code',
        'nom',
        'prenoms',
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'telephone',
    )

    ordering = ('nom', 'prenoms')

    filter_horizontal = ('custom_permissions',)

    inlines = [SubordonnesInline]

    fieldsets = (
        ('Informations de connexion', {
            'fields': ('user', 'code')
        }),
        ('Informations personnelles', {
            'fields': ('nom', 'prenoms', 'telephone', 'photo')
        }),
        ('Role et fonction', {
            'fields': ('role', 'fonction', 'superieur_hierarchique')
        }),
        ('Permissions personnalisees', {
            'fields': ('custom_permissions',),
            'classes': ('collapse',),
            'description': 'Permissions supplementaires specifiques a cet utilisateur'
        }),
        ('Informations systeme', {
            'fields': ('user_is_active', 'user_is_staff', 'user_is_superuser', 'user_last_login'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = (
        'user_is_active',
        'user_is_staff',
        'user_is_superuser',
        'user_last_login'
    )

    # ============================================
    # Methodes d'affichage personnalisees
    # ============================================

    def nom_complet(self, obj):
        """Affiche le nom complet"""
        return obj.get_full_name()
    nom_complet.short_description = 'Nom complet'
    nom_complet.admin_order_field = 'nom'

    def username(self, obj):
        """Affiche le username"""
        return obj.user.username
    username.short_description = 'Username'
    username.admin_order_field = 'user__username'

    def email(self, obj):
        """Affiche l'email"""
        return obj.user.email
    email.short_description = 'Email'
    email.admin_order_field = 'user__email'

    def role_badge(self, obj):
        """Affiche le role avec couleur"""
        colors = {
            'SUPERADMIN': '#e74c3c',  # Rouge
            'ADMIN': '#e67e22',        # Orange
            'COORDONNATEUR': '#3498db',  # Bleu
            'STOCKMAN': '#9b59b6',     # Violet
            'SUPERVISEUR': '#2ecc71',  # Vert
        }
        color = colors.get(obj.role, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'
    role_badge.admin_order_field = 'role'

    def superieur_link(self, obj):
        """Lien vers le superieur hierarchique"""
        if obj.superieur_hierarchique:
            url = reverse('admin:users_profile_change', args=[obj.superieur_hierarchique.id])
            return format_html('<a href="{}">{}</a>', url, obj.superieur_hierarchique.get_full_name())
        return '-'
    superieur_link.short_description = 'Superieur'
    superieur_link.admin_order_field = 'superieur_hierarchique'

    def subordonnes_count(self, obj):
        """Nombre de subordonnes directs"""
        count = obj.subordonnés.count()
        if count > 0:
            return format_html('<strong>{}</strong>', count)
        return count
    subordonnes_count.short_description = 'Subordonnes'

    def is_active_badge(self, obj):
        """Badge pour le statut actif"""
        if obj.user.is_active:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Actif</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Inactif</span>'
        )
    is_active_badge.short_description = 'Statut'
    is_active_badge.admin_order_field = 'user__is_active'

    def last_login(self, obj):
        """Derniere connexion"""
        if obj.user.last_login:
            return obj.user.last_login.strftime('%d/%m/%Y %H:%M')
        return 'Jamais'
    last_login.short_description = 'Derniere connexion'
    last_login.admin_order_field = 'user__last_login'

    # ============================================
    # Champs readonly supplementaires
    # ============================================

    def user_is_active(self, obj):
        """Statut actif de l'utilisateur"""
        return obj.user.is_active
    user_is_active.short_description = 'Utilisateur actif'
    user_is_active.boolean = True

    def user_is_staff(self, obj):
        """Statut staff de l'utilisateur"""
        return obj.user.is_staff
    user_is_staff.short_description = 'Staff'
    user_is_staff.boolean = True

    def user_is_superuser(self, obj):
        """Statut superuser de l'utilisateur"""
        return obj.user.is_superuser
    user_is_superuser.short_description = 'Superuser'
    user_is_superuser.boolean = True

    def user_last_login(self, obj):
        """Derniere connexion de l'utilisateur"""
        return obj.user.last_login
    user_last_login.short_description = 'Derniere connexion'

    # ============================================
    # Permissions et securite
    # ============================================

    def has_delete_permission(self, request, obj=None):
        """
        Empeche la suppression du super admin
        """
        if obj and obj.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        """
        Configure les champs readonly
        - code : readonly apres creation
        - user : readonly apres creation
        """
        readonly = list(self.readonly_fields)
        if obj:  # Edition
            readonly.extend(['code', 'user'])
        return readonly

    def get_queryset(self, request):
        """
        Optimise les requetes avec select_related et prefetch_related
        """
        qs = super().get_queryset(request)
        return qs.select_related(
            'user',
            'superieur_hierarchique',
            'superieur_hierarchique__user'
        ).prefetch_related(
            'subordonnés',
            'custom_permissions',
            'custom_permissions__module'
        )

    # ============================================
    # Actions personnalisees
    # ============================================

    actions = ['activer_utilisateurs', 'desactiver_utilisateurs']

    def activer_utilisateurs(self, request, queryset):
        """Active les utilisateurs selectionnes"""
        count = 0
        for profile in queryset:
            if not profile.user.is_active:
                profile.user.is_active = True
                profile.user.save()
                count += 1

        self.message_user(
            request,
            f'{count} utilisateur(s) active(s) avec succes.'
        )
    activer_utilisateurs.short_description = 'Activer les utilisateurs selectionnes'

    def desactiver_utilisateurs(self, request, queryset):
        """Desactive les utilisateurs selectionnes (sauf super admins)"""
        count = 0
        skipped = 0
        for profile in queryset:
            if profile.user.is_superuser:
                skipped += 1
                continue
            if profile.user.is_active:
                profile.user.is_active = False
                profile.user.save()
                count += 1

        message = f'{count} utilisateur(s) desactive(s) avec succes.'
        if skipped > 0:
            message += f' {skipped} super admin(s) ignore(s).'

        self.message_user(request, message)
    desactiver_utilisateurs.short_description = 'Desactiver les utilisateurs selectionnes'


# ============================================
# Personnalisation du site admin
# ============================================

# Titre du site admin
admin.site.site_header = "SUPERVISOR V2.0 - Administration"
admin.site.site_title = "SUPERVISOR Admin"
admin.site.index_title = "Gestion de l'application"
