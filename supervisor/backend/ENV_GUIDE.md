# Guide des Variables d'Environnement

Guide complet pour configurer le fichier `.env` de SUPERVISOR V2.0

## 📋 Installation

1. **Copier le fichier template :**
```bash
cp .env.example .env
```

2. **Éditer le fichier `.env` avec vos valeurs réelles**

⚠️ **IMPORTANT** : Le fichier `.env` contient des secrets et ne doit JAMAIS être commité dans Git !

---

## 🔧 Variables d'Environnement Détaillées

### Django Core

#### SECRET_KEY
```env
SECRET_KEY=your-secret-key-here-change-in-production
```
**Description** : Clé secrète utilisée pour la cryptographie dans Django

**Comment générer une clé sécurisée :**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Production** : DOIT être changée et gardée secrète

---

#### DEBUG
```env
DEBUG=True
```
**Description** : Active le mode debug de Django

**Valeurs possibles :**
- `True` : Mode développement (affiche les erreurs détaillées)
- `False` : Mode production (masque les erreurs sensibles)

**Production** : DOIT être `False`

---

#### ALLOWED_HOSTS
```env
ALLOWED_HOSTS=localhost,127.0.0.1,mondomaine.com
```
**Description** : Liste des hôtes/domaines autorisés à accéder à l'application

**Format** : Liste séparée par des virgules sans espaces

**Exemples :**
- Développement : `localhost,127.0.0.1`
- Production : `supervisor.aiventure.com,www.supervisor.aiventure.com,192.168.1.100`

---

### Base de Données MySQL

#### DB_NAME
```env
DB_NAME=supervisor_db
```
**Description** : Nom de la base de données MySQL

**Création de la base :**
```sql
CREATE DATABASE supervisor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

#### DB_USER
```env
DB_USER=root
```
**Description** : Utilisateur MySQL

**Production** : Créer un utilisateur dédié avec privilèges limités
```sql
CREATE USER 'supervisor_user'@'localhost' IDENTIFIED BY 'mot_de_passe_fort';
GRANT ALL PRIVILEGES ON supervisor_db.* TO 'supervisor_user'@'localhost';
FLUSH PRIVILEGES;
```

---

#### DB_PASSWORD
```env
DB_PASSWORD=votre_mot_de_passe_mysql
```
**Description** : Mot de passe de l'utilisateur MySQL

**Sécurité** : Utiliser un mot de passe fort en production (minimum 16 caractères, avec majuscules, minuscules, chiffres, symboles)

---

#### DB_HOST
```env
DB_HOST=localhost
```
**Description** : Hôte du serveur MySQL

**Valeurs possibles :**
- `localhost` : Serveur local
- `127.0.0.1` : IP locale
- `192.168.1.10` : Serveur sur le réseau local
- `mysql.example.com` : Serveur distant

---

#### DB_PORT
```env
DB_PORT=3306
```
**Description** : Port du serveur MySQL (3306 par défaut)

---

### JWT (Authentification)

#### JWT_ACCESS_TOKEN_LIFETIME_HOURS
```env
JWT_ACCESS_TOKEN_LIFETIME_HOURS=2
```
**Description** : Durée de vie du token d'accès en heures

**Recommandations :**
- Développement : 2-8 heures
- Production : 1-2 heures (pour plus de sécurité)

---

#### JWT_REFRESH_TOKEN_LIFETIME_DAYS
```env
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```
**Description** : Durée de vie du token de rafraîchissement en jours

**Recommandations :**
- Développement : 7-30 jours
- Production : 7-14 jours

---

#### JWT_ROTATE_REFRESH_TOKENS
```env
JWT_ROTATE_REFRESH_TOKENS=True
```
**Description** : Générer un nouveau refresh token à chaque utilisation

**Valeurs** : `True` ou `False`

**Production** : Recommandé `True` pour plus de sécurité

---

#### JWT_BLACKLIST_AFTER_ROTATION
```env
JWT_BLACKLIST_AFTER_ROTATION=True
```
**Description** : Invalider l'ancien refresh token après rotation

**Valeurs** : `True` ou `False`

**Production** : Recommandé `True`

---

### CORS (Frontend)

#### CORS_ALLOWED_ORIGINS
```env
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:9000
```
**Description** : Liste des origines autorisées pour les requêtes cross-origin

**Format** : Liste séparée par des virgules sans espaces

**Exemples :**
- Développement : `http://localhost:8080,http://localhost:9000`
- Production : `https://supervisor.aiventure.com,https://app.aiventure.com`

---

### Upload de Fichiers

#### DATA_UPLOAD_MAX_MEMORY_SIZE
```env
DATA_UPLOAD_MAX_MEMORY_SIZE=104857600
```
**Description** : Taille maximale des données uploadées en bytes

**Conversions utiles :**
- 10 MB = 10485760
- 50 MB = 52428800
- 100 MB = 104857600
- 500 MB = 524288000

---

#### FILE_UPLOAD_MAX_MEMORY_SIZE
```env
FILE_UPLOAD_MAX_MEMORY_SIZE=104857600
```
**Description** : Taille maximale d'un fichier uploadé en bytes

**Note** : Doit être cohérent avec `DATA_UPLOAD_MAX_MEMORY_SIZE`

---

#### ALLOWED_IMAGE_TYPES
```env
ALLOWED_IMAGE_TYPES=image/jpeg,image/jpg,image/png,image/gif
```
**Description** : Types MIME autorisés pour les images

**Types courants :**
- `image/jpeg` : JPEG
- `image/png` : PNG
- `image/gif` : GIF
- `image/webp` : WebP

