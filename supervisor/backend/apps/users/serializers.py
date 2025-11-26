"""
Serializers pour l'application users - SUPERVISOR V2.0

Ce module définit les serializers Django REST Framework pour :
- Module, Permission, Role : Système de permissions granulaires
- Profile : Profil utilisateur avec informations métier
- User : Compte utilisateur Django (authentification)
"""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Module, Permission, Role, Profile


# ============================================
# Serializers pour le système de permissions
# ============================================

class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Module.

    Utilisé pour regrouper les permissions par fonctionnalité.
    """
    permissions_count = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'code', 'nom', 'description', 'ordre', 'permissions_count']
        read_only_fields = ['id']

    def get_permissions_count(self, obj):
        """Retourne le nombre de permissions dans ce module"""
        return obj.permissions.filter(is_active=True).count()


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Permission.

    Permissions granulaires par action (create, read, update, delete).
    """
    module_nom = serializers.CharField(source='module.nom', read_only=True)
    module_code = serializers.CharField(source='module.code', read_only=True)

    class Meta:
        model = Permission
        fields = [
            'id', 'code', 'nom', 'description',
            'module', 'module_nom', 'module_code', 'is_active'
        ]
        read_only_fields = ['id']


class PermissionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour le modèle Permission avec module complet.
    """
    module = ModuleSerializer(read_only=True)

    class Meta:
        model = Permission
        fields = ['id', 'code', 'nom', 'description', 'module', 'is_active']
        read_only_fields = ['id']


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Role.

    Ensembles de permissions prédéfinis.
    """
    permissions_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'code', 'nom', 'description', 'permissions', 'permissions_count']
        read_only_fields = ['id']

    def get_permissions_count(self, obj):
        """Retourne le nombre de permissions actives dans ce rôle"""
        return obj.permissions.filter(is_active=True).count()


class RoleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour le modèle Role avec permissions complètes.
    """
    permissions = PermissionDetailSerializer(many=True, read_only=True)
    permissions_by_module = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'code', 'nom', 'description', 'permissions', 'permissions_by_module']
        read_only_fields = ['id']

    def get_permissions_by_module(self, obj):
        """Retourne les permissions regroupées par module"""
        return obj.get_permissions_by_module()


# ============================================
# Serializers pour User et Profile
# ============================================

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle User Django natif.

    Utilisé pour l'authentification et les informations de base.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Profile.

    Contient les informations métier de l'utilisateur.
    """
    user = UserSerializer(read_only=True)
    superieur_nom = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    fonction_display = serializers.CharField(source='get_fonction_display', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'code', 'nom', 'prenoms', 'telephone', 'photo',
            'role', 'role_display', 'fonction', 'fonction_display',
            'superieur_hierarchique', 'superieur_nom', 'custom_permissions',
            'full_name'
        ]
        read_only_fields = ['id']

    def get_superieur_nom(self, obj):
        """Retourne le nom complet du supérieur hiérarchique"""
        if obj.superieur_hierarchique:
            return obj.superieur_hierarchique.get_full_name()
        return None


class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour le modèle Profile avec toutes les relations.
    """
    user = UserSerializer(read_only=True)
    superieur_hierarchique = ProfileSerializer(read_only=True)
    custom_permissions = PermissionDetailSerializer(many=True, read_only=True)
    subordonnes = serializers.SerializerMethodField()
    permissions_codes = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'code', 'nom', 'prenoms', 'telephone', 'photo',
            'role', 'fonction', 'superieur_hierarchique', 'custom_permissions',
            'subordonnes', 'permissions_codes'
        ]
        read_only_fields = ['id']

    def get_subordonnes(self, obj):
        """Retourne la liste des subordonnés directs"""
        subordonnes = obj.subordonnés.all()
        return ProfileSerializer(subordonnes, many=True).data

    def get_permissions_codes(self, obj):
        """Retourne la liste des codes de permissions"""
        return obj.get_all_permissions_codes()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création d'un utilisateur avec son profil.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Cet email est déjà utilisé")]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    # Champs du profil
    code = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all(), message="Ce code utilisateur est déjà utilisé")]
    )
    nom = serializers.CharField(required=True)
    prenoms = serializers.CharField(required=True)
    telephone = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=Profile.RoleChoices.choices, default=Profile.RoleChoices.SUPERVISEUR)
    fonction = serializers.ChoiceField(choices=Profile.FonctionChoices.choices, required=False, allow_null=True)
    superieur_hierarchique = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'code', 'nom', 'prenoms', 'telephone', 'role', 'fonction', 'superieur_hierarchique'
        ]

    def validate(self, attrs):
        """Validation personnalisée"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})

        # Vérifier que le username n'existe pas
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Ce nom d'utilisateur est déjà utilisé"})

        return attrs

    def create(self, validated_data):
        """Crée un utilisateur User et son Profile associé"""
        # Extraire les données du profil
        profile_data = {
            'code': validated_data.pop('code'),
            'nom': validated_data.pop('nom'),
            'prenoms': validated_data.pop('prenoms'),
            'telephone': validated_data.pop('telephone', ''),
            'role': validated_data.pop('role', Profile.RoleChoices.SUPERVISEUR),
            'fonction': validated_data.pop('fonction', None),
            'superieur_hierarchique': validated_data.pop('superieur_hierarchique', None),
        }

        # Supprimer password2
        validated_data.pop('password2')

        # Créer l'utilisateur User
        user = User.objects.create_user(**validated_data)

        # Créer le profil associé
        profile = Profile.objects.create(user=user, **profile_data)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la mise à jour d'un utilisateur et son profil.
    """
    email = serializers.EmailField(required=False)

    # Champs du profil
    code = serializers.CharField(required=False)
    nom = serializers.CharField(required=False)
    prenoms = serializers.CharField(required=False)
    telephone = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=Profile.RoleChoices.choices, required=False)
    fonction = serializers.ChoiceField(choices=Profile.FonctionChoices.choices, required=False, allow_null=True)
    superieur_hierarchique = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'is_active',
            'code', 'nom', 'prenoms', 'telephone', 'role', 'fonction', 'superieur_hierarchique'
        ]

    def update(self, instance, validated_data):
        """Met à jour l'utilisateur User et son Profile"""
        # Extraire les données du profil
        profile_data = {}
        profile_fields = ['code', 'nom', 'prenoms', 'telephone', 'role', 'fonction', 'superieur_hierarchique']
        for field in profile_fields:
            if field in validated_data:
                profile_data[field] = validated_data.pop(field)

        # Mettre à jour l'utilisateur User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mettre à jour le profil
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer pour le changement de mot de passe.
    """
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, validators=[validate_password], style={'input_type': 'password'})
    new_password2 = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        """Validation personnalisée"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Les nouveaux mots de passe ne correspondent pas"})
        return attrs

    def validate_old_password(self, value):
        """Vérifie que l'ancien mot de passe est correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect")
        return value


class LoginSerializer(serializers.Serializer):
    """
    Serializer pour l'authentification.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer combiné User + Profile pour les réponses API complètes.
    """
    profile = ProfileDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'date_joined', 'last_login', 'profile'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
