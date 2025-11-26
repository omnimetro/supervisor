# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Langue du Projet / Project Language

**IMPORTANT: Ce projet est entièrement en français.**
- Toutes les communications avec l'utilisateur doivent être en français
- Tous les commentaires de code doivent être en français
- Toute la documentation doit être en français
- Les noms de variables, fonctions et classes peuvent être en anglais (convention de programmation) mais les docstrings et commentaires doivent être en français
- Les messages d'erreur et retours utilisateur doivent être en français

## Présentation du Projet

SUPERVISOR V2.0 est une application web complète pour la gestion de projets de déploiement de réseaux fibre optique, les raccordements B2B, les opérations de maintenance, et les équipements de terrain pour AI Venture (AIV), un sous-traitant en télécommunications.

**Modules principaux :**
- Gestion des chantiers (déploiement, backbone, transport, réseaux de distribution)
- Suivi des raccordements et maintenances B2B
- Gestion des stocks de matériels et consommables
- Suivi des dépenses et facturation
- Reporting terrain en temps réel avec photos géolocalisées
- Cartographie et tracking des véhicules via Google Maps
- Analyse et reporting assistés par IA

## Stack Technique

**Frontend :**
- Quasar Framework v2.16.0 (basé sur Vue.js 3.4.18)
- Vite v7.2.2 comme build tool
- Pinia v3.0.1 pour la gestion d'état
- Axios v1.2.1 pour les requêtes HTTP
- PWA avec Workbox (mode hors ligne)
- Design responsive mobile-first (téléphone/tablette/desktop)
- Intégration Google Maps API
- Authentication JWT (access + refresh tokens)
- Composition API Vue.js 3

**Backend :**
- Django 4.2.16
- Django REST Framework
- Python 3.12.7
- Base de données MySQL
- JWT Authentication (Simple JWT)
- CORS configuré pour le frontend

**Environnement de Développement :**
- Windows 11
- VS Code
- Environnement virtuel Python (.venv)
- WAMP Server pour MySQL
- Node.js et npm
- Quasar CLI v2.4.0

## Commandes de Développement

### Configuration de l'Environnement
```bash
# Se placer dans le dossier backend
cd supervisor/backend

# Activer l'environnement virtuel (Windows)
.venv\Scripts\activate

# Installer les dépendances Python
pip install -r requirements.txt

# Configuration des variables d'environnement
# Créer un fichier .env à la racine de backend/ avec :
# - SECRET_KEY : Clé secrète Django
# - DEBUG : True/False
# - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT : Configuration MySQL
# - GOOGLE_MAPS_API_KEY : Clé API Google Maps
# - TWILIO_* : Configuration WhatsApp (optionnel)
# - WHATSGPS_* : Configuration tracking GPS (optionnel)

# Migrations de base de données
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### Lancement de l'Application
```bash
# Démarrer le serveur de développement Django (depuis backend/)
python manage.py runserver

# Lancer avec un port personnalisé
python manage.py runserver 8080

# Accéder à l'interface admin
# http://localhost:8000/admin/

# Accéder à la documentation API Swagger
# http://localhost:8000/api/docs/

# Démarrer le serveur de développement frontend (Quasar)
cd ../frontend
npm install
quasar dev
```

### Tests
```bash
# Lancer tous les tests (depuis backend/)
python manage.py test

# Lancer les tests d'une application spécifique
python manage.py test apps.<app_name>

# Utiliser pytest (recommandé)
pytest

# Lancer avec couverture de code
pytest --cov=apps --cov-report=html

# Linter et formatage du code
flake8 apps/
black apps/
isort apps/
```

### Opérations sur la Base de Données
```bash
# Créer une sauvegarde de la base de données
python manage.py dumpdata > backup.json

# Charger une sauvegarde
python manage.py loaddata backup.json

