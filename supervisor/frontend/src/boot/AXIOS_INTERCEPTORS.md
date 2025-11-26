# Documentation des Intercepteurs Axios - SUPERVISOR V2.0

Ce document explique le fonctionnement des intercepteurs Axios configurés pour la gestion automatique de l'authentification JWT.

## Vue d'ensemble

Le fichier `boot/axios.js` configure deux intercepteurs :

1. **Request Interceptor** : Ajoute automatiquement le token JWT dans les headers de toutes les requêtes
2. **Response Interceptor** : Gère les erreurs d'authentification et rafraîchit automatiquement le token expiré

## Architecture et Flux d'Authentification

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Flux d'Authentification JWT                       │
└─────────────────────────────────────────────────────────────────────┘

1. CONNEXION
   User → Login Form → authStore.login() → Backend /api/auth/login/
                                          ↓
                          { access, refresh, user }
                                          ↓
                          storage.saveToken(access)
                          storage.saveRefreshToken(refresh)

2. REQUÊTE API AVEC TOKEN
   Component → api.get('/users/') → Request Interceptor
                                   ↓
                      Ajoute: Authorization: Bearer {token}
                                   ↓
                            Backend Django → 200 OK
                                   ↓
                          Response renvoyée

3. TOKEN EXPIRÉ (Refresh Automatique)
   Component → api.get('/data/') → Request Interceptor
                                  ↓
                     Authorization: Bearer {expired_token}
                                  ↓
                          Backend Django → 401 Unauthorized
                                  ↓
                         Response Interceptor détecte 401
                                  ↓
                   Récupère refresh token depuis storage
                                  ↓
          POST /api/token/refresh/ { refresh: refreshToken }
                                  ↓
          Backend → { access, refresh } (nouveau refresh si rotation)
                                  ↓
              storage.saveToken(newAccessToken)
              storage.saveRefreshToken(newRefreshToken) // Si rotation
                                  ↓
         Retry requête originale avec nouveau access token
                                  ↓
                          Backend → 200 OK

4. REFRESH TOKEN EXPIRÉ (Déconnexion)
   Component → api.get('/data/') → 401 → Refresh échoue
                                        ↓
                               storage.clear()
                                        ↓
                          Notify: "Session expirée"
                                        ↓
                        Redirect → /login?redirect=/data
```

## Intercepteur de Requête (Request)

### Fonctionnement

```javascript
api.interceptors.request.use((config) => {
  const token = storage.getToken()

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})
```

### Caractéristiques

- **Automatique** : Toutes les requêtes passent par cet intercepteur
- **Non-bloquant** : Si pas de token, la requête est envoyée sans header Authorization
- **Indépendant du store** : Utilise directement `storage.getToken()` pour éviter les dépendances circulaires
- **Logging en DEV** : Affiche les détails des requêtes dans la console

### Pourquoi utiliser `storage` au lieu du `authStore` ?

```
authStore.login() → apiService.auth.login() → api.post()
                                              ↓
                                  Request Interceptor (besoin du token)
```

Si l'intercepteur importait `authStore`, cela créerait une **dépendance circulaire** :
- `authStore` importe `api` pour faire ses requêtes
- `api` (intercepteur) importerait `authStore` pour lire le token

**Solution** : L'intercepteur lit directement depuis `storage`, et le `authStore` écrit dans `storage`. Séparation claire des responsabilités.

## Intercepteur de Réponse (Response)

### Gestion des Codes HTTP

| Code | Description | Action |
|------|-------------|--------|
| **200-299** | Succès | Retourne la réponse directement |
| **400** | Bad Request | Notification "Requête invalide" |
| **401** | Unauthorized | **Tentative de refresh automatique** (voir ci-dessous) |
| **403** | Forbidden | Notification "Accès refusé" |
| **404** | Not Found | Notification "Ressource non trouvée" |
| **422** | Validation Error | Notification "Erreur de validation" |
| **429** | Too Many Requests | Notification "Trop de requêtes" |
| **500** | Server Error | Notification "Erreur serveur" |
| **503** | Service Unavailable | Notification "Service indisponible" |
| **Network Error** | Pas de réponse | Notification "Erreur de connexion" |

### Gestion Spéciale du Code 401 (Unauthorized)

Le code 401 déclenche un processus automatique de rafraîchissement du token :

#### Étape 1 : Détection de l'erreur 401

```javascript
if (error.response?.status === 401 && !originalRequest._retry) {
  originalRequest._retry = true // Marque pour éviter boucle infinie
  // ...
}
```

#### Étape 2 : Récupération du refresh token

```javascript
const refreshToken = storage.getRefreshToken()

