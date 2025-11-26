"""
Configuration des URLs pour l'application users - SUPERVISOR V2.0

Ce module définit les routes API pour :
- Modules, Permissions, Roles : Gestion du système de permissions
- Users (Profiles) : Gestion des utilisateurs
- Auth : Authentification JWT (Login, Register, Logout)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ModuleViewSet,
    PermissionViewSet,
    RoleViewSet,
    ProfileViewSet,
)
from .auth_views import (
    CustomTokenObtainPairView,
    login_view,
    register_view,
    logout_view,
    verify_token_view,
)

# Créer le router DRF
router = DefaultRouter()

# Enregistrer les ViewSets
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'users', ProfileViewSet, basename='user')

# URLs de l'application
urlpatterns = [
    # Routes des ViewSets
    path('', include(router.urls)),

    # Routes d'authentification JWT
    path('auth/login/', login_view, name='auth-login'),
    path('auth/register/', register_view, name='auth-register'),
    path('auth/logout/', logout_view, name='auth-logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/verify/', verify_token_view, name='auth-verify'),

    # Route alternative avec TokenObtainPairView personnalisée
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='auth-token'),
]