# Réinitialiser la base de données (attention : destructif)
python manage.py flush
```

## Architecture et Concepts Clés

### Structure du Projet Backend

Le backend Django est organisé selon une architecture modulaire :

```
backend/
├── config/              # Configuration centrale du projet
│   ├── settings.py     # Configuration Django (utilise python-decouple pour .env)
│   ├── urls.py         # Routage principal de l'API
│   ├── celery.py       # Configuration des tâches asynchrones
│   ├── wsgi.py         # Point d'entrée WSGI pour production
│   └── asgi.py         # Point d'entrée ASGI pour WebSockets
│
├── apps/               # Applications Django modulaires
│   ├── users/         # ✅ COMPLÉTÉ - Gestion des utilisateurs et permissions
│   │   ├── models.py          # Profile, Module, Permission, Role
│   │   ├── serializers.py     # Tous les serializers DRF (13KB)
│   │   ├── views.py           # ViewSets CRUD (17KB)
│   │   ├── auth_views.py      # Vues JWT custom (8KB)
│   │   ├── admin.py           # Interface admin Django (15KB)
│   │   ├── urls.py            # Routes API
│   │   └── tests/             # Tests unitaires complets (78KB)
│   ├── deployment/    # (À créer) Gestion des chantiers de déploiement
│   ├── b2b/          # (À créer) Raccordements et maintenances B2B
│   ├── inventory/     # (À créer) Gestion des stocks
│   ├── expenses/      # (À créer) Suivi des dépenses
│   └── mapping/       # (À créer) Cartographie et tracking GPS
│
├── media/             # Fichiers uploadés (photos, documents)
├── static/            # Fichiers statiques de développement
├── staticfiles/       # Fichiers statiques collectés pour production
├── logs/              # Logs de l'application
└── templates/         # Templates Django globaux
```

**Convention de nommage des apps Django :**
- Chaque app dans `apps/` contient : models.py, views.py, serializers.py, urls.py, admin.py, tests/
- Les URLs des apps sont préfixées par `/api/<app_name>/`
- Authentification JWT requise pour tous les endpoints sauf `/api/token/`

### Hiérarchie du Modèle de Données

**Gestion des Chantiers :**
- Opérateurs (Orange, Moov) → Chantiers → Tâches
- Chaque opérateur possède un BOQ (Bordereau de Quantité) avec les travaux standardisés et prix unitaires
- Les chantiers suivent un planning prévisionnel vs réalisé avec reporting quotidien
- Les tâches sont affectées aux techniciens AIV ou aux sous-traitants

**Opérations B2B :**
- Organisation par zones géographiques avec équipes dédiées
- Processus en deux étapes : Étude (repérage terrain) → Raccordement (installation)
- Les demandes de maintenance sont traitées directement sans phase d'étude
- L'utilisation des matériels est tracée par intervention

**Système de Gestion des Stocks :**
- Deux types de stocks : matériels propriété AIV et matériels fournis par l'opérateur
- Traçabilité des mouvements : acquisitions, affectations, récupérations, retours, indisponibilités
- Métriques calculées : QMP (quantité matériel possédé), QAffectés (quantité affectée), Dispos (quantité disponible)

**Gestion des Dépenses :**
- Liées aux chantiers, équipes B2B ou techniciens
- Catégories : achats, locations, prestations, main d'œuvre, carburant, per diem

### Rôles Utilisateurs et Permissions

- Super Administrateur : Accès complet au système
- Administrateur : Gestion au niveau des modules
- Coordonnateur : Supervision multi-chantiers
- Superviseur : Gestion au niveau chantier/équipe
- Gestionnaire de Stock : Contrôle des inventaires

Toutes les actions sensibles sont journalisées pour audit.

### Reporting et Documentation

**Génération Automatique de Rapports :**
- Rapports quotidiens de tâches avec photos géolocalisées (NoteCam)
- Rapports de fin de chantier (RFC) au format PowerPoint selon modèle opérateur
- Récapitulatifs des travaux en Excel selon modèles fournis par l'opérateur
- Rapports d'étude et rapports d'installation pour B2B

**Extraction des Données GPS :**
- Positions extraites des photos NoteCam pour cartographie
- Cartographie des infrastructures : poteaux (métallique/béton), équipements (PCO, PEC, PEP, JDV), chambres

### Points d'Intégration

- Google Maps API : cartographie, positionnement des clients, tracking des véhicules
- WhatsGPS API : intégration des traceurs GPS pour véhicules équipés
- Application mobile de tracking : suivi GPS pour véhicules non équipés
- WhatsApp : notifications et alertes
- Import de fichiers KMZ : visualisation en temps réel des réseaux

## Règles de Développement Obligatoires

**Extraites de instructions.md :**

1. **JAMAIS improviser** : Suivre uniquement les spécifications fournies
2. **JAMAIS sauter d'étape** : Compléter chaque phase avant de passer à la suivante
3. **TOUJOURS valider** : Tester le code à chaque étape avant de continuer
4. **TOUJOURS documenter** : Commenter le code et documenter les décisions de conception
5. **TOUJOURS demander confirmation** : Clarifier les instructions ambiguës ou incohérentes
6. **JAMAIS inventer de fonctionnalités** : Créer uniquement ce qui est explicitement spécifié
7. **TOUJOURS expliquer et attendre** : Décrire ce qui sera fait et attendre validation avant d'implémenter

## Système de Design

**Palette de Couleurs :**
- Primaire : #ea1d31 (rouge de marque)
- Secondaire : #cc4b5a, #cd5d63
- Accent : #00BFA5 (bleu sarcelle), #FFD54F (jaune)
- Fonctionnel : Succès #43A047, Erreur #E53935, Neutre #9E9E9E
- Fonds : #FFFFFF (blanc), #F5F7F9 (clair), #263238 (mode sombre)

**Typographie :**
- Police Principale : SF Pro Text (iOS) / Roboto (Android) / Inter (Web)
- H1 : 28px/Gras, H2 : 24px/Gras, H3 : 20px/Semi-gras
- Corps : 15-17px/Régulier

**Composants :**
- Boutons : hauteur 48dp, rayon de bordure 8dp
- Cartes : rayon de bordure 12dp, ombre subtile
- Champs de saisie : hauteur 56dp, rayon de bordure 8dp
- Icônes : 24dp standard, 28dp navigation

**Système d'Espacement :**
- 4dp (micro), 8dp (petit), 16dp (défaut), 24dp (moyen), 32dp (large), 48dp (padding écran)

**Animations :**
- Standard : 200ms ease-out
- Accent : 300ms spring
- Micro-interactions : 150ms ease-in-out
- Transitions de page : 350ms cubic-bezier

## Configuration Technique Importante

### Variables d'Environnement (.env)

Le projet utilise `python-decouple` pour gérer la configuration. Créer un fichier `.env` dans `backend/` avec :

```env
# Django Core
SECRET_KEY=votre-cle-secrete-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database MySQL
DB_NAME=supervisor_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME_HOURS=2
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
JWT_ROTATE_REFRESH_TOKENS=True
JWT_BLACKLIST_AFTER_ROTATION=True

