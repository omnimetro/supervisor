"""
Vues (ViewSets) pour l'application users - SUPERVISOR V2.0

Ce module définit les ViewSets Django REST Framework pour :
- Module, Permission, Role : Gestion du système de permissions
- Profile : Gestion des utilisateurs avec actions personnalisées
"""

from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Module, Permission, Role, Profile
from .serializers import (
    ModuleSerializer,
    PermissionSerializer,
    PermissionDetailSerializer,
    RoleSerializer,
    RoleDetailSerializer,
    ProfileSerializer,
    ProfileDetailSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
)


# ============================================
# ViewSets pour le système de permissions
# ============================================

class ModuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Module.

    Actions disponibles :
    - list : Liste de tous les modules
    - retrieve : Détails d'un module
    - create : Créer un nouveau module (admin)
    - update : Mettre à jour un module (admin)
    - partial_update : Mise à jour partielle (admin)
    - destroy : Supprimer un module (admin)

    Filtres :
    - code : Filtrer par code exact
    - search : Recherche dans nom et description
    - ordering : Trier par ordre, nom, code
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code']
    search_fields = ['nom', 'description']
    ordering_fields = ['ordre', 'nom', 'code']
    ordering = ['ordre', 'nom']

    def get_permissions(self):
        """Seuls les admins peuvent créer, modifier ou supprimer"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class PermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Permission.

    Actions disponibles :
    - list : Liste de toutes les permissions
    - retrieve : Détails d'une permission
    - create : Créer une nouvelle permission (admin)
    - update : Mettre à jour une permission (admin)
    - partial_update : Mise à jour partielle (admin)
    - destroy : Supprimer une permission (admin)

    Filtres :
    - module : Filtrer par module (ID)
    - is_active : Filtrer par statut actif/inactif
    - code : Filtrer par code exact
    - search : Recherche dans code, nom et description
    - ordering : Trier par module, code, nom
    """
    queryset = Permission.objects.select_related('module').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['module', 'is_active', 'code']
    search_fields = ['code', 'nom', 'description']
    ordering_fields = ['module__ordre', 'code', 'nom']
    ordering = ['module__ordre', 'code']

    def get_serializer_class(self):
        """Utilise le serializer détaillé pour retrieve"""
        if self.action == 'retrieve':
            return PermissionDetailSerializer
        return PermissionSerializer

    def get_permissions(self):
        """Seuls les admins peuvent créer, modifier ou supprimer"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Role.

    Actions disponibles :
    - list : Liste de tous les rôles
    - retrieve : Détails d'un rôle avec permissions
    - create : Créer un nouveau rôle (admin)
    - update : Mettre à jour un rôle (admin)
    - partial_update : Mise à jour partielle (admin)
    - destroy : Supprimer un rôle (admin)

    Filtres :
    - code : Filtrer par code exact
    - search : Recherche dans nom et description
    - ordering : Trier par nom, code
    """
    queryset = Role.objects.prefetch_related('permissions__module').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code']
    search_fields = ['nom', 'description']
    ordering_fields = ['nom', 'code']
    ordering = ['nom']

    def get_serializer_class(self):
        """Utilise le serializer détaillé pour retrieve"""
        if self.action == 'retrieve':
            return RoleDetailSerializer
        return RoleSerializer

    def get_permissions(self):
        """Seuls les admins peuvent créer, modifier ou supprimer"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


# ============================================
# ViewSet pour Profile (User)
# ============================================

class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Profile (gestion des utilisateurs).

    Actions disponibles :
    - list : Liste de tous les utilisateurs
    - retrieve : Détails d'un utilisateur
    - create : Créer un nouvel utilisateur (admin)
    - update : Mettre à jour un utilisateur (admin)
    - partial_update : Mise à jour partielle (admin)
    - destroy : Désactiver un utilisateur - soft delete (admin)
    - me : Obtenir le profil de l'utilisateur connecté
    - change_password : Changer son mot de passe

    Filtres :
    - role : Filtrer par rôle (SUPERADMIN, ADMIN, etc.)
    - fonction : Filtrer par fonction (DG, DT, CHEF_PROJET)
    - is_active : Filtrer par statut actif/inactif
    - superieur_hierarchique : Filtrer par supérieur (ID)
    - has_permission : Filtrer par permission (code)
    - search : Recherche dans code, nom, prenoms, email
    - ordering : Trier par nom, prenoms, code, role
    """
    queryset = Profile.objects.select_related(
        'user', 'superieur_hierarchique'
    ).prefetch_related(
        'custom_permissions__module', 'subordonnés'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'fonction', 'superieur_hierarchique']
    search_fields = ['code', 'nom', 'prenoms', 'user__email', 'user__username']
    ordering_fields = ['nom', 'prenoms', 'code', 'role']
    ordering = ['nom', 'prenoms']

    def get_serializer_class(self):
        """Sélectionne le serializer approprié selon l'action"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'retrieve':
            return ProfileDetailSerializer
        elif self.action == 'me':
            return UserProfileSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return ProfileSerializer

    def get_queryset(self):
        """Filtre le queryset selon les paramètres"""
        queryset = super().get_queryset()

        # Filtre par is_active (statut du User Django)
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active_bool = is_active.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(user__is_active=is_active_bool)

        # Filtre par permission personnalisée
        has_permission = self.request.query_params.get('has_permission', None)
        if has_permission:
            queryset = queryset.filter(
                custom_permissions__code=has_permission,
                custom_permissions__is_active=True
            ).distinct()

        return queryset

    def get_permissions(self):
        """
        Gestion des permissions :
        - me, change_password : Accessible par l'utilisateur connecté
        - create, update, destroy : Admin uniquement
        - list, retrieve : Utilisateur authentifié
        """
        if self.action in ['me', 'change_password']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        Crée un nouvel utilisateur (User + Profile).

        POST /api/users/
        {
            "username": "user123",
            "email": "user@example.com",
            "password": "SecurePass123!",
            "password2": "SecurePass123!",
            "code": "AIV001",
            "nom": "KOUASSI",
            "prenoms": "Yao",
            "telephone": "+225XXXXXXXXXX",
            "role": "SUPERVISEUR",
            "fonction": null,
            "superieur_hierarchique": 1
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Retourner le profil complet créé
        profile = user.profile
        profile_serializer = UserProfileSerializer(user)

        return Response(
            profile_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """
        Met à jour un utilisateur (User + Profile).

        PUT/PATCH /api/users/{id}/
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # L'instance est un Profile, on récupère le User
        user = instance.user

        serializer = self.get_serializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Retourner le profil complet mis à jour
        profile_serializer = UserProfileSerializer(user)
        return Response(profile_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Désactive un utilisateur (soft delete) au lieu de le supprimer.

        DELETE /api/users/{id}/

        L'utilisateur est marqué comme inactif (is_active=False)
        mais n'est pas supprimé de la base de données.
        """
        instance = self.get_object()
        user = instance.user

        # Soft delete : marquer comme inactif
        user.is_active = False
        user.save()

        return Response(
            {'detail': 'Utilisateur désactivé avec succès'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retourne le profil de l'utilisateur connecté.

        GET /api/users/me/

        Response:
        {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "profile": {
                "id": 1,
                "code": "AIV001",
                "nom": "ADMIN",
                "prenoms": "Super",
                "role": "SUPERADMIN",
                ...
            }
        }
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        Permet à l'utilisateur de changer son mot de passe.

        POST /api/users/change_password/
        {
            "old_password": "ancien_mot_de_passe",
            "new_password": "nouveau_mot_de_passe",
            "new_password2": "nouveau_mot_de_passe"
        }
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Changer le mot de passe
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()

            return Response(
                {'detail': 'Mot de passe modifié avec succès'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        """
        Réactive un utilisateur désactivé.

        POST /api/users/{id}/activate/
        """
        profile = self.get_object()
        user = profile.user

        user.is_active = True
        user.save()

        return Response(
            {'detail': 'Utilisateur activé avec succès'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def deactivate(self, request, pk=None):
        """
        Désactive un utilisateur.

        POST /api/users/{id}/deactivate/
        """
        profile = self.get_object()
        user = profile.user

        user.is_active = False
        user.save()

        return Response(
            {'detail': 'Utilisateur désactivé avec succès'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def subordonnes(self, request, pk=None):
        """
        Retourne la liste des subordonnés d'un utilisateur.

        GET /api/users/{id}/subordonnes/
        """
        profile = self.get_object()
        subordonnes = profile.subordonnés.all()
        serializer = ProfileSerializer(subordonnes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def permissions(self, request, pk=None):
        """
        Retourne les permissions personnalisées d'un utilisateur.

        GET /api/users/{id}/permissions/
        """
        profile = self.get_object()
        permissions = profile.custom_permissions.filter(is_active=True)
        serializer = PermissionDetailSerializer(permissions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def add_permission(self, request, pk=None):
        """
        Ajoute une permission personnalisée à un utilisateur.

        POST /api/users/{id}/add_permission/
        {
            "permission_id": 5
        }
        """
        profile = self.get_object()
        permission_id = request.data.get('permission_id')

        if not permission_id:
            return Response(
                {'error': 'permission_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            permission = Permission.objects.get(id=permission_id)
            profile.custom_permissions.add(permission)
            return Response(
                {'detail': 'Permission ajoutée avec succès'},
                status=status.HTTP_200_OK
            )
        except Permission.DoesNotExist:
            return Response(
                {'error': 'Permission non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def remove_permission(self, request, pk=None):
        """
        Retire une permission personnalisée d'un utilisateur.

        POST /api/users/{id}/remove_permission/
        {
            "permission_id": 5
        }
        """
        profile = self.get_object()
        permission_id = request.data.get('permission_id')

        if not permission_id:
            return Response(
                {'error': 'permission_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            permission = Permission.objects.get(id=permission_id)
            profile.custom_permissions.remove(permission)
            return Response(
                {'detail': 'Permission retirée avec succès'},
                status=status.HTTP_200_OK
            )
        except Permission.DoesNotExist:
            return Response(
                {'error': 'Permission non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
