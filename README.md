# SUPERVISOR V2.0

Application web de gestion des opérations terrain pour AI Venture - Projets de déploiement de réseaux fibre optique, raccordements B2B, maintenance et gestion des équipements.

## 📋 Vue d'ensemble

SUPERVISOR V2.0 est une plateforme complète de gestion qui centralise :
- Gestion des chantiers de déploiement (backbone, transport, distribution)
- Suivi des raccordements et maintenances B2B
- Gestion des stocks de matériels et équipements
- Suivi des dépenses et facturation
- Cartographie et tracking GPS des véhicules
- Reporting terrain avec photos géolocalisées
- Analyse et génération de rapports assistés par IA

## 🏗️ Structure du Projet

```
monapp/
├── .git/                       # Dépôt Git
├── .gitignore                  # Règles d'exclusion Git
├── CLAUDE.md                   # Guide pour Claude Code
├── PROJECT_STATE.md            # État d'avancement du projet
├── README.md                   # Ce fichier
├── instructions.md             # Règles de développement
│
├── supervisor_doc/             # Documentation du projet
│   ├── supervisor_presentation.md      # Spécifications fonctionnelles
│   ├── supervisor_design_patern.md     # Design system et UI/UX
│   ├── travaux_orange.xlsx             # BOQ opérateur Orange
│   └── travaux_moov.xlsx               # BOQ opérateur Moov
│
└── supervisor/                 # Code source de l'application
    ├── backend/                # Backend Django
    │   ├── .venv/             # Environnement virtuel Python 3.12.7
    │   ├── apps/              # Applications Django modulaires
    │   ├── config/            # Configuration Django
    │   ├── media/             # Fichiers uploadés
    │   ├── static/            # Fichiers statiques
    │   └── README.md          # Documentation backend
    │
    └── frontend/               # Frontend Quasar (Vue.js)
        └── (à initialiser)
```

## 🛠️ Technologies

### Backend
- **Python** 3.12.7
- **Django** 4.2.16
- **Django REST Framework**
- **MySQL** (via WAMP Server)
- **Pillow** (traitement d'images)

### Frontend
- **Quasar Framework** (Vue.js)
- **Google Maps API** (cartographie)
- **Design responsive** mobile-first

### Intégrations
- WhatsGPS API (tracking véhicules)
- WhatsApp (notifications)
- OCR et IA pour analyse de documents

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.12.7
- MySQL (WAMP Server)
- Node.js et npm
- Git

### Installation Backend

```bash
# Se placer dans le dossier backend
cd supervisor/backend

# Activer l'environnement virtuel
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Installer les dépendances (une fois Django installé)
pip install -r requirements.txt

# Lancer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Démarrer le serveur de développement
python manage.py runserver
```

### Installation Frontend

```bash
# Se placer dans le dossier frontend
cd supervisor/frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement Quasar
quasar dev
```

## 📖 Documentation

- **CLAUDE.md** : Guide complet pour les développeurs et instances Claude Code
- **PROJECT_STATE.md** : Suivi en temps réel de l'avancement du projet
- **instructions.md** : Règles et méthodologie de développement strictes
- **supervisor_doc/** : Spécifications fonctionnelles et design system

## 🎯 État du Projet

**Phase actuelle** : Initialisation (40%)

### Complété ✅
- Documentation de base
- Structure des répertoires
- Environnement virtuel Python
- Initialisation Git et .gitignore

### En cours 🔄
- Installation de Django et dépendances
- Création du projet Django
- Configuration de la base de données

### À venir 📋
- Modélisation de la base de données
- Création des applications Django
- Configuration de l'API REST
- Initialisation du frontend Quasar

Consulter **PROJECT_STATE.md** pour les détails complets.

## 🔒 Règles de Développement

⚠️ **IMPORTANT** : Ce projet suit une méthodologie stricte définie dans `instructions.md`

1. **JAMAIS improviser** - Suivre uniquement les spécifications
2. **JAMAIS sauter d'étape** - Valider avant de continuer
3. **TOUJOURS documenter** - Commenter et expliquer
4. **TOUJOURS demander confirmation** - Clarifier les ambiguïtés
5. **JAMAIS inventer de fonctionnalités** - Créer uniquement ce qui est demandé

## 👥 Équipe

**Client** : AI Venture (AIV)
**Secteur** : Télécommunications - Déploiement fibre optique
**Langue du projet** : Français

## 📝 Licence

Propriété de AI Venture - Usage interne uniquement

---

**Dernière mise à jour** : 2025-11-11
**Version** : 0.1.0 (Phase d'initialisation)