# CORS (pour le frontend Quasar)
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:9000

# Google Maps API
GOOGLE_MAPS_API_KEY=votre-cle-api-google-maps

# WhatsApp via Twilio (optionnel)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_FROM=

# WhatsGPS API (optionnel)
WHATSGPS_API_KEY=
WHATSGPS_API_URL=

# Celery & Redis (pour tâches asynchrones)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Services Requis

**Pour le développement complet :**
1. **MySQL** : WAMP Server sur Windows (port 3306)
2. **Redis** : Requis pour Celery (tâches asynchrones comme génération de rapports)
   - Windows : Télécharger depuis https://github.com/microsoftarchive/redis/releases
   - Démarrer : `redis-server`
3. **Tesseract OCR** : Pour l'analyse de documents (pytesseract)
   - Windows : https://github.com/UB-Mannheim/tesseract/wiki

**Démarrage des workers Celery (optionnel en dev) :**
```bash
# Terminal 1 : Django
python manage.py runserver

# Terminal 2 : Celery Worker
celery -A config worker -l info

# Terminal 3 : Celery Beat (tâches planifiées)
celery -A config beat -l info
```

### API REST Framework

**Structure des endpoints :**
- Authentification JWT : `/api/token/` (obtain, refresh, verify)
- Documentation Swagger : `/api/docs/`
- Documentation ReDoc : `/api/redoc/`
- Schema JSON : `/api/schema/`

**Pagination par défaut :** 50 éléments par page

**Filtrage et recherche :**
- Utilise `django-filter` pour filtrage avancé
- Support du tri via paramètre `?ordering=`
- Support de la recherche via paramètre `?search=`

## Fichiers de Documentation Clés

- `instructions.md` : Règles fondamentales de développement et méthodologie
- `supervisor_doc/supervisor_presentation.md` : Spécifications fonctionnelles complètes
- `supervisor_doc/supervisor_design_patern.md` : Directives UI/UX et spécifications des composants
- `supervisor_doc/travaux_orange.xlsx` : BOQ de référence de l'opérateur Orange
- `supervisor_doc/travaux_moov.xlsx` : BOQ de référence de l'opérateur Moov

## Notes Importantes