if (!refreshToken) {
  // Pas de refresh token → Déconnexion immédiate
  handleLogout()
  return Promise.reject(error)
}
```

#### Étape 3 : Appel de l'endpoint de refresh

```javascript
const response = await axios.post(
  `${API_BASE_URL}/token/refresh/`,
  { refresh: refreshToken }
)

const newAccessToken = response.data.access
const newRefreshToken = response.data.refresh // Si rotation activée
```

**Note importante** : Utilise `axios.post()` (instance native) et **non** `api.post()` pour éviter que cet appel passe par l'intercepteur (évite récursion).

#### Étape 4 : Sauvegarde des nouveaux tokens

```javascript
storage.saveToken(newAccessToken)

// Si Django renvoie un nouveau refresh token (rotation)
if (newRefreshToken) {
  storage.saveRefreshToken(newRefreshToken)
}
```

**Configuration Django pour la rotation** :
```python
# settings.py
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

Avec cette configuration :
- Chaque refresh génère un **nouveau refresh token**
- L'ancien refresh token est **blacklisté** (ne peut plus être réutilisé)
- Sécurité renforcée contre le vol de tokens

#### Étape 5 : Retry de la requête originale

```javascript
originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
return api(originalRequest) // Retry avec le nouveau token
```

La requête originale est automatiquement renvoyée avec le nouveau token. Du point de vue du composant Vue, c'est **transparent** :

```javascript
// Dans un composant Vue
async function loadData() {
  try {
    // Si le token expire pendant cet appel, il sera automatiquement
    // rafraîchi et la requête retentée sans que le composant le sache
    const response = await api.get('/users/')
    users.value = response.data
  } catch (error) {
    // N'arrive que si le refresh token est aussi expiré
    console.error('Failed to load users')
  }
}
```

#### Étape 6 : Gestion de l'échec du refresh

Si le refresh échoue (refresh token expiré ou invalide) :

```javascript
catch (refreshError) {
  console.error('❌ Token refresh failed:', refreshError)
  handleLogout()
  return Promise.reject(refreshError)
}
```

### Fonction `handleLogout()`

Appelée automatiquement en cas d'échec d'authentification :

```javascript
function handleLogout() {
  // 1. Nettoyer complètement le localStorage
  storage.clear()

  // 2. Notifier l'utilisateur
  Notify.create({
    type: 'warning',
    message: 'Session expirée',
    caption: 'Veuillez vous reconnecter'
  })

  // 3. Rediriger vers la page de login
  router.push({
    path: '/login',
    query: { redirect: currentPath } // Permet de revenir après reconnexion
  })
}
```

**Note** : La fonction `handleLogout()` nettoie seulement le `storage`. Le store Pinia détectera automatiquement que les tokens n'existent plus et mettra à jour son état en conséquence (grâce aux refs réactifs).

## Intégration avec le Store Pinia

### Séparation des Responsabilités

```
┌─────────────────────────────────────────────────────────────┐
│                  Architecture des Couches                    │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│         Composants Vue (UI Layer)              │
│  - LoginPage.vue                               │
│  - UsersList.vue                               │
│  - ProfilePage.vue                             │
└────────────────┬───────────────────────────────┘
                 │
                 │ Utilise
                 ↓
┌────────────────────────────────────────────────┐
│      Store Pinia (State Management)            │
│  - authStore : user, tokens, actions           │
│  - login(), logout(), fetchCurrentUser()       │
└────────────────┬───────────────────────────────┘
                 │
                 │ Utilise
                 ↓
┌────────────────────────────────────────────────┐
│        API Service (Business Logic)            │
│  - apiService.auth.login()                     │
│  - apiService.users.list()                     │
└────────────────┬───────────────────────────────┘
                 │
                 │ Utilise
                 ↓
┌────────────────────────────────────────────────┐
│    Axios Instance (HTTP Transport)             │
│  - api.get(), api.post(), etc.                 │
│  - Intercepteurs (Request + Response)          │
└────────────────┬───────────────────────────────┘
                 │
                 │ Lit/Écrit
                 ↓
┌────────────────────────────────────────────────┐
│      LocalStorage (Persistence)                │
│  - auth_token                                  │
│  - refresh_token                               │
│  - user                                        │
└────────────────────────────────────────────────┘
```

