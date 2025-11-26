# Guide d'utilisation du Store d'Authentification

Ce guide explique comment utiliser le store Pinia d'authentification dans vos composants Vue.

## Importation du Store

```javascript
import { useAuthStore } from 'src/stores/auth'
```

## Utilisation dans un Composant Vue

### 1. Connexion (Page de Login)

```vue
<template>
  <q-page class="flex flex-center">
    <q-card class="login-card">
      <q-card-section>
        <div class="text-h5 text-center">Connexion</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="handleLogin">
          <q-input
            v-model="username"
            label="Nom d'utilisateur"
            outlined
            :rules="[val => !!val || 'Requis']"
          />

          <q-input
            v-model="password"
            type="password"
            label="Mot de passe"
            outlined
            :rules="[val => !!val || 'Requis']"
          />

          <q-btn
            type="submit"
            label="Se connecter"
            color="primary"
            class="full-width"
            :loading="loading"
          />
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  loading.value = true

  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })

    $q.notify({
      type: 'positive',
      message: `Bienvenue ${authStore.userFullName} !`,
      position: 'top'
    })

    // Rediriger vers la page d'accueil
    router.push('/')
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.response?.data?.detail || 'Identifiants incorrects',
      position: 'top'
    })
  } finally {
    loading.value = false
  }
}
</script>
```

### 2. Déconnexion

```vue
<template>
  <q-btn
    flat
    icon="logout"
    label="Déconnexion"
    @click="handleLogout"
  />
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

async function handleLogout() {
  try {
    await authStore.logout()

    $q.notify({
      type: 'info',
      message: 'Déconnexion réussie',
      position: 'top'
    })

    router.push('/login')
  } catch (error) {
    console.error('Erreur lors de la déconnexion:', error)
  }
}
</script>
```

### 3. Afficher les Informations de l'Utilisateur

```vue
<template>
  <div v-if="authStore.isAuthenticated">
    <q-card>
      <q-card-section>
        <div class="text-h6">Profil Utilisateur</div>
      </q-card-section>

      <q-card-section>
        <p><strong>Nom complet :</strong> {{ authStore.userFullName }}</p>
        <p><strong>Email :</strong> {{ authStore.user?.email }}</p>
        <p><strong>Rôle :</strong> {{ authStore.userRole }}</p>
        <p><strong>Code :</strong> {{ authStore.user?.profile?.code }}</p>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()
</script>
```

### 4. Vérifications de Rôles et Permissions

```vue
<template>
  <div>
    <!-- Bouton visible uniquement pour les admins -->
    <q-btn
      v-if="authStore.hasAdminRights"
      label="Administration"
      color="primary"
      @click="goToAdmin"
    />

    <!-- Bouton visible uniquement pour les superviseurs -->
    <q-btn
      v-if="authStore.isSuperviseur"
      label="Mes Tâches"
      color="secondary"
      @click="goToTasks"
    />

    <!-- Vérification d'une permission spécifique -->
    <q-btn
      v-if="authStore.hasPermission('users.create')"
      label="Créer Utilisateur"
      color="positive"
      @click="createUser"
    />
  </div>
</template>

<script setup>
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()

function goToAdmin() {
  // Navigation vers admin
}

function goToTasks() {
  // Navigation vers tâches
}

function createUser() {
  // Créer utilisateur
}
</script>
```

### 5. Mise à Jour du Profil

```vue
<template>
  <q-form @submit="handleUpdateProfile">
    <q-input
      v-model="form.telephone"
      label="Téléphone"
      outlined
    />

    <q-input
      v-model="form.email"
      label="Email"
      type="email"
      outlined
    />

    <q-btn
      type="submit"
      label="Mettre à jour"
      color="primary"
      :loading="loading"
    />
  </q-form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

const $q = useQuasar()
const authStore = useAuthStore()

const form = ref({
  telephone: '',
  email: ''
})
const loading = ref(false)

onMounted(() => {
  // Charger les données actuelles
  if (authStore.user?.profile) {
    form.value.telephone = authStore.user.profile.telephone || ''
    form.value.email = authStore.user.email || ''
  }
})

async function handleUpdateProfile() {
  loading.value = true

  try {
    await authStore.updateUserProfile(form.value)

    $q.notify({
      type: 'positive',
      message: 'Profil mis à jour avec succès',
      position: 'top'
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de la mise à jour',
      position: 'top'
    })
  } finally {
    loading.value = false
  }
}
</script>
```

### 6. Changement de Mot de Passe

