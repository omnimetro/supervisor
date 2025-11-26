# Installation du Backend SUPERVISOR V2.0

Guide d'installation des dépendances Python pour le backend Django.

## Prérequis

- Python 3.12.7 installé
- MySQL Server (via WAMP ou installation standalone)
- Git
- Tesseract OCR (pour l'OCR des documents)

## 📦 Fichiers de Dépendances

Le projet utilise trois fichiers de dépendances :

- **requirements.txt** : Dépendances de base (obligatoires)
- **requirements-dev.txt** : Dépendances de développement (debug, tests, linting)
- **requirements-prod.txt** : Dépendances de production (serveurs, monitoring)

## 🚀 Installation

### 1. Activer l'environnement virtuel

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

### 2. Mettre à jour pip

```bash
python -m pip install --upgrade pip
```

### 3. Installer les dépendances

**Pour le développement (recommandé) :**
```bash
pip install -r requirements-dev.txt
```

**Pour la production :**
```bash
pip install -r requirements-prod.txt
```

**Installation de base uniquement :**
```bash
pip install -r requirements.txt
```

## 🔧 Configuration des Dépendances Spéciales

### mysqlclient (Connecteur MySQL)

**Windows :**
Si l'installation échoue, vous avez deux options :

1. Installer via wheel pré-compilé :
   ```bash
   pip install mysqlclient-<version>-cp312-cp312-win_amd64.whl
   ```

2. Utiliser PyMySQL comme alternative :
   ```bash
   pip uninstall mysqlclient
   pip install PyMySQL
   ```
   Puis dans `config/settings.py` :
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

**Linux :**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

### Tesseract OCR

**Windows :**
1. Télécharger depuis : https://github.com/UB-Mannheim/tesseract/wiki
2. Installer et ajouter au PATH
3. Vérifier : `tesseract --version`

**Linux :**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-fra
```

### python-magic (Détection type MIME)

**Windows :**
```bash
pip install python-magic-bin
```

**Linux/Mac :**
```bash
pip install python-magic
```

### WeasyPrint (Génération PDF)

**Windows :**
1. Installer GTK3 : https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
2. Puis : `pip install WeasyPrint`

**Linux :**
```bash
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
pip install WeasyPrint
```

## 📋 Vérification de l'Installation

```bash
# Lister les packages installés
pip list

# Vérifier les versions
python -c "import django; print(django.get_version())"
python -c "import rest_framework; print(rest_framework.__version__)"
python -c "import PIL; print(PIL.__version__)"

# Vérifier la connexion MySQL
python -c "import MySQLdb; print('MySQL OK')"
```

## 🔄 Mise à jour des Dépendances

```bash
# Mettre à jour toutes les dépendances
pip install --upgrade -r requirements-dev.txt

# Mettre à jour une dépendance spécifique
pip install --upgrade Django

# Générer un nouveau requirements.txt avec versions exactes
pip freeze > requirements-freeze.txt
```

## 🐛 Dépannage

### Erreur : "Microsoft Visual C++ 14.0 is required"

**Solution Windows :**
1. Installer Visual Studio Build Tools
2. Ou installer le package via wheel pré-compilé

### Erreur : "mysqlclient installation fails"

**Solutions :**
1. Vérifier que MySQL est installé
2. Installer les en-têtes MySQL développement
3. Utiliser PyMySQL comme alternative

### Erreur : "ModuleNotFoundError"

**Solution :**
```bash
# Vérifier que l'environnement virtuel est activé
which python  # Linux/Mac
where python  # Windows

# Réinstaller les dépendances
pip install -r requirements-dev.txt --force-reinstall
```

## 📦 Packages Principaux et leur Usage

| Package | Version | Usage |
|---------|---------|-------|
| Django | 4.2.16 | Framework web principal |
| djangorestframework | 3.14.0 | API REST |
| mysqlclient | 2.2.4 | Connecteur base de données |
| Pillow | 10.2.0 | Traitement images |
| openpyxl | 3.1.2 | Génération Excel |
| python-docx | 1.1.0 | Génération Word |
| python-pptx | 0.6.23 | Génération PowerPoint |
| reportlab | 4.0.9 | Génération PDF |
| celery | 5.3.4 | Tâches asynchrones |
| djangorestframework-simplejwt | 5.3.1 | Authentification JWT |

## 🔐 Sécurité

Avant de déployer en production :

1. Scanner les vulnérabilités :
   ```bash
   safety check
   bandit -r apps/
   ```

2. Mettre à jour les packages avec CVE connus :
   ```bash
   pip-audit
   ```

## 📚 Documentation

Pour plus d'informations sur les packages :
- Django : https://docs.djangoproject.com/
- DRF : https://www.django-rest-framework.org/
- Celery : https://docs.celeryq.dev/

---

**Dernière mise à jour** : 2025-11-11
