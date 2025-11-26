# Exemples Pratiques d'Utilisation des Intercepteurs Axios

Ce document présente des exemples concrets d'utilisation des intercepteurs Axios dans l'application SUPERVISOR V2.0.

## Exemple 1 : Connexion et Requêtes Protégées

```vue
<template>
  <q-page class="q-pa-md">
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="text-h6">Connexion</div>
      </q-card-section>

      <q-card-section>
        <q-input v-model="username" label="Username" outlined />
        <q-input v-model="password" type="password" label="Password" outlined class="q-mt-md" />
        <q-btn @click="handleLogin" label="Se connecter" color="primary" class="q-mt-md" />
      </q-card-section>
    </q-card>

    <q-card v-if="isLoggedIn">
      <q-card-section>
        <div class="text-h6">Données Protégées</div>
      </q-card-section>

      <q-card-section>
        <q-btn @click="fetchProtectedData" label="Charger Données" color="secondary" />
        <pre v-if="data" class="q-mt-md">{{ data }}</pre>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from 'src/stores/auth'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const data = ref(null)
const isLoggedIn = ref(false)

async function handleLogin() {
  try {
    // 1. Connexion via le store
    await authStore.login({
      username: username.value,
      password: password.value
    })

    isLoggedIn.value = true

    $q.notify({
      type: 'positive',
      message: 'Connexion réussie'
    })

    console.log('✅ Connexion réussie')
    console.log('📦 Token sauvegardé dans localStorage')
    console.log('🔒 Prochaines requêtes auront automatiquement le token')
  } catch (error) {
    console.error('❌ Erreur de connexion:', error)
  }
}

async function fetchProtectedData() {
  try {
    // 2. Requête protégée - Le token est ajouté automatiquement par l'intercepteur
    console.log('📤 Envoi de la requête...')
    console.log('🔑 L\'intercepteur ajoute automatiquement: Authorization: Bearer {token}')

    const response = await api.get('/users/me/')

    data.value = response.data

    console.log('✅ Données reçues:', response.data)
    console.log('💡 Si le token avait expiré, il aurait été rafraîchi automatiquement')
  } catch (error) {
    console.error('❌ Erreur:', error)
    console.log('⚠️ Si le refresh token est aussi expiré, vous serez déconnecté automatiquement')
  }
}
</script>
```

**Flux d'exécution** :

1. **Login** → `authStore.login()` → Tokens sauvegardés dans localStorage
2. **Requête protégée** → Intercepteur lit token depuis localStorage → Ajoute header `Authorization: Bearer {token}`
3. **Si 401** → Intercepteur tente refresh automatique → Retry requête avec nouveau token
4. **Si refresh échoue** → Déconnexion automatique → Redirection vers `/login`

## Exemple 2 : Gestion Automatique de l'Expiration du Token

```javascript
// Composant qui fait une requête toutes les 5 minutes
import { ref, onMounted, onUnmounted } from 'vue'
import { api } from 'boot/axios'

export default {
  setup() {
    const stats = ref(null)
    let intervalId = null

    async function fetchStats() {
      try {
        // Cette requête sera automatiquement réessayée avec un nouveau token
        // si l'access token a expiré (après 2h par défaut)
        const response = await api.get('/dashboard/stats/')
        stats.value = response.data

        console.log('✅ Stats récupérées')
      } catch (error) {
        // N'arrive que si le refresh token est aussi expiré (après 7 jours)
        console.error('❌ Impossible de récupérer les stats')
        // L'utilisateur sera automatiquement redirigé vers /login
      }
    }

    onMounted(() => {
      // Première récupération
      fetchStats()

      // Ensuite toutes les 5 minutes
      intervalId = setInterval(fetchStats, 5 * 60 * 1000)
    })

    onUnmounted(() => {
      if (intervalId) clearInterval(intervalId)
    })

    return { stats }
  }
}
```

**Ce qui se passe en arrière-plan** :

- **Minute 0** : Connexion, access token valide pour 2h
- **Minute 5, 10, 15...** : Requêtes réussies avec le même access token
- **Minute 125** : Access token expiré → Intercepteur détecte 401 → Refresh automatique → Requête réessayée → Succès
- **Minute 130, 135...** : Requêtes réussies avec le nouveau access token
- **Jour 8** : Refresh token expiré → Refresh échoue → Déconnexion automatique → Redirection `/login`

## Exemple 3 : Upload de Fichier avec Authentification