```vue
<template>
  <q-form @submit="handleChangePassword">
    <q-input
      v-model="form.old_password"
      type="password"
      label="Ancien mot de passe"
      outlined
      :rules="[val => !!val || 'Requis']"
    />

    <q-input
      v-model="form.new_password"
      type="password"
      label="Nouveau mot de passe"
      outlined
      :rules="[
        val => !!val || 'Requis',
        val => val.length >= 8 || 'Minimum 8 caractères'
      ]"
    />

    <q-input
      v-model="form.confirm_password"
      type="password"
      label="Confirmer le mot de passe"
      outlined
      :rules="[
        val => !!val || 'Requis',
        val => val === form.new_password || 'Les mots de passe ne correspondent pas'
      ]"
    />

    <q-btn
      type="submit"
      label="Changer le mot de passe"
      color="primary"
      :loading="loading"
    />
  </q-form>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

const $q = useQuasar()
const authStore = useAuthStore()

const form = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})
const loading = ref(false)

async function handleChangePassword() {
  loading.value = true

  try {
    await authStore.changePassword({
      old_password: form.value.old_password,
      new_password: form.value.new_password
    })

    $q.notify({
      type: 'positive',
      message: 'Mot de passe changé avec succès',
      position: 'top'
    })

    // Réinitialiser le formulaire
    form.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.response?.data?.old_password?.[0] || 'Erreur lors du changement',
      position: 'top'
    })
  } finally {
    loading.value = false
  }
}
</script>
```

## Initialisation du Store au Démarrage de l'Application

Dans votre `App.vue` ou dans un boot file :

```javascript
// src/App.vue
<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  // Initialiser le store depuis localStorage
  await authStore.initializeStore()
})
</script>
```

Ou dans un boot file `src/boot/auth.js` :

```javascript
import { useAuthStore } from 'src/stores/auth'

export default async ({ app }) => {
  const authStore = useAuthStore()
  await authStore.initializeStore()
}
```

## Guards de Navigation dans Vue Router

Protégez vos routes avec des guards d'authentification :

```javascript
// src/router/index.js
import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'src/stores/auth'

export default route(function () {
  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createWebHistory()
  })

  // Guard global d'authentification
  Router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Vérifier si la route nécessite une authentification
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      next('/login')
      return
    }

    // Vérifier les rôles requis
    if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
      next('/unauthorized')
      return
    }

    // Vérifier les permissions requises
    if (to.meta.permissions) {
      const hasPermission = to.meta.permissions.every(
        perm => authStore.hasPermission(perm)
      )
      if (!hasPermission) {
        next('/unauthorized')
        return
      }
    }

    next()
  })

  return Router
})
```

Exemple de définition de routes avec meta :

```javascript
// src/router/routes.js
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: () => import('pages/IndexPage.vue')
      },
      {
        path: 'admin',
        component: () => import('pages/AdminPage.vue'),
        meta: {
          requiresAuth: true,
          roles: ['SUPERADMIN', 'ADMIN']
        }
      },
      {
        path: 'users',
        component: () => import('pages/UsersPage.vue'),
        meta: {
          requiresAuth: true,
          permissions: ['users.view', 'users.create']
        }
      }
    ]
  },
  {
    path: '/login',
    component: () => import('pages/LoginPage.vue')
  }
]

export default routes
```

## API du Store

### State

- `user` : Informations de l'utilisateur connecté
- `accessToken` : Token JWT d'accès
- `refreshToken` : Token JWT de rafraîchissement
- `isAuthenticated` : Boolean (computed)

### Getters

- `userRole` : Rôle de l'utilisateur ('SUPERADMIN', 'ADMIN', etc.)
- `userFullName` : Nom complet de l'utilisateur
- `isSuperAdmin` : Boolean
- `isAdmin` : Boolean
- `isCoordonnateur` : Boolean
- `isStockman` : Boolean
- `isSuperviseur` : Boolean
- `hasAdminRights` : Boolean (SUPERADMIN ou ADMIN)
- `hasPermission(code)` : Function - Vérifie une permission spécifique

### Actions

- `login(credentials)` : Connexion
- `logout()` : Déconnexion
- `refreshAccessToken()` : Rafraîchir le token (automatique via intercepteur)
- `fetchCurrentUser()` : Récupérer les infos utilisateur
- `updateUserProfile(data)` : Mettre à jour le profil
- `changePassword(data)` : Changer le mot de passe
- `initializeStore()` : Initialiser depuis localStorage
- `isTokenValid()` : Vérifier la validité du token

## Notes Importantes

1. **Persistance** : Les tokens et les données utilisateur sont automatiquement sauvegardés dans localStorage
2. **Refresh automatique** : L'intercepteur Axios gère automatiquement le rafraîchissement du token en cas de 401
3. **Déconnexion automatique** : Si le refresh token expire, l'utilisateur est automatiquement déconnecté
4. **Sécurité** : Ne jamais exposer les tokens dans les logs ou la console en production

## Bonnes Pratiques

1. **Initialiser le store au démarrage** de l'application
2. **Utiliser les guards de navigation** pour protéger les routes
3. **Vérifier les permissions** avant d'afficher des actions sensibles
4. **Gérer les erreurs** correctement avec des notifications utilisateur
5. **Déconnecter l'utilisateur** en cas d'erreur d'authentification critique
