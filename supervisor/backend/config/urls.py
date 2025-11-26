"""
Configuration des URLs pour SUPERVISOR V2.0

La liste `urlpatterns` route les URLs vers les vues. Pour plus d'informations :
https://docs.djangoproject.com/en/4.2/topics/http/urls/

Structure de l'API :
- /admin/ : Interface d'administration Django
- /api/token/ : Authentification JWT (obtain, refresh, verify)
- /api/users/ : Gestion des utilisateurs et authentification
- /api/deployment/ : Gestion des chantiers de déploiement
- /api/b2b/ : Gestion des raccordements et maintenances B2B
- /api/inventory/ : Gestion des stocks de matériels
- /api/expenses/ : Gestion des dépenses
- /api/mapping/ : Gestion de la cartographie et tracking GPS
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import permissions


def api_root(request):
    """
    Vue racine de l'API - Fournit une liste des endpoints disponibles
    """
    return JsonResponse({
        'message': 'Bienvenue sur l\'API SUPERVISOR V2.0',
        'version': '2.0',
        'endpoints': {
            'admin': '/admin/',
            'auth': {
                'token_obtain': '/api/token/',
                'token_refresh': '/api/token/refresh/',
                'token_verify': '/api/token/verify/',
            },
            'documentation': '/api/docs/',
            'users': '/api/users/',
            'deployment': '/api/deployment/',
            # 'b2b': '/api/b2b/',
            # 'inventory': '/api/inventory/',
            # 'expenses': '/api/expenses/',
            # 'mapping': '/api/mapping/',
        }
    })


# ============================================
# Configuration de la documentation API (Swagger)
# ============================================
try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="SUPERVISOR V2.0 API",
            default_version='v2.0',
            description="""
            API REST pour l'application SUPERVISOR V2.0

            Gestion complète des opérations terrain pour AI Venture :
            - Chantiers de déploiement de réseaux fibre optique
            - Raccordements et maintenances B2B
            - Gestion des stocks de matériels
            - Suivi des dépenses
            - Cartographie et tracking GPS

            **Authentification:** JWT Bearer Token

            Pour obtenir un token :
            1. POST /api/token/ avec username et password
            2. Utiliser le token dans le header : Authorization: Bearer <token>
            """,
            terms_of_service="",
            contact=openapi.Contact(email="contact@aiventure.com"),
            license=openapi.License(name="Propriété AI Venture"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    # Routes de documentation disponibles
    documentation_urls = [
        # Documentation Swagger UI
        re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        # Documentation ReDoc
        re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        # Schema JSON
        re_path(r'^api/schema/$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    ]
except ImportError:
    # drf-yasg n'est pas installé, on ignore
    documentation_urls = []


urlpatterns = [
    # ============================================
    # Vue racine de l'API
    # ============================================
    path('', api_root, name='api_root'),
    path('api/', api_root, name='api_root_explicit'),

    # ============================================
    # Administration Django
    # ============================================
    path('admin/', admin.site.urls),

    # ============================================
    # Authentification JWT
    # ============================================
    # Obtenir un nouveau token (login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Rafraîchir un token expiré
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Vérifier la validité d'un token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # ============================================
    # URLs des applications métier
    # ============================================

    # Gestion des utilisateurs et authentification
    path('api/', include('apps.users.urls')),

    # Gestion des chantiers de déploiement
    path('api/deployment/', include('apps.deployment.urls')),

    # Gestion des raccordements et maintenances B2B
    # path('api/b2b/', include('apps.b2b.urls')),

    # Gestion des stocks de matériels et consommables
    # path('api/inventory/', include('apps.inventory.urls')),

    # Gestion des dépenses liées aux travaux
    # path('api/expenses/', include('apps.expenses.urls')),

    # Gestion de la cartographie et tracking GPS
    # path('api/mapping/', include('apps.mapping.urls')),
]

# Ajouter les URLs de documentation (si drf-yasg est installé)
urlpatterns += documentation_urls

# Configuration pour servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Django Debug Toolbar (si installé)
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass

# Personnalisation de l'administration
admin.site.site_header = "SUPERVISOR V2.0 - Administration"
admin.site.site_title = "SUPERVISOR Admin"
admin.site.index_title = "Gestion de l'application"