### Flux de Connexion Complet

```javascript
// 1. Composant Vue appelle le store
await authStore.login({ username, password })

// 2. Store appelle l'API service
const response = await apiService.auth.login(credentials)

// 3. API service utilise l'instance axios
return api.post('/api/auth/login/', credentials)

// 4. Intercepteur de requête (pas de token pour /login)
config.headers.Authorization = undefined // Pas de token pour login

// 5. Backend Django répond
{ access: "...", refresh: "...", user: {...} }

// 6. Store sauvegarde dans storage
storage.saveToken(access)
storage.saveRefreshToken(refresh)
storage.saveUser(user)

// 7. Store met à jour son state
accessToken.value = access
refreshToken.value = refresh
user.value = userData

// 8. Prochaines requêtes auront automatiquement le token
// (grâce à l'intercepteur qui lit depuis storage)
```

### Pourquoi cette architecture ?

**✅ Avantages** :
- **Pas de dépendance circulaire** : `axios` ne dépend pas du `store`, le `store` dépend d'`axios`
- **Réutilisabilité** : Les intercepteurs fonctionnent indépendamment du store
- **Testabilité** : Chaque couche peut être testée indépendamment
- **Séparation claire** : UI ↔ State ↔ API ↔ HTTP ↔ Storage

**❌ Alternative à éviter** :
```javascript
// MAUVAIS : Dépendance circulaire
import { useAuthStore } from 'stores/auth'

api.interceptors.request.use((config) => {
  const authStore = useAuthStore() // ❌ Problème !
  config.headers.Authorization = `Bearer ${authStore.accessToken}`
})
```

## Configuration Requise

### 1. Backend Django (settings.py)

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### 2. Frontend (src/utils/constants.js)

```javascript
export const API_BASE_URL = process.env.DEV
  ? 'http://localhost:8000/api'
  : process.env.API_URL

export const API_TIMEOUT = 30000 // 30 secondes
```

### 3. Boot Files Order (quasar.config.js)

L'ordre de chargement des boot files est important :

```javascript
boot: [
  'axios',  // Doit être chargé en premier
  'pinia',  // Ensuite le store
  // ... autres boots
]
```

## Debugging et Logs

### Mode Développement

En mode développement (`process.env.DEV === true`), les intercepteurs loggent :

**Request Interceptor** :
```
📤 API Request: {
  method: "GET",
  url: "/users/",
  data: undefined,
  params: { page: 1 },
  hasAuth: true
}
```

**Response Interceptor (Succès)** :
```
📥 API Response: {
  status: 200,
  url: "/users/",
  data: { results: [...] }
}
```

**Response Interceptor (Erreur)** :
```
❌ API Error: {
  status: 401,
  url: "/protected/",
  message: "Unauthorized",
  data: { detail: "Token has expired" }
}
```

**Token Refresh** :
```
✅ Access token refreshed successfully
🔄 Token rotated: New refresh token received
```

### Désactiver les logs en production

Les logs sont automatiquement désactivés en production. Pour forcer la désactivation :

```javascript
// Dans boot/axios.js, remplacer :
if (process.env.DEV) {
  console.log(...)
}

// Par :
const ENABLE_LOGS = false
if (ENABLE_LOGS && process.env.DEV) {
  console.log(...)
}
```

## Tests et Scénarios

### Tester le Refresh Automatique

