# Structure des Routes API - SUPERVISOR V2.0

Documentation complète de la structure des URLs de l'API REST

---

## 📍 Routes Principales

### Vue Racine

```
GET /
GET /api/
```

**Description** : Point d'entrée de l'API, retourne la liste des endpoints disponibles

**Authentification** : Non requise

**Réponse** :
```json
{
  "message": "Bienvenue sur l'API SUPERVISOR V2.0",
  "version": "2.0",
  "endpoints": {
    "admin": "/admin/",
    "auth": {
      "token_obtain": "/api/token/",
      "token_refresh": "/api/token/refresh/",
      "token_verify": "/api/token/verify/"
    },
    "documentation": "/api/docs/"
  }
}
```

---

## 🔐 Authentification JWT

### Obtenir un Token (Login)

```
POST /api/token/
```

**Description** : Obtenir un access token et un refresh token

**Authentification** : Non requise

**Corps de la requête** :
```json
{
  "username": "utilisateur",
  "password": "motdepasse"
}
```

**Réponse** :
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Durée de vie** :
- Access token : 2 heures (configurable via JWT_ACCESS_TOKEN_LIFETIME_HOURS)
- Refresh token : 7 jours (configurable via JWT_REFRESH_TOKEN_LIFETIME_DAYS)

---

### Rafraîchir un Token

```
POST /api/token/refresh/
```

**Description** : Obtenir un nouveau access token avec un refresh token

**Authentification** : Non requise (utilise le refresh token)

**Corps de la requête** :
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Réponse** :
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."  // Nouveau refresh token si rotation activée
}
```

---

### Vérifier un Token

```
POST /api/token/verify/
```

**Description** : Vérifier la validité d'un token

**Authentification** : Non requise

**Corps de la requête** :
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Réponse** :
```json
{}  // 200 OK si valide, 401 si invalide
```

---

## 📚 Documentation de l'API

### Swagger UI (Interface Interactive)

```
GET /api/docs/
```

**Description** : Interface interactive Swagger pour explorer et tester l'API

**Fonctionnalités** :
- Liste de tous les endpoints
- Schémas de requête/réponse
- Tester les endpoints directement dans le navigateur
- Authentification JWT intégrée

**Accès** : http://localhost:8000/api/docs/

---

### ReDoc (Documentation Alternative)

```
GET /api/redoc/
```

**Description** : Documentation API en format ReDoc (lecture seule, design épuré)

**Accès** : http://localhost:8000/api/redoc/

---

### Schema JSON

```
GET /api/schema/
```

**Description** : Schéma OpenAPI au format JSON

**Utilisation** : Pour générer des clients API automatiquement

---

## 👥 Gestion des Utilisateurs

```
/api/users/
```

**Routes (à implémenter)** :
- `GET /api/users/` - Liste des utilisateurs
- `POST /api/users/` - Créer un utilisateur
- `GET /api/users/{id}/` - Détails d'un utilisateur
- `PUT /api/users/{id}/` - Modifier un utilisateur
- `PATCH /api/users/{id}/` - Modification partielle
- `DELETE /api/users/{id}/` - Supprimer un utilisateur
- `GET /api/users/me/` - Profil de l'utilisateur connecté
- `PUT /api/users/me/password/` - Changer le mot de passe

**Authentification** : JWT Bearer Token requis

---

## 🏗️ Gestion des Chantiers (Deployment)

```
/api/deployment/
```

**Modules** :
- `/api/deployment/sites/` - Gestion des chantiers
- `/api/deployment/operators/` - Gestion des opérateurs
- `/api/deployment/boq/` - Bordereaux de quantité (BOQ)
- `/api/deployment/tasks/` - Gestion des tâches
- `/api/deployment/planning/` - Plannings prévisionnels
- `/api/deployment/reporting/` - Rapports quotidiens
- `/api/deployment/cartography/` - Fiches cartographie
- `/api/deployment/deliveries/` - Phase de livraison

**Authentification** : JWT Bearer Token requis

---

## 🏢 Gestion B2B (Raccordements & Maintenance)

```
/api/b2b/
```

**Modules** :
- `/api/b2b/clients/` - Dossiers clients
- `/api/b2b/teams/` - Équipes B2B
- `/api/b2b/zones/` - Zones géographiques
- `/api/b2b/study-reports/` - Rapports d'étude
- `/api/b2b/installation-reports/` - Rapports d'installation
- `/api/b2b/maintenance/` - Maintenances

**Authentification** : JWT Bearer Token requis

---

## 📦 Gestion des Stocks (Inventory)

```
/api/inventory/
```

**Modules** :
- `/api/inventory/materials/` - Matériels et équipements
- `/api/inventory/movements/` - Mouvements de stock
- `/api/inventory/categories/` - Catégories de matériels
- `/api/inventory/warehouses/` - Entrepôts
- `/api/inventory/reports/` - Rapports de stock

**Types de mouvements** :
- Inventaire
- Acquisition
- Affectation
- Récupération
- Enlèvement
- Retour matériel
- Indisponibilité
- Intégration
- Retrait de stock

**Authentification** : JWT Bearer Token requis

---

## 💰 Gestion des Dépenses (Expenses)

```
/api/expenses/
```

**Modules** :
- `/api/expenses/records/` - Fiches de dépenses
- `/api/expenses/categories/` - Catégories de dépenses
- `/api/expenses/reports/` - Rapports de dépenses
- `/api/expenses/budgets/` - Budgets

**Types de dépenses** :
- Achat
- Location
- Prestation
- Main d'œuvre
- Communication
- Carburant
- Per diem

**Authentification** : JWT Bearer Token requis

---

## 🗺️ Cartographie et Tracking GPS (Mapping)

```
/api/mapping/
```

**Modules** :
- `/api/mapping/locations/` - Points GPS
- `/api/mapping/vehicles/` - Véhicules
- `/api/mapping/tracking/` - Suivi en temps réel
- `/api/mapping/zones/` - Zones de travail
- `/api/mapping/kmz/` - Import/Export KMZ

**Intégrations** :
- Google Maps API
- WhatsGPS API (véhicules avec traceur)
- Application mobile tracking (véhicules sans traceur)

**Authentification** : JWT Bearer Token requis

---

## 🛡️ Administration Django

```
GET /admin/
```

**Description** : Interface d'administration Django

**Accès** : Réservé aux administrateurs (superuser)

**Fonctionnalités** :
- Gestion complète des modèles
- Visualisation des données
- Actions en masse
- Logs d'actions

**Authentification** : Session Django (username/password)

---

## 🔧 Configuration pour le Développement

### Fichiers Media (Uploads)

```
GET /media/{path}
```

**Description** : Servir les fichiers uploadés en développement

**Note** : En production, utilisez nginx ou un CDN

**Disponible uniquement si** : `DEBUG = True`

---

### Fichiers Static

```
GET /static/{path}
```

**Description** : Servir les fichiers statiques en développement

**Note** : En production, utilisez WhiteNoise ou nginx

**Disponible uniquement si** : `DEBUG = True`

---

### Django Debug Toolbar

```
GET /__debug__/
```

**Description** : Interface de debugging Django

**Disponible uniquement si** :
- `DEBUG = True`
- `django-debug-toolbar` installé

---

## 📝 Utilisation des Tokens JWT

### Dans les Headers

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Exemple avec curl

```bash
# Obtenir un token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Utiliser le token
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Exemple avec JavaScript (Fetch)