- Toutes les opérations terrain sont tracées avec coordonnées GPS et photos horodatées
- Les périodes de facturation s'étendent du 20 du mois en cours au 21 du mois suivant
- Chaque opérateur fournit ses propres modèles de rapports Excel et présentations PowerPoint
- L'application doit supporter un mode hors ligne pour l'usage terrain avec stockage temporaire local
- Le design responsive est critique : les appareils mobiles sont l'interface principale pour les équipes terrain
- Intégration IA prévue pour l'analyse des rapports, la détection d'anomalies et les suggestions automatiques
- **Fuseau horaire** : Africa/Abidjan (Côte d'Ivoire)
- **Langue** : Français (fr-fr) pour l'interface et les messages
- **Format de date** : YYYY-MM-DD (ISO 8601)
- **Fichiers uploadés** : Limite de 100 MB par fichier par défaut

## Architecture Frontend Quasar

### Structure du Projet Frontend

```
frontend/
├── src/
│   ├── boot/                    # Boot files Quasar (chargés au démarrage)
│   │   ├── axios.js            # Configuration Axios + intercepteurs JWT (302 lignes)
│   │   ├── i18n.js             # Configuration internationalisation
│   │   └── pinia.js            # Configuration store Pinia
│   │
│   ├── components/              # Composants Vue réutilisables
│   │   ├── common/             # Composants communs (Button, Card, Modal, etc.)
│   │   ├── forms/              # Composants de formulaires
│   │   └── layout/             # Composants de layout (Header, Sidebar, Footer)
│   │
│   ├── pages/                   # Pages Vue (routes)
│   │   ├── auth/               # Pages d'authentification (Login, Register)
│   │   ├── deployment/         # Pages de gestion des chantiers
│   │   ├── b2b/               # Pages B2B (raccordements, maintenances)
│   │   ├── inventory/          # Pages de gestion des stocks
│   │   ├── expenses/           # Pages de gestion des dépenses
│   │   └── mapping/            # Pages de cartographie et GPS
│   │
│   ├── layouts/                 # Layouts Vue
│   │   ├── MainLayout.vue      # Layout principal avec navigation
│   │   └── AuthLayout.vue      # Layout pour pages publiques
│   │
│   ├── stores/                  # Stores Pinia (gestion d'état)
│   │   ├── auth.js             # Store d'authentification
│   │   ├── user.js             # Store utilisateur
│   │   ├── deployment.js       # Store chantiers
│   │   ├── b2b.js             # Store B2B
│   │   ├── inventory.js        # Store stocks
│   │   ├── expenses.js         # Store dépenses
│   │   └── mapping.js          # Store cartographie
│   │
│   ├── router/                  # Configuration Vue Router
│   │   ├── index.js            # Routes principales
│   │   └── routes.js           # Définition des routes
│   │
│   ├── services/                # Services API
│   │   └── api.js              # Service API complet avec 80+ méthodes (550 lignes)
│   │
│   ├── utils/                   # Utilitaires
│   │   ├── constants.js        # Constantes de l'application (440 lignes)
│   │   └── storage.js          # Utilitaires de stockage local (76 lignes)
│   │
│   ├── css/                     # Système de design SCSS
│   │   ├── variables.scss      # Design tokens (couleurs, espacements, etc.)
│   │   ├── typography.scss     # Hiérarchie typographique
│   │   ├── animations.scss     # Transitions et keyframes
│   │   ├── app.scss           # Styles principaux et utilitaires
│   │   ├── quasar.variables.scss  # Variables Quasar (brand colors)
│   │   └── README.md           # Documentation complète du design system
│   │
│   ├── i18n/                    # Traductions
│   │   └── locales/
│   │       └── fr-FR.json      # Traduction française
│   │
│   ├── assets/                  # Assets statiques (images, icônes)
│   │
│   ├── App.vue                  # Composant racine Vue
│   └── index.template.html      # Template HTML
│
├── public/                      # Fichiers publics
│   ├── icons/                  # Icônes PWA (15 tailles)
│   └── favicon.ico
│
├── quasar.config.js            # Configuration Quasar
├── package.json                # Dépendances npm
└── .eslintrc.js               # Configuration ESLint
```

### Configuration Axios et Communication Backend

**Fichier : `src/boot/axios.js`**

Instance Axios configurée avec :
- Base URL dynamique : `http://localhost:8000/api` (dev) ou `process.env.API_URL` (prod)
- Timeout : 30 secondes
- Headers par défaut : `Content-Type: application/json`, `Accept: application/json`
- withCredentials : false (utilise JWT, pas de cookies)

**Intercepteurs configurés :**

1. **Request Interceptor** :
   - Ajoute automatiquement le token JWT dans `Authorization: Bearer ${token}`
   - Token récupéré depuis LocalStorage via `storage.getToken()`
   - Logging des requêtes en mode DEV

2. **Response Interceptor** :
   - **Succès** : Retourne la réponse directement
   - **Erreur 401** :
     - Vérifie si retry déjà tenté (flag `_retry`)
     - Récupère refresh token via `storage.getRefreshToken()`
     - Appelle `/token/refresh/` pour nouveau access token
     - Sauvegarde nouveau token via `storage.saveToken()`
     - Retente requête originale avec nouveau token
     - Si échec : déconnexion automatique via `handleLogout()`
   - **Autres erreurs (400, 403, 404, 422, 429, 500, 503)** :
     - Notifications Quasar appropriées pour l'utilisateur
   - **Erreurs réseau** : Notification "Erreur de connexion"

**Fichier : `src/services/api.js`**

Service API centralisé avec méthodes pour tous les modules :

**Modules disponibles :**
- `apiService.auth` : login, refresh, logout, register, profil, changePassword
- `apiService.deployment` : projects, tasks, operators, boq, progress, reports
- `apiService.b2b` : teams, studies, connections, maintenances, interventions
- `apiService.inventory` : materials, movements, allocations, returns, reports
- `apiService.expenses` : CRUD, categories, reports, approval
- `apiService.mapping` : locations, infrastructure, vehicles, gpsTracking
- `apiService.users` : CRUD, roles, permissions, activityLog

**Fonctions utilitaires :**
- `formatParams()` : Nettoyage des paramètres de requête
- `createFormData()` : Création de FormData pour uploads de fichiers
- `uploadFile()` : Upload générique de fichiers
- `downloadFile()` : Téléchargement automatique de fichiers
- `batchOperation()` : Opérations en lot (suppression, mise à jour multiple)

**Exemple d'utilisation :**
```javascript
import { apiService } from 'src/services/api'

// Authentification
const response = await apiService.auth.login({ username, password })
const { access, refresh, user } = response.data

// Récupérer des projets avec filtres
const projects = await apiService.deployment.projects.list({
  status: 'in_progress',
  page: 1
})

// Upload de photos pour une tâche
await apiService.deployment.tasks.uploadPhotos(taskId, filesArray)

// Télécharger un rapport Excel
await apiService.downloadFile(
  apiService.deployment.reports.exportExcel(projectId),
  'rapport.xlsx'
)
```

### Constantes et Configuration

**Fichier : `src/utils/constants.js`**

Centralise toutes les constantes de l'application :

**Configuration API :**
```javascript
export const API_BASE_URL // URL dynamique dev/prod
export const API_TIMEOUT = 30000 // 30 secondes
export const API_ENDPOINTS // Tous les endpoints organisés par module
```

**Clés de stockage local :**
```javascript
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
  THEME: 'theme',
  // ...
}
```

**Limites et contraintes :**
```javascript
export const FILE_UPLOAD_LIMITS = {
  MAX_SIZE: 10 * 1024 * 1024, // 10 MB
  MAX_SIZE_IMAGE: 5 * 1024 * 1024, // 5 MB
  // ...
}

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
}
```

**Statuts et états :**
```javascript
export const TASK_STATUS = {
  PENDING: 'pending',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  // ...
}

export const USER_ROLES = {
  SUPER_ADMIN: 'super_admin',
  ADMIN: 'admin',
  COORDINATOR: 'coordinator',
  // ...
}
```

**Configuration externe :**
```javascript
export const GOOGLE_MAPS = {
  API_KEY: process.env.GOOGLE_MAPS_API_KEY,
  DEFAULT_CENTER: { lat: 5.3599517, lng: -4.0082563 }, // Abidjan
  DEFAULT_ZOOM: 12
}

export const DATE_FORMATS = {
  DISPLAY: 'DD/MM/YYYY',
  API: 'YYYY-MM-DD',
  // ...
}
```

**Patterns de validation :**
```javascript
export const VALIDATION_PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE_CI: /^((\+225|00225)?[0-9]{10})$/, // Téléphone Côte d'Ivoire
  // ...
}
```

### Système de Design (SCSS)

**Documentation complète : `src/css/README.md`**

**Variables de design (`variables.scss`) :**
- Couleurs : primaire, secondaire, accent, fonctionnelles, fonds
- Espacement : système basé sur 4dp (4px, 8px, 16px, 24px, 32px, 48px, 64px)
- Typographie : tailles de police, poids, hauteurs de ligne
- Animations : durées (150ms, 200ms, 300ms, 400ms), easings
- Borders & Shadows : rayons de bordure, ombres
- Z-index : layers de superposition
- Breakpoints responsive : xs (0), sm (600px), md (960px), lg (1280px), xl (1920px)

**Hiérarchie typographique (`typography.scss`) :**
- H1 : 28px / Bold (700)
- H2 : 24px / Bold (700)
- H3 : 20px / Semi-bold (600)
- H4 : 18px / Semi-bold (600)
- Body Large : 17px / Regular (400)
- Body : 15px / Regular (400)
- Small : 13px / Regular (400)
- Caption : 12px / Regular (400)

**Animations (`animations.scss`) :**
- Keyframes : fade, slide, scale, rotation, bounce, shake, shimmer
- Transitions : standard (200ms), accent (300ms), micro (150ms)
- États interactifs : hover-elevate, hover-scale, hover-glow
- Transitions de page Vue Router : fade, slide, scale

**Utilitaires (`app.scss`) :**
- Spacing : m-*, p-*, mx-*, my-*, mt-*, mb-*, ml-*, mr-*
- Display : d-flex, d-grid, d-none, d-block
- Flexbox : justify-*, align-*, flex-*
- Backgrounds : bg-white, bg-light, bg-primary, bg-accent
- Borders : border, rounded, rounded-lg, rounded-full
- Shadows : shadow-sm, shadow-md, shadow-lg
- Typography : text-left, text-center, text-uppercase, text-truncate

**Exemple d'utilisation dans les composants :**
```vue
<template>
  <div class="card-container mb-md p-base">
    <h2 class="text-h2 text-brand mb-sm">Titre de la carte</h2>
    <p class="text-body text-secondary mb-base">Description...</p>
    <q-btn
      class="btn btn-primary hover-elevate"
      label="Action"
    />
  </div>
</template>
```

### Gestion d'État avec Pinia

**Convention de nommage des stores :**
- Fichiers dans `src/stores/` : `auth.js`, `user.js`, `deployment.js`, etc.
- Nom du store : `useAuthStore`, `useUserStore`, `useDeploymentStore`

**Structure type d'un store :**
```javascript
import { defineStore } from 'pinia'
import { apiService } from 'src/services/api'
import { storage } from 'src/utils/storage'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: storage.getToken() || null,
    refreshToken: storage.getRefreshToken() || null,
    user: storage.getUser() || null,
    isAuthenticated: !!storage.getToken()
  }),

  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    currentUser: (state) => state.user
  },

  actions: {
    async login(credentials) {
      const response = await apiService.auth.login(credentials)
      const { access, refresh, user } = response.data

      this.token = access
      this.refreshToken = refresh
      this.user = user
      this.isAuthenticated = true

      storage.saveToken(access)
      storage.saveRefreshToken(refresh)
      storage.saveUser(user)
    },

    logout() {
      this.token = null
      this.refreshToken = null
      this.user = null
      this.isAuthenticated = false

      storage.clear()
    }
  }
})
```

**Utilisation dans les composants :**
```vue
<script setup>
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()

const handleLogin = async () => {
  try {
    await authStore.login({ username, password })
    router.push('/dashboard')
  } catch (error) {
    // Erreur gérée par l'intercepteur Axios
  }
}
</script>
```

### Router et Guards d'Authentification

**Configuration recommandée (`src/router/index.js`) :**
```javascript
import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'src/stores/auth'

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  // Guard d'authentification
  Router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

    if (requiresAuth && !authStore.isLoggedIn) {
      next('/login')
    } else if (to.path === '/login' && authStore.isLoggedIn) {
      next('/dashboard')
    } else {
      next()
    }
  })

  return Router
})
```

**Définition des routes (`src/router/routes.js`) :**
```javascript
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', component: () => import('pages/DashboardPage.vue') },
      { path: 'deployment', component: () => import('pages/deployment/ProjectsPage.vue') },
      // ... autres routes protégées
    ]
  },
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      { path: 'login', component: () => import('pages/auth/LoginPage.vue') },
      { path: 'register', component: () => import('pages/auth/RegisterPage.vue') }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
```

### PWA Configuration

**Workbox configuré dans `quasar.config.js` :**

Stratégies de cache :
1. **Google Fonts** : CacheFirst (1 an)
2. **Images** : CacheFirst (30 jours)
3. **API** : NetworkFirst (5 minutes de cache)

Mode hors ligne supporté avec :
- Cache des assets essentiels (HTML, CSS, JS, icônes)
- Synchronisation en arrière-plan des données modifiées hors ligne
- Notifications de mise à jour de l'application

### Tests et Validation Frontend

**ESLint configuré** :
- Configuration dans `.eslintrc.js`
- Commande : `npm run lint`

**Tests recommandés** :
- Unit tests : Vitest (à configurer)
- E2E tests : Cypress (à configurer)
- Component tests : @vue/test-utils + Vitest

### Bonnes Pratiques Frontend

1. **Composition API** : Utiliser la Composition API de Vue 3 pour tous les nouveaux composants
2. **Stores Pinia** : Un store par module métier
3. **Services API** : Toujours utiliser `apiService` au lieu d'appeler `api` directement
4. **Constantes** : Centraliser toutes les constantes dans `constants.js`
5. **Typage** : Utiliser JSDoc pour documenter les fonctions et paramètres
6. **Responsive** : Mobile-first, tester sur différentes tailles d'écran
7. **Performance** : Lazy loading des routes et composants volumineux
8. **Accessibilité** : Respecter les standards WCAG (labels, aria-*, contraste)
9. **Mode hors ligne** : Gérer gracieusement les erreurs réseau
10. **Notifications** : Utiliser Quasar Notify pour tous les feedbacks utilisateur

### Commandes Frontend Utiles

```bash
# Installation des dépendances
npm install

# Développement avec hot-reload
quasar dev
# ou
npm run dev

# Build de production
quasar build
# ou
npm run build

# Linter
npm run lint

# Formater le code
npm run format

# Ajouter un mode Quasar (PWA, Capacitor, Electron)
quasar mode add pwa

# Analyser le bundle de production
quasar build --analyze

# Build en mode debug
quasar build --debug
```

### URLs Frontend Importantes

- Dev Server : `http://localhost:8080` (configuré dans session actuelle)
- Backend API : `http://localhost:8000`
- Build output : `frontend/dist/spa/`
- PWA Service Worker : `frontend/src-pwa/`
- Configuration : `frontend/quasar.config.js`
- Design System docs : `frontend/src/css/README.md`

---

## État Actuel du Frontend (Phase 2 Complétée)

### Stores Pinia Créés

**`src/stores/auth.js`** - Store d'authentification (100% fonctionnel)
- **State** :
  - `token` : Access token JWT
  - `refreshToken` : Refresh token JWT
  - `user` : Objet utilisateur complet
  - `isAuthenticated` : Statut de connexion
- **Getters** :
  - `isLoggedIn` : Retourne true si authentifié
  - `hasAdminRights` : Vérifie si l'utilisateur est SUPERADMIN ou ADMIN
  - `userRole` : Retourne le rôle formaté (ex: "Super Administrateur")
  - `userFullName` : Retourne "Prénom NOM"
- **Actions** :
  - `login(credentials)` : Connexion avec username/password
  - `logout()` : Déconnexion et nettoyage
  - `refreshToken()` : Rafraîchissement du token JWT
  - `fetchCurrentUser()` : Récupère les données utilisateur actuelles
  - `updateUserProfile(profileData)` : Met à jour le profil
  - `initialize()` : Initialise le store au démarrage
- **Persistence** : Sauvegarde automatique dans LocalStorage via `storage.js`

### Pages Créées

**Pages d'authentification**
- **`src/pages/auth/LoginPage.vue`** (584 lignes)
  - Formulaire de connexion avec validation
  - Champs : username (min 3 car), password (min 4 car)
  - Gestion des erreurs avec messages contextuels (401, 403, 429, 500, etc.)
  - Toggle affichage mot de passe
  - Bouton "Mot de passe oublié" (placeholder)
  - Logo AI Venture intégré
  - Design responsive avec animations
  - Auto-redirection si déjà connecté

**Pages protégées**
- **`src/pages/DashboardPage.vue`**
  - Page d'accueil après connexion
  - Placeholder pour le tableau de bord

- **`src/pages/ProfilePage.vue`**
  - Page de profil utilisateur
  - Placeholder pour les informations du profil

- **`src/pages/ErrorNotFound.vue`**
  - Page 404 avec design personnalisé
  - Bouton retour à l'accueil

### Layouts Créés

**`src/layouts/AuthLayout.vue`**
- Layout minimaliste pour pages publiques (login, register)
- Pas de navigation
- Fond avec gradient
- Contenu centré

**`src/layouts/MainLayout.vue`** (660 lignes) - Layout principal de l'application
- **Header** (QHeader) :
  - Logo "SUPERVISOR V2.0"
  - Bouton hamburger pour mobile
  - Icône sync avec badge (données en attente)
  - Icône notifications avec badge (notifications non lues)
  - Menu utilisateur dropdown :
    - Avatar avec initiales
    - Nom complet + rôle
    - "Mon Profil" → `/profile`
    - "Paramètres" → `/settings` (visible seulement si admin)
    - "Aide" → Dialog d'aide
    - "Se déconnecter" → Logout

- **Drawer** (QDrawer - Navigation latérale) :
  - Header avec "AI Venture" et "Gestion des chantiers"
  - Menu de navigation :
    - Tableau de Bord (actif)
    - Chantiers (expansion item avec sous-menus, désactivé)
    - B2B (expansion item, désactivé)
    - Stocks (désactivé)
    - Dépenses (désactivé)
    - Cartographie (désactivé)
  - Highlight du module actif
  - Width : 260px
  - `show-if-above` : Toujours visible sur desktop

- **Dialog Notifications** :
  - Liste des notifications avec icônes et couleurs par type
  - Clic sur notification pour marquer comme lue
  - Filtrage automatique des notifications non lues

- **Responsive** :
  - Desktop : Sidebar fixe + header
  - Tablet : Sidebar collapsible
  - Mobile : Drawer avec hamburger menu

### Router Configuration

**`src/router/index.js`**
- Configuration complète avec navigation guards
- **beforeEach** guard :
  - Vérifie l'authentification via `authStore.isLoggedIn`
  - Redirige vers `/auth/login` si non authentifié
  - Redirige vers `/dashboard` si déjà connecté et accès à `/login`
  - Vérifie tous les `to.matched` pour `requiresAuth`

**`src/router/routes.js`**
- **Routes publiques** (`requiresAuth: false`) :
  - `/auth/login` → LoginPage.vue (AuthLayout)
  - `/login` → Alias vers `/auth/login`
  - `/:catchAll(.*)` → ErrorNotFound.vue (404)

- **Routes protégées** (`requiresAuth: true`) :
  - `/` → Redirect vers `/dashboard` (MainLayout)
  - `/dashboard` → DashboardPage.vue
  - `/profile` → ProfilePage.vue

- **Routes futures** (commentées) :
  - `/users` - Gestion des utilisateurs
  - `/deployment` - Gestion des chantiers
  - `/b2b` - Raccordements B2B
  - `/inventory` - Gestion des stocks
  - `/expenses` - Gestion des dépenses
  - `/mapping` - Cartographie

### Corrections et Optimisations Appliquées

**ESLint** :
- ✅ Aucune erreur ESLint
- Imports non utilisés supprimés (`useRoute` dans MainLayout)
- Try/catch inutiles retirés (auth.js)
- Paramètres non utilisés supprimés

**SCSS** :
- ✅ Aucun warning SCSS
- Migration de `darken()` et `lighten()` vers `color.adjust()`
- Ajout de `@use 'sass:color'` dans tous les fichiers SCSS
- Conformité avec Sass moderne

**Bugs critiques résolus** :
- ✅ Boucle de redirection infinie corrigée
  - Ajout de `meta: { requiresAuth: false }` aux routes parentes
- ✅ Asset loading avec Vite
  - Import des assets : `import logo from 'src/assets/aiventure.jpg'`
  - Binding dynamique : `:src="logo"`

**Performance** :
- Hot-reload fonctionnel
- Temps de build : ~14.8s
- Aucune erreur console
- Navigation fluide

---

## Prochaines Étapes : Phase 3 - Module Deployment

La Phase 2 (Utilisateurs et Authentification) est **100% complétée**. Le système d'authentification est pleinement fonctionnel end-to-end :
- Backend API REST avec JWT
- Frontend avec login, guards, layouts
- Refresh automatique des tokens
- Gestion complète des erreurs

**Prochaine phase** : Créer le module Deployment pour la gestion des chantiers (voir PROJECT_STATE.md pour le plan détaillé).