```vue
<template>
  <q-file
    v-model="file"
    label="Sélectionner une photo"
    outlined
    accept="image/*"
    @update:model-value="uploadPhoto"
  >
    <template v-slot:prepend>
      <q-icon name="attach_file" />
    </template>
  </q-file>
</template>

<script setup>
import { ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const file = ref(null)

async function uploadPhoto() {
  if (!file.value) return

  const formData = new FormData()
  formData.append('photo', file.value)
  formData.append('description', 'Photo de chantier')

  try {
    // L'intercepteur ajoute automatiquement le token même pour les FormData
    const response = await api.post('/tasks/123/photos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        console.log(`Upload: ${percentCompleted}%`)
      }
    })

    $q.notify({
      type: 'positive',
      message: 'Photo uploadée avec succès'
    })

    console.log('✅ Photo uploadée:', response.data)
  } catch (error) {
    console.error('❌ Erreur upload:', error)
  }
}
</script>
```

**Headers envoyés** :
```
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Accept: application/json
```

## Exemple 4 : Requêtes Parallèles avec Gestion d'Erreurs

```javascript
import { api } from 'boot/axios'

async function loadDashboardData() {
  try {
    // Toutes ces requêtes auront automatiquement le token JWT
    // Si l'une échoue avec 401, elle sera automatiquement rafraîchie
    const [users, tasks, projects, stats] = await Promise.all([
      api.get('/users/'),
      api.get('/tasks/?status=in_progress'),
      api.get('/projects/?status=active'),
      api.get('/dashboard/stats/')
    ])

    console.log('✅ Toutes les données chargées')

    return {
      users: users.data,
      tasks: tasks.data,
      projects: projects.data,
      stats: stats.data
    }
  } catch (error) {
    console.error('❌ Erreur de chargement:', error)

    // Si une requête échoue après refresh (refresh token expiré),
    // l'utilisateur sera automatiquement déconnecté
    throw error
  }
}
```

**Scénario de token expiré pendant les requêtes parallèles** :

1. **4 requêtes** envoyées en même temps
2. **Toutes reçoivent 401** (token expiré)
3. **Une seule tente le refresh** (grâce au flag `_retry`)
4. **Les autres attendent** que le token soit rafraîchi
5. **Toutes sont retentées** avec le nouveau token
6. **Succès**

## Exemple 5 : Tester le Refresh Automatique

```javascript
// Utilitaire de test pour forcer l'expiration du token
export async function testTokenRefresh() {
  const { storage } = await import('src/utils/storage')
  const { api } = await import('boot/axios')

  console.log('🧪 Test de refresh automatique du token')

  // 1. Vérifier qu'on est connecté
  const oldToken = storage.getToken()
  if (!oldToken) {
    console.error('❌ Pas de token, veuillez vous connecter d\'abord')
    return
  }

  console.log('✅ Token actuel:', oldToken.substring(0, 20) + '...')

  // 2. Invalider le token en le modifiant
  console.log('🔧 Invalidation du token...')
  storage.saveToken('invalid_token_for_testing')

  // 3. Tenter une requête protégée
  console.log('📤 Envoi d\'une requête avec token invalide...')

  try {
    const response = await api.get('/users/me/')

    console.log('✅ Requête réussie après refresh automatique!')
    console.log('🔄 Nouveau token:', storage.getToken().substring(0, 20) + '...')
    console.log('📊 Données:', response.data)
  } catch (error) {
    console.error('❌ Échec du refresh (refresh token probablement expiré)')
    console.log('🔒 Vous avez été déconnecté automatiquement')
  }
}
```

**Utilisation** :
```javascript
// Dans la console du navigateur
import { testTokenRefresh } from './test-utils'
await testTokenRefresh()
```

**Output attendu** :
```
🧪 Test de refresh automatique du token
✅ Token actuel: eyJ0eXAiOiJKV1QiLCJ...
🔧 Invalidation du token...
📤 Envoi d'une requête avec token invalide...
❌ API Error: { status: 401, url: "/users/me/" }
🔄 Token rotated: New refresh token received
✅ Access token refreshed successfully
📤 Retry request with new token
✅ Requête réussie après refresh automatique!
🔄 Nouveau token: eyJ0eXAiOiJKV1QiLCJ...
📊 Données: { id: 1, username: "admin", ... }
```

## Exemple 6 : Intercepter les Erreurs Personnalisées

```javascript
// Dans un composant ou service
import { api } from 'boot/axios'

async function deleteUser(userId) {
  try {
    await api.delete(`/users/${userId}/`)

    // Succès - notification déjà affichée par l'intercepteur
    return true
  } catch (error) {
    // L'intercepteur a déjà affiché une notification générique
    // On peut ajouter une logique métier spécifique ici

    if (error.response?.status === 403) {
      console.log('💡 Vous n\'avez pas les permissions pour supprimer cet utilisateur')
      // Peut-être afficher un dialogue explicatif
    } else if (error.response?.status === 404) {
      console.log('💡 Cet utilisateur n\'existe plus')
      // Rafraîchir la liste
    }

    return false
  }
}
```

