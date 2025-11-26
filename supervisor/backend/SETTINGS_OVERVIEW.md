# Configuration Django - Vue d'ensemble

Document récapitulatif de la configuration Django de SUPERVISOR V2.0

---

## ✅ Configurations en Place

### 1. Utilisation de python-decouple

**Status** : ✅ Configuré

Toutes les variables sensibles utilisent `python-decouple` pour lire les valeurs depuis le fichier `.env` :

```python
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY', default='...')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
```

**Avantages** :
- Séparation des secrets du code source
- Valeurs par défaut pour le développement
- Conversion automatique des types (bool, int, Csv)

---

### 2. Configuration MySQL

**Status** : ✅ Configuré

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='supervisor_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

**Caractéristiques** :
- Encodage UTF-8 (utf8mb4) pour support complet Unicode
- Mode strict activé pour éviter les données invalides
- Toutes les valeurs configurables via .env

---

### 3. Django REST Framework

**Status** : ✅ Configuré

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M:%S',
}
```

**Fonctionnalités activées** :
- ✅ Authentification JWT + Session
- ✅ Permissions par défaut (IsAuthenticated)
- ✅ Pagination (50 éléments par page)
- ✅ Filtres (DjangoFilter, Search, Ordering)
- ✅ Formats de date/heure standardisés

---

### 4. Simple JWT (Authentification)

**Status** : ✅ Configuré avec variables d'environnement

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        hours=config('JWT_ACCESS_TOKEN_LIFETIME_HOURS', default=2, cast=int)
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7, cast=int)
    ),
    'ROTATE_REFRESH_TOKENS': config('JWT_ROTATE_REFRESH_TOKENS', default=True, cast=bool),
    'BLACKLIST_AFTER_ROTATION': config('JWT_BLACKLIST_AFTER_ROTATION', default=True, cast=bool),
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

**Paramètres de sécurité** :
- ✅ Durée de vie des tokens configurable via .env
- ✅ Rotation automatique des refresh tokens
- ✅ Blacklist des tokens après rotation
- ✅ Mise à jour de last_login
- ✅ Algorithme HS256

---

### 5. CORS (Cross-Origin Resource Sharing)

**Status** : ✅ Configuré

```python
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:8080,http://localhost:9000',
    cast=Csv()
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]
```

**Configuration** :
- ✅ Origines autorisées configurables via .env
- ✅ Credentials (cookies) autorisés
- ✅ Méthodes HTTP standards autorisées
- ✅ Headers nécessaires pour JWT autorisés

---

### 6. Fichiers Media et Static

**Status** : ✅ Configuré

```python
# Fichiers statiques (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Fichiers media (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Caractéristiques** :
- ✅ Fichiers statiques servis par WhiteNoise (production)
- ✅ Compression et cache des fichiers statiques
- ✅ Séparation claire entre static et media
- ✅ Structure de dossiers organisée

---

### 7. Configuration des Uploads

**Status** : ✅ Configuré avec variables d'environnement

```python
# Taille maximale des fichiers uploadés (100 MB par défaut)
DATA_UPLOAD_MAX_MEMORY_SIZE = config(
    'DATA_UPLOAD_MAX_MEMORY_SIZE',
    default=104857600,  # 100 MB
    cast=int
)
FILE_UPLOAD_MAX_MEMORY_SIZE = config(
    'FILE_UPLOAD_MAX_MEMORY_SIZE',
    default=104857600,  # 100 MB
    cast=int
)

# Types de fichiers autorisés
ALLOWED_IMAGE_TYPES = config(
    'ALLOWED_IMAGE_TYPES',
    default='image/jpeg,image/jpg,image/png,image/gif',
    cast=Csv()
)

ALLOWED_DOCUMENT_TYPES = config(
    'ALLOWED_DOCUMENT_TYPES',
    default='application/pdf,application/msword,...',
    cast=Csv()
)
```

**Sécurité** :
- ✅ Limite de taille configurable
- ✅ Validation des types MIME
- ✅ Types autorisés configurables via .env

---

### 8. Internationalisation

