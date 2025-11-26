# Guide de Démarrage Rapide - SUPERVISOR V2.0

Guide pour configurer et lancer le projet en quelques étapes

---

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir :

- [x] Python 3.12.7 installé
- [x] MySQL installé et démarré (via WAMP Server ou installation standalone)
- [x] Git installé
- [ ] Redis installé (optionnel, pour Celery)

---

## 🚀 Installation en 7 Étapes

### 1. Activer l'Environnement Virtuel

**Windows :**
```bash
cd supervisor/backend
.venv\Scripts\activate
```

**Linux/Mac :**
```bash
cd supervisor/backend
source .venv/bin/activate
```

Vous devriez voir `(.venv)` apparaître dans votre terminal.

---

### 2. Mettre à Jour pip

```bash
python -m pip install --upgrade pip
```

---

### 3. Installer les Dépendances

**Pour le développement (recommandé) :**
```bash
pip install -r requirements-dev.txt
```

**Installation de base uniquement :**
```bash
pip install -r requirements.txt
```

⏱️ **Temps estimé :** 5-10 minutes

**Note :** Si l'installation de `mysqlclient` échoue sous Windows :
```bash
pip install pymysql
```
Puis dans `config/__init__.py`, ajouter avant les imports :
```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

### 4. Configurer le Fichier .env

Le fichier `.env` a déjà été créé avec des valeurs par défaut pour le développement.

**À faire :**
1. Ouvrir le fichier `.env`
2. Vérifier/Modifier les paramètres MySQL si nécessaire :
   ```env
   DB_NAME=supervisor_db
   DB_USER=root
   DB_PASSWORD=          # Votre mot de passe MySQL
   DB_HOST=localhost
   DB_PORT=3306
   ```

3. (Optionnel) Ajouter les clés API si disponibles :
   - `GOOGLE_MAPS_API_KEY`
   - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM`
   - `WHATSGPS_API_KEY`, `WHATSGPS_API_URL`

---

### 5. Créer la Base de Données MySQL

**Option A : Via MySQL CLI**
```bash
mysql -u root -p
```
```sql
CREATE DATABASE supervisor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

**Option B : Via phpMyAdmin (WAMP)**
1. Ouvrir phpMyAdmin : http://localhost/phpmyadmin
2. Créer une nouvelle base de données :
   - Nom : `supervisor_db`
   - Interclassement : `utf8mb4_unicode_ci`

---

### 6. Effectuer les Migrations Django

```bash
# Vérifier la configuration
python manage.py check

# Créer les migrations initiales
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

**Résultat attendu :**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

### 7. Créer un Superutilisateur

```bash
python manage.py createsuperuser
```

**Saisir :**
- Username : `admin` (ou votre choix)
- Email : `admin@aiventure.com` (ou votre email)
- Password : (minimum 8 caractères)

---

## 🎉 Lancer le Serveur de Développement

```bash
python manage.py runserver
```

**Résultat attendu :**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🔍 Vérifier l'Installation

### 1. Page d'Accueil de l'API
**URL :** http://localhost:8000/

**Réponse attendue :**
```json
{
  "message": "Bienvenue sur l'API SUPERVISOR V2.0",
  "version": "2.0",
  "endpoints": {
    "admin": "/admin/",
    "auth": {...},
    "documentation": "/api/docs/"
  }
}
```

---

### 2. Administration Django
**URL :** http://localhost:8000/admin/

**Connexion :** Utiliser le superutilisateur créé à l'étape 7

**Ce que vous devriez voir :**
- Interface d'administration Django
- "SUPERVISOR V2.0 - Administration" dans le header
- Modules : Users, Groups

---

### 3. Documentation API (Swagger)
**URL :** http://localhost:8000/api/docs/

**Ce que vous devriez voir :**
- Interface Swagger UI interactive
- Titre : "SUPERVISOR V2.0 API"
- Liste des endpoints disponibles
- Possibilité de tester les endpoints