1. **Connectez-vous** à l'application
2. **Attendez 2 heures** (ou modifiez `ACCESS_TOKEN_LIFETIME` à 1 minute pour les tests)
3. **Faites une requête API** depuis l'application
4. **Vérifiez les logs** :
   - Vous devriez voir "❌ API Error: status 401"
   - Suivi de "✅ Access token refreshed successfully"
   - Puis la requête originale qui réussit

### Tester l'Expiration Complète

1. **Connectez-vous** à l'application
2. **Attendez 7 jours** (ou modifiez `REFRESH_TOKEN_LIFETIME` à 5 minutes)
3. **Faites une requête API**
4. **Attendez-vous à** :
   - Notification "Session expirée"
   - Redirection vers `/login`
   - Storage vidé

### Tester la Rotation des Tokens

1. **Activez les logs** dans `axios.js`
2. **Connectez-vous**
3. **Forcez une erreur 401** (supprimez manuellement le token dans localStorage)
4. **Faites une requête**
5. **Vérifiez les logs** pour "🔄 Token rotated: New refresh token received"

## Bonnes Pratiques

### ✅ À FAIRE

1. **Toujours utiliser l'instance `api`** exportée depuis `boot/axios.js` :
   ```javascript
   import { api } from 'boot/axios'
   const response = await api.get('/users/')
   ```

2. **Laisser les intercepteurs gérer l'authentification** :
   ```javascript
   // Pas besoin d'ajouter manuellement le token
   await api.get('/protected/') // Token ajouté automatiquement
   ```

3. **Gérer les erreurs au niveau des composants** :
   ```javascript
   try {
     await api.post('/data/', formData)
   } catch (error) {
     // Notifications déjà affichées par l'intercepteur
     // Gérer la logique métier ici (réinitialiser formulaire, etc.)
   }
   ```

### ❌ À ÉVITER

1. **N'utilisez pas l'instance axios native** pour les appels API :
   ```javascript
   // MAUVAIS
   import axios from 'axios'
   await axios.get('http://localhost:8000/api/users/') // Pas d'intercepteurs !

   // BON
   import { api } from 'boot/axios'
   await api.get('/users/') // Passe par les intercepteurs
   ```

2. **Ne gérez pas manuellement le refresh dans les composants** :
   ```javascript
   // MAUVAIS
   try {
     await api.get('/data/')
   } catch (error) {
     if (error.response?.status === 401) {
       await authStore.refreshAccessToken() // L'intercepteur le fait déjà !
       await api.get('/data/')
     }
   }

   // BON
   await api.get('/data/') // L'intercepteur gère le refresh automatiquement
   ```

3. **N'importez pas authStore dans axios.js** :
   ```javascript
   // MAUVAIS - Dépendance circulaire
   import { useAuthStore } from 'stores/auth'

   // BON - Utiliser storage directement
   import { storage } from 'utils/storage'
   ```

## Résolution de Problèmes

### Problème : "Token refresh en boucle infinie"

**Cause** : Le flag `_retry` n'est pas correctement défini

**Solution** : Vérifier que `originalRequest._retry = true` est bien positionné avant le refresh

### Problème : "Session expirée immédiatement après connexion"

**Cause** : Problème de synchronisation entre storage et store

**Solution** : Vérifier que `authStore.login()` appelle bien `storage.saveToken()` et `storage.saveRefreshToken()`

### Problème : "Erreur CORS sur /token/refresh/"

**Cause** : L'endpoint de refresh n'est pas configuré dans les CORS du backend

**Solution** : Ajouter dans Django `settings.py` :
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:9000',
    # ... autres origines
]
```

### Problème : "Les notifications s'affichent plusieurs fois"

**Cause** : Plusieurs requêtes échouent en même temps et déclenchent plusieurs notifications

**Solution** : Implémenter un système de debounce pour les notifications dans l'intercepteur

## Ressources Additionnelles

- [Documentation Axios Interceptors](https://axios-http.com/docs/interceptors)
- [Documentation JWT Simple Django](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Documentation Quasar Boot Files](https://quasar.dev/quasar-cli-vite/boot-files)
- [Guide d'authentification JWT - Best Practices](https://tools.ietf.org/html/rfc8725)