**Status** : ✅ Configuré (Français, Côte d'Ivoire)

```python
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Abidjan'
USE_I18N = True
USE_TZ = True
```

**Configuration** :
- ✅ Langue : Français (fr-fr)
- ✅ Timezone : Africa/Abidjan (Côte d'Ivoire)
- ✅ Internationalisation activée
- ✅ Support des timezones activé

---

### 9. INSTALLED_APPS

**Status** : ✅ Configuré avec commentaires pour apps futures

```python
INSTALLED_APPS = [
    # Applications Django par défaut
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications tierces
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'django_extensions',

    # Applications du projet (à décommenter une fois créées)
    # 'apps.users',
    # 'apps.deployment',
    # 'apps.b2b',
    # 'apps.inventory',
    # 'apps.expenses',
    # 'apps.mapping',
]
```

**Organisation** :
- ✅ Apps Django par défaut
- ✅ Apps tierces (REST, JWT, CORS)
- ✅ Apps du projet commentées (à activer)

---

### 10. Validateurs de Mots de Passe

**Status** : ✅ Configuré

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Validations** :
- ✅ Similarité avec attributs utilisateur
- ✅ Longueur minimale : 8 caractères
- ✅ Vérification des mots de passe courants
- ✅ Interdiction des mots de passe purement numériques

---

### 11. Celery (Tâches Asynchrones)

**Status** : ✅ Configuré

```python
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
```

**Caractéristiques** :
- ✅ Broker Redis configurable
- ✅ Format JSON pour sérialisation
- ✅ Timezone synchronisée
- ✅ Tracking des tâches
- ✅ Timeout de 30 minutes

---

### 12. Logging (Journalisation)

**Status** : ✅ Configuré

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {...},
        'simple': {...},
    },
    'handlers': {
        'console': {...},  # Sortie console
        'file': {...},     # Fichier logs/django.log
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}
```

**Fonctionnalités** :
- ✅ Logs dans console et fichier
- ✅ Format détaillé pour fichiers
- ✅ Niveau ajustable selon DEBUG
- ✅ Dossier logs/ créé automatiquement

---

### 13. APIs Externes

**Status** : ✅ Configuré

```python
# Google Maps API
GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY', default='')

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_WHATSAPP_FROM = config('TWILIO_WHATSAPP_FROM', default='')

# WhatsGPS API
WHATSGPS_API_KEY = config('WHATSGPS_API_KEY', default='')
WHATSGPS_API_URL = config('WHATSGPS_API_URL', default='')
```

**APIs intégrées** :
- ✅ Google Maps (cartographie)
- ✅ Twilio (WhatsApp)
- ✅ WhatsGPS (tracking véhicules)

---

### 14. Configuration Spécifique au Projet

**Status** : ✅ Configuré

```python
# Configuration de la facturation (périodes du 20 au 21 du mois suivant)
BILLING_START_DAY = 20
BILLING_END_DAY = 21

# Opérateurs supportés
OPERATORS = {
    'ORANGE': {
        'name': 'Orange Côte d\'Ivoire',
        'code': 'ORANGE',
    },
    'MOOV': {
        'name': 'Moov Africa',
        'code': 'MOOV',
    },
}
```

**Paramètres métier** :
- ✅ Périodes de facturation
- ✅ Liste des opérateurs

---

### 15. Sécurité Production

**Status** : ✅ Configuré (activé si DEBUG=False)

```python
if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HSTS
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Autres paramètres de sécurité
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
```

**Sécurité activée en production** :
- ✅ Redirection HTTPS forcée
- ✅ Cookies sécurisés
- ✅ HSTS (HTTP Strict Transport Security)
- ✅ Protection XSS
- ✅ Protection Clickjacking

---

## 📋 Checklist de Configuration

- [x] python-decouple pour variables d'environnement
- [x] Configuration MySQL
- [x] Django REST Framework
- [x] Simple JWT avec variables .env
- [x] CORS pour le frontend
- [x] Fichiers media et static
- [x] Configuration des uploads avec variables .env
- [x] Internationalisation (français, Abidjan)
- [x] INSTALLED_APPS avec commentaires
- [x] Validateurs de mots de passe
- [x] Celery (tâches asynchrones)
- [x] Logging (console + fichier)
- [x] APIs externes (Google Maps, Twilio, WhatsGPS)
- [x] Configuration métier (facturation, opérateurs)
- [x] Sécurité production

---

## 🚀 Prochaines Étapes

1. **Créer le fichier `.env`** à partir de `.env.example`
2. **Installer les dépendances** : `pip install -r requirements-dev.txt`
3. **Créer la base de données MySQL** : `supervisor_db`
4. **Tester la configuration** : `python manage.py check`
5. **Effectuer les migrations** : `python manage.py migrate`
6. **Créer un superutilisateur** : `python manage.py createsuperuser`

---

**Dernière mise à jour** : 2025-11-11