---

### 4. Tester l'Authentification JWT

**Obtenir un token :**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "votre_mot_de_passe"}'
```

**Réponse attendue :**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 📊 Structure du Projet

```
supervisor/backend/
├── .env                    # ✅ Configuration locale (NE PAS COMMITER)
├── .env.example           # Template de configuration
├── manage.py              # Utilitaire CLI Django
├── config/                # Configuration Django
│   ├── settings.py       # Paramètres Django
│   ├── urls.py           # Routes de l'API
│   ├── wsgi.py           # WSGI
│   ├── asgi.py           # ASGI
│   └── celery.py         # Celery
├── apps/                  # Applications Django (à créer)
├── media/                 # Fichiers uploadés
├── static/                # Fichiers statiques
├── logs/                  # Logs de l'application
└── templates/             # Templates Django
```

---

## 🐛 Dépannage

### Erreur : "Can't connect to MySQL server"

**Solutions :**
1. Vérifier que MySQL est démarré (WAMP Server)
2. Vérifier les identifiants dans `.env`
3. Tester la connexion manuellement :
   ```bash
   mysql -u root -p
   ```

---

### Erreur : "ModuleNotFoundError: No module named..."

**Solution :**
1. Vérifier que l'environnement virtuel est activé
2. Réinstaller les dépendances :
   ```bash
   pip install -r requirements-dev.txt
   ```

---

### Erreur : "mysqlclient installation fails"

**Solution :**
1. Utiliser PyMySQL comme alternative :
   ```bash
   pip install pymysql
   ```
2. Voir les instructions à l'étape 3

---

### Erreur : "SECRET_KEY not found"

**Solution :**
Le fichier `.env` existe mais n'est peut-être pas lu correctement.
1. Vérifier que `.env` est à la racine de `backend/`
2. Vérifier qu'il n'y a pas d'espaces autour du `=`
3. Redémarrer le serveur

---

## 📚 Commandes Utiles

```bash
# Vérifier la configuration Django
python manage.py check

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver

# Lancer le serveur sur un port spécifique
python manage.py runserver 8080

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Ouvrir un shell Django interactif
python manage.py shell

# Collecter les fichiers statiques (production)
python manage.py collectstatic

# Créer une application Django
python manage.py startapp nom_app

# Afficher les migrations
python manage.py showmigrations

# Voir les requêtes SQL
python manage.py sqlmigrate app_name migration_name
```

---

## 🔄 Prochaines Étapes

Maintenant que le projet est configuré :

1. **Créer les applications Django** dans `apps/` :
   - `apps.users` - Gestion des utilisateurs
   - `apps.deployment` - Gestion des chantiers
   - `apps.b2b` - Gestion B2B
   - `apps.inventory` - Gestion des stocks
   - `apps.expenses` - Gestion des dépenses
   - `apps.mapping` - Cartographie et GPS

2. **Définir les modèles de données** pour chaque application

3. **Créer les serializers** (Django REST Framework)

4. **Créer les vues et viewsets** (API endpoints)

5. **Configurer les URLs** de chaque application

6. **Écrire les tests** unitaires et d'intégration

---

## 📖 Documentation Complète

- **ENV_GUIDE.md** - Guide des variables d'environnement
- **SETTINGS_OVERVIEW.md** - Vue d'ensemble de la configuration
- **API_ROUTES.md** - Documentation des routes API
- **INSTALLATION.md** - Guide d'installation détaillé

---

## 🆘 Besoin d'Aide ?

1. Consulter les fichiers de documentation
2. Vérifier les logs Django dans `logs/django.log`
3. Activer le mode DEBUG dans `.env` pour plus de détails
4. Utiliser le Django Debug Toolbar : http://localhost:8000/__debug__/

---

**Dernière mise à jour** : 2025-11-11
**Version** : 2.0