---

#### ALLOWED_DOCUMENT_TYPES
```env
ALLOWED_DOCUMENT_TYPES=application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document
```
**Description** : Types MIME autorisés pour les documents

**Types courants :**
- `application/pdf` : PDF
- `application/msword` : Word (.doc)
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` : Word (.docx)
- `application/vnd.ms-excel` : Excel (.xls)
- `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` : Excel (.xlsx)

---

### Celery & Redis

#### CELERY_BROKER_URL
```env
CELERY_BROKER_URL=redis://localhost:6379/0
```
**Description** : URL du broker Celery (Redis)

**Format** : `redis://[host]:[port]/[db]`

**Exemples :**
- Local : `redis://localhost:6379/0`
- Avec auth : `redis://:password@localhost:6379/0`
- Distant : `redis://redis.example.com:6379/0`

---

#### CELERY_RESULT_BACKEND
```env
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```
**Description** : Backend pour stocker les résultats des tâches Celery

**Note** : Peut utiliser la même instance Redis que le broker ou une différente

---

### APIs Externes

#### GOOGLE_MAPS_API_KEY
```env
GOOGLE_MAPS_API_KEY=AIzaSyB1234567890abcdefghijklmnopqrstuv
```
**Description** : Clé API Google Maps

**Comment obtenir :**
1. Aller sur https://console.cloud.google.com/
2. Créer un projet
3. Activer Google Maps JavaScript API
4. Créer une clé API

**APIs nécessaires :**
- Maps JavaScript API
- Geocoding API
- Places API

---

#### TWILIO_ACCOUNT_SID
```env
TWILIO_ACCOUNT_SID=AC1234567890abcdefghijklmnopqrstuv
```
**Description** : Identifiant du compte Twilio (pour WhatsApp)

**Comment obtenir :**
1. Créer un compte sur https://www.twilio.com/
2. Accéder au Dashboard
3. Copier le Account SID

---

#### TWILIO_AUTH_TOKEN
```env
TWILIO_AUTH_TOKEN=1234567890abcdefghijklmnopqrstuv
```
**Description** : Token d'authentification Twilio

**Sécurité** : Ne JAMAIS exposer ce token publiquement

---

#### TWILIO_WHATSAPP_FROM
```env
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```
**Description** : Numéro WhatsApp Twilio (format E.164)

**Format** : `whatsapp:+[code_pays][numéro]`

---

#### WHATSGPS_API_KEY
```env
WHATSGPS_API_KEY=your-whatsgps-api-key
```
**Description** : Clé API WhatsGPS pour le tracking des véhicules

---

#### WHATSGPS_API_URL
```env
WHATSGPS_API_URL=https://api.whatsgps.com
```
**Description** : URL de l'API WhatsGPS

---

### Email (Optionnel)

#### EMAIL_BACKEND
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```
**Description** : Backend d'envoi d'emails

**Valeurs possibles :**
- `django.core.mail.backends.smtp.EmailBackend` : SMTP réel
- `django.core.mail.backends.console.EmailBackend` : Affichage en console (dev)
- `django.core.mail.backends.filebased.EmailBackend` : Sauvegarde dans fichiers

---

#### EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```
**Description** : Configuration du serveur SMTP

**Exemples de configurations :**

**Gmail :**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**Outlook/Office365 :**
```env
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

**SendGrid :**
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

---

#### EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
```env
EMAIL_HOST_USER=noreply@aiventure.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-email
```
**Description** : Identifiants du compte email

**Gmail** : Utiliser un "App Password" (pas le mot de passe du compte)

---

### Monitoring (Optionnel)

#### SENTRY_DSN
```env
SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
```
**Description** : DSN Sentry pour le monitoring des erreurs

**Comment obtenir :**
1. Créer un compte sur https://sentry.io/
2. Créer un projet Django
3. Copier le DSN

---

## 🔒 Bonnes Pratiques de Sécurité

1. **Ne jamais commiter le fichier `.env` dans Git**
   - Vérifier que `.env` est dans `.gitignore`

2. **Utiliser des valeurs différentes en production**
   - Générer une nouvelle SECRET_KEY
   - Utiliser des mots de passe forts
   - Changer tous les tokens/clés API

3. **Limiter les accès**
   - Créer des utilisateurs MySQL dédiés avec privilèges limités
   - Utiliser des sous-comptes API avec restrictions

4. **Sauvegarder les secrets en lieu sûr**
   - Utiliser un gestionnaire de mots de passe (1Password, LastPass, etc.)
   - Documenter les secrets dans un coffre-fort d'équipe

5. **Rotation régulière des secrets**
   - Changer les mots de passe tous les 3-6 mois
   - Régénérer les clés API périodiquement

---

## 🔍 Vérification de la Configuration

Après avoir configuré le fichier `.env`, tester avec :

```bash
# Activer l'environnement virtuel
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Vérifier la configuration Django
python manage.py check

# Tester la connexion à la base de données
python manage.py dbshell
```

---

## 🆘 Dépannage

### Erreur : "SECRET_KEY not found"
**Solution** : Créer le fichier `.env` à partir de `.env.example`

### Erreur : "Can't connect to MySQL"
**Solutions** :
1. Vérifier que MySQL est démarré (WAMP Server)
2. Vérifier DB_NAME, DB_USER, DB_PASSWORD
3. Tester la connexion manuellement : `mysql -u root -p`

### Erreur : "CORS error"
**Solution** : Ajouter l'origine du frontend dans CORS_ALLOWED_ORIGINS

---

**Dernière mise à jour** : 2025-11-11