## Exemple 7 : Mode Hors Ligne (Service Worker + Intercepteur)

```javascript
// Détection de mode hors ligne
api.interceptors.response.use(
  response => response,
  async error => {
    // Si erreur réseau (pas de connexion)
    if (!error.response && error.message === 'Network Error') {
      console.log('🔌 Mode hors ligne détecté')

      // Sauvegarder la requête pour retry plus tard
      const offlineQueue = JSON.parse(
        localStorage.getItem('offline_requests') || '[]'
      )

      offlineQueue.push({
        method: error.config.method,
        url: error.config.url,
        data: error.config.data,
        timestamp: Date.now()
      })

      localStorage.setItem('offline_requests', JSON.stringify(offlineQueue))

      console.log('💾 Requête mise en file d\'attente')
    }

    return Promise.reject(error)
  }
)

// Quand la connexion revient
window.addEventListener('online', async () => {
  console.log('🌐 Connexion rétablie')

  const offlineQueue = JSON.parse(
    localStorage.getItem('offline_requests') || '[]'
  )

  if (offlineQueue.length > 0) {
    console.log(`📤 Envoi de ${offlineQueue.length} requêtes en attente...`)

    for (const req of offlineQueue) {
      try {
        await api({
          method: req.method,
          url: req.url,
          data: req.data
        })
        console.log('✅ Requête envoyée:', req.url)
      } catch (error) {
        console.error('❌ Échec:', req.url)
      }
    }

    localStorage.removeItem('offline_requests')
  }
})
```

## Exemple 8 : Debug et Monitoring

```javascript
// Ajouter un système de monitoring des requêtes
let requestCount = 0
let errorCount = 0
let refreshCount = 0

// Dans l'intercepteur de requête
api.interceptors.request.use((config) => {
  requestCount++
  config.metadata = { startTime: Date.now() }

  console.log(`📊 Total requests: ${requestCount}`)

  return config
})

// Dans l'intercepteur de réponse
api.interceptors.response.use(
  (response) => {
    const duration = Date.now() - response.config.metadata.startTime
    console.log(`⏱️ Request took ${duration}ms`)

    return response
  },
  async (error) => {
    errorCount++

    if (error.response?.status === 401) {
      refreshCount++
      console.log(`🔄 Token refresh count: ${refreshCount}`)
    }

    console.log(`📊 Error rate: ${(errorCount / requestCount * 100).toFixed(2)}%`)

    return Promise.reject(error)
  }
)

// Afficher les stats
export function getApiStats() {
  return {
    totalRequests: requestCount,
    totalErrors: errorCount,
    tokenRefreshes: refreshCount,
    errorRate: (errorCount / requestCount * 100).toFixed(2) + '%'
  }
}
```

## Bonnes Pratiques Démontrées

1. ✅ **Toujours utiliser l'instance `api` configurée**
2. ✅ **Laisser les intercepteurs gérer l'authentification**
3. ✅ **Ne pas gérer manuellement le refresh du token**
4. ✅ **Utiliser try/catch pour la logique métier spécifique**
5. ✅ **Logger les opérations en mode développement**
6. ✅ **Tester régulièrement les scénarios d'expiration**
7. ✅ **Gérer gracieusement le mode hors ligne**
8. ✅ **Monitorer les performances et erreurs**

## Tests Recommandés

### Test 1 : Connexion et Accès aux Ressources Protégées
- Connexion → Requête protégée → Vérifier header Authorization

### Test 2 : Expiration du Token
- Connexion → Attendre 2h (ou modifier lifetime) → Requête → Vérifier refresh automatique

### Test 3 : Expiration Complète
- Connexion → Attendre 7 jours → Requête → Vérifier déconnexion automatique

### Test 4 : Requêtes Parallèles avec Token Expiré
- Connexion → Invalider token → 4 requêtes simultanées → Vérifier qu'une seule refresh

### Test 5 : Rotation des Tokens
- Connexion → Forcer refresh → Vérifier nouveau refresh token reçu

### Test 6 : Gestion des Erreurs
- Tester chaque code d'erreur (400, 403, 404, 422, 429, 500, 503)
- Vérifier les notifications appropriées

Ces exemples démontrent la puissance et la transparence des intercepteurs Axios configurés pour SUPERVISOR V2.0.