```javascript
// Login
const response = await fetch('http://localhost:8000/api/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'admin',
    password: 'password',
  }),
});

const { access, refresh } = await response.json();

// Utiliser le token
const usersResponse = await fetch('http://localhost:8000/api/users/', {
  headers: {
    'Authorization': `Bearer ${access}`,
  },
});

const users = await usersResponse.json();
```

---

## 🔄 Pagination

Toutes les listes utilisent la pagination par défaut :

```
GET /api/users/?page=2
```

**Paramètres** :
- `page` : Numéro de page (défaut: 1)
- `page_size` : Nombre d'éléments par page (défaut: 50)

**Réponse** :
```json
{
  "count": 250,
  "next": "http://localhost:8000/api/users/?page=3",
  "previous": "http://localhost:8000/api/users/?page=1",
  "results": [...]
}
```

---

## 🔍 Filtres et Recherche

### Filtres

```
GET /api/users/?role=supervisor&is_active=true
```

### Recherche

```
GET /api/users/?search=john
```

### Tri

```
GET /api/users/?ordering=-created_at
GET /api/users/?ordering=username
```

**Note** : `-` pour ordre décroissant

---

## ⚠️ Codes de Statut HTTP

| Code | Description |
|------|-------------|
| 200 | OK - Succès |
| 201 | Created - Ressource créée |
| 204 | No Content - Suppression réussie |
| 400 | Bad Request - Données invalides |
| 401 | Unauthorized - Authentification requise |
| 403 | Forbidden - Permissions insuffisantes |
| 404 | Not Found - Ressource introuvable |
| 500 | Internal Server Error - Erreur serveur |

---

## 📖 Documentation Complète

Pour explorer l'API de manière interactive :

**En développement :**
- Swagger UI : http://localhost:8000/api/docs/
- ReDoc : http://localhost:8000/api/redoc/

**En production :**
- Remplacer `localhost:8000` par le domaine de production

---

**Dernière mise à jour** : 2025-11-11
**Version de l'API** : 2.0
