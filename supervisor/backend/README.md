# Backend SUPERVISOR V2.0

Backend Django pour l'application SUPERVISOR V2.0

## Structure du Projet

```
backend/
├── .venv/                    # Environnement virtuel Python 3.12.7
├── apps/                     # Applications Django modulaires
│   ├── deployment/           # Gestion des chantiers (à créer)
│   ├── b2b/                 # Gestion B2B (à créer)
│   ├── inventory/           # Gestion des stocks (à créer)
│   ├── expenses/            # Gestion des dépenses (à créer)
│   ├── users/               # Gestion des utilisateurs (à créer)
│   └── mapping/             # Gestion de la cartographie (à créer)
├── config/                  # Configuration Django (settings, urls, wsgi)
├── media/                   # Fichiers uploadés (photos, documents)
├── static/                  # Fichiers statiques (CSS, JS, images)
├── requirements.txt         # Dépendances de base
├── requirements-dev.txt     # Dépendances de développement
├── requirements-prod.txt    # Dépendances de production
├── INSTALLATION.md          # Guide d'installation détaillé
└── README.md                # Ce fichier
```

## Activation de l'Environnement Virtuel

### Windows
```bash
.venv\Scripts\activate
```

### Linux/Mac
```bash
source .venv/bin/activate
```

## Installation des Dépendances

### Installation pour le développement (recommandé)
```bash
pip install -r requirements-dev.txt
```

### Installation pour la production
```bash
pip install -r requirements-prod.txt
```

### Installation de base uniquement
```bash
pip install -r requirements.txt
```

**Note :** Consulter `INSTALLATION.md` pour le guide détaillé et le dépannage.

## Prochaines Étapes

1. ✅ Fichiers de dépendances créés
2. ⏳ Installer les dépendances dans l'environnement virtuel
3. ⏳ Initialiser le projet Django dans le dossier `config/`
4. ⏳ Créer les applications Django dans le dossier `apps/`
5. ⏳ Configurer la connexion à MySQL
6. ⏳ Créer les modèles de données

## Technologies

- Python 3.12.7
- Django 4.2.16
- Django REST Framework
- MySQL
- Pillow (gestion des images)

## Documentation

Consulter `CLAUDE.md` et `PROJECT_STATE.md` à la racine du projet pour plus d'informations.
