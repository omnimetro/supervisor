# Documentation du MainLayout - SUPERVISOR V2.0

Ce document décrit le layout principal de l'application SUPERVISOR, qui sert de conteneur pour toutes les pages protégées.

## Vue d'ensemble

Le `MainLayout.vue` fournit la structure principale de l'application une fois l'utilisateur authentifié. Il comprend :
- **Header** avec logo, icônes d'actions, et menu utilisateur
- **Sidebar** avec navigation
- **Container principal** pour le contenu des pages

## Structure du Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Header                                                     │
│  [Menu] SUPERVISOR V2.0    [Sync] [Notif] [User Menu]     │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│  Sidebar │  Page Content (router-view)                     │
│          │                                                  │
│  • Dash  │                                                  │
│  • Chant │                                                  │
│  • B2B   │                                                  │
│  • ...   │                                                  │
│          │                                                  │
│  Footer  │                                                  │
└──────────┴──────────────────────────────────────────────────┘
```

## Composants du Header

### 1. Logo et Titre

```vue
<q-toolbar-title class="text-primary text-weight-bold">
  SUPERVISOR V2.0
</q-toolbar-title>
```

- Couleur primaire (#ea1d31)
- Position à gauche après le bouton menu
- Toujours visible

### 2. Bouton Synchronisation

```vue
<q-btn flat dense round icon="sync" @click="handleSync">
  <q-badge v-if="pendingSyncCount > 0" color="warning" floating>
    {{ pendingSyncCount }}
  </q-badge>
  <q-tooltip>
    {{ pendingSyncCount > 0 ? `${pendingSyncCount} données en attente de synchronisation` : 'Synchronisation' }}
  </q-tooltip>
</q-btn>
```

**Fonctionnalités :**
- Affiche un badge orange avec le nombre de données en attente si `pendingSyncCount > 0`
- Tooltip informatif
- Appelle `handleSync()` au clic
- **TODO** : Implémenter la logique de synchronisation complète

**Usage futur :**
```javascript
// Dans un composant ou store
const syncStore = useSyncStore()
const pendingSyncCount = syncStore.getPendingCount()

// Déclencher la synchronisation
await syncStore.syncAll()
```

### 3. Bouton Notifications

```vue
<q-btn flat dense round icon="notifications" @click="showNotifications = true">
  <q-badge v-if="unreadNotificationsCount > 0" color="negative" floating>
    {{ unreadNotificationsCount }}
  </q-badge>
  <q-tooltip>
    {{ unreadNotificationsCount > 0 ? `${unreadNotificationsCount} notifications non lues` : 'Notifications' }}
  </q-tooltip>
</q-btn>
```

**Fonctionnalités :**
- Affiche un badge rouge avec le nombre de notifications non lues
- Ouvre le panneau de notifications au clic
- Le compteur est calculé automatiquement via computed property

**Computed property :**
```javascript
const unreadNotificationsCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})
```

### 4. Menu Utilisateur (Dropdown)

```vue
<q-btn-dropdown flat dense no-caps>
  <template v-slot:label>
    <div class="row items-center no-wrap">
      <q-avatar size="32px" color="primary" text-color="white">
        <span class="text-caption">{{ getUserInitials() }}</span>
      </q-avatar>
      <div class="text-left gt-xs">
        <div class="text-body2 text-weight-medium">{{ authStore.userFullName }}</div>
        <div class="text-caption text-grey-6">{{ authStore.userRole }}</div>
      </div>
    </div>
  </template>

  <q-list style="min-width: 220px">
    <!-- User Info Header -->
    <!-- Mon Profil -->
    <!-- Paramètres (Admin only) -->
    <!-- Aide -->
    <!-- Se déconnecter -->
  </q-list>
</q-btn-dropdown>
```

**Options du menu :**

| Option | Icône | Couleur | Visible | Action |
|--------|-------|---------|---------|--------|
| **En-tête** | - | bg-grey-2 | Toujours | Affiche nom + email |
| **Mon Profil** | person | primary | Toujours | `goToProfile()` → `/profile` |
| **Paramètres** | settings | secondary | Admin uniquement | `goToSettings()` → `/settings` |
| **Aide** | help | info | Toujours | `showHelp()` → Dialog |
| **Se déconnecter** | logout | negative | Toujours | `handleLogout()` → Confirmation |

**Condition d'affichage "Paramètres" :**
```vue
<q-item v-if="authStore.hasAdminRights" ...>
```

`hasAdminRights` est `true` pour les rôles : **SUPERADMIN** et **ADMIN**

## Sidebar (Navigation)

### Structure

```vue
<q-drawer
  v-model="leftDrawerOpen"
  show-if-above
  bordered
  :width="260"
  class="main-drawer"
>
  <!-- Drawer Header -->
  <!-- Navigation Menu -->
  <!-- Drawer Footer -->
</q-drawer>
```

**Caractéristiques :**
- Largeur : 260px
- `show-if-above` : Affiche automatiquement sur écrans ≥ 1024px (lg)
- `v-model="leftDrawerOpen"` : Contrôlé par le bouton menu

### Header du Drawer

```vue
<div class="drawer-header q-pa-md bg-primary text-white">
  <div class="text-h6 text-weight-bold">AI Venture</div>
  <div class="text-caption">Gestion des chantiers</div>
</div>
```

- Dégradé rouge (primaire)
- Nom de l'entreprise : **AI Venture**
- Sous-titre : "Gestion des chantiers"

### Menu de Navigation

**Items actifs :**

```vue
<q-item
  clickable
  v-ripple
  :active="$route.name === 'dashboard'"
  @click="navigateTo('/dashboard')"
  active-class="active-menu-item"
>
  <q-item-section avatar>
    <q-icon name="dashboard" />
  </q-item-section>
  <q-item-section>
    <q-item-label>Tableau de Bord</q-item-label>
  </q-item-section>
</q-item>
```

| Menu | Route | Icône | État |
|------|-------|-------|------|
| Tableau de Bord | /dashboard | dashboard | ✅ Actif |
| Chantiers | - | construction | ⏸️ Désactivé (futur) |
| B2B | - | business_center | ⏸️ Désactivé (futur) |
| Stocks | - | inventory | ⏸️ Désactivé (futur) |
| Dépenses | - | payments | ⏸️ Désactivé (futur) |
| Cartographie | - | map | ⏸️ Désactivé (futur) |
| Administration | - | settings | ⏸️ Désactivé (Admin uniquement) |

**État actif :**
- Classe CSS : `active-menu-item`
- Background : rgba(#ea1d31, 0.1)
- Couleur texte/icône : #ea1d31 (primaire)
- Font-weight : 600

**Items désactivés :**
- Attribut `disable`
- Opacité : 0.5
- Non cliquables

### Footer du Drawer

```vue
<div class="drawer-footer absolute-bottom q-pa-md text-center text-caption text-grey-6">
  <div>SUPERVISOR V2.0</div>
  <div>&copy; {{ currentYear }} AI Venture</div>
</div>
```

- Position absolue en bas
- Affiche version et copyright
- `currentYear` : Calculé automatiquement

## Panneau de Notifications

### Dialog de Notifications

```vue
<q-dialog v-model="showNotifications" position="right">
  <q-card style="width: 400px; max-width: 90vw">
    <q-card-section class="row items-center q-pb-none">
      <div class="text-h6">Notifications</div>
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />
    </q-card-section>

    <q-card-section>
      <q-list v-if="notifications.length > 0" separator>
        <!-- Notifications items -->
      </q-list>

      <div v-else class="text-center text-grey-6 q-py-lg">
        <q-icon name="notifications_none" size="48px" />
        <div>Aucune notification</div>
      </div>
    </q-card-section>

    <q-card-actions v-if="notifications.length > 0" align="right">
      <q-btn
        flat
        label="Tout marquer comme lu"
        color="primary"
        @click="markAllAsRead"
      />
    </q-card-actions>
  </q-card>
</q-dialog>
```

**Caractéristiques :**
- Position : `right` (s'ouvre depuis la droite)
- Largeur : 400px (max 90vw sur mobile)
- Bouton de fermeture en haut à droite
- État vide avec icône et message

### Structure d'une Notification

```javascript
{
  id: 1,
  type: 'info',  // 'info' | 'success' | 'warning' | 'error'
  title: 'Nouveau chantier assigné',
  message: 'Déploiement FTTH Zone Nord - Orange',
  time: 'Il y a 5 minutes',
  read: false
}
```

**Types de notifications :**

| Type | Couleur | Icône |
|------|---------|-------|
| info | info (bleu) | info |
| success | positive (vert) | check_circle |
| warning | warning (orange) | warning |
| error | negative (rouge) | error |

### Actions sur les Notifications

#### Marquer comme lu (une seule)

```javascript
function markAsRead(notificationId) {
  const notification = notifications.value.find(n => n.id === notificationId)
  if (notification) {
    notification.read = true
    // TODO: Appeler l'API
  }
}
```

**Usage :**
```vue
<q-item @click="markAsRead(notification.id)">
```

#### Marquer toutes comme lues

```javascript
function markAllAsRead() {
  notifications.value.forEach(n => {
    n.read = true
  })

  $q.notify({
    type: 'positive',
    message: 'Toutes les notifications ont été marquées comme lues',
    position: 'top',
    timeout: 2000
  })

  // TODO: Appeler l'API
}
```

**Visual feedback :**
- Notification non lue : `bg-grey-2` (fond gris clair)
- Notification lue : fond blanc (par défaut)

## State Management

### Variables d'État

```javascript
const leftDrawerOpen = ref(false)
const currentYear = new Date().getFullYear()
const showNotifications = ref(false)
const pendingSyncCount = ref(0)

const notifications = ref([
  {
    id: 1,
    type: 'info',
    title: 'Nouveau chantier assigné',
    message: 'Déploiement FTTH Zone Nord - Orange',
    time: 'Il y a 5 minutes',
    read: false
  },
  // ... autres notifications
])
```

### Computed Properties

```javascript
const unreadNotificationsCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})
```

## Méthodes Principales

### Navigation

#### toggleLeftDrawer()

```javascript
function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
```

Appelé par le bouton menu dans le header.

#### navigateTo(path)

```javascript
function navigateTo(path) {
  router.push(path)
}
```

Navigation programmatique vers une route.

#### goToProfile()

```javascript
function goToProfile() {
  router.push('/profile')
}
```

Navigue vers la page de profil utilisateur.

#### goToSettings()

```javascript
function goToSettings() {
  router.push('/settings')
}
```

Navigue vers la page de paramètres (admin uniquement).

**Note :** La route `/settings` doit être créée dans `routes.js`

### Actions Utilisateur

#### handleLogout()

```javascript
async function handleLogout() {
  $q.dialog({
    title: 'Déconnexion',
    message: 'Êtes-vous sûr de vouloir vous déconnecter ?',
    cancel: {
      label: 'Annuler',
      flat: true
    },
    ok: {
      label: 'Déconnexion',
      color: 'negative'
    },
    persistent: true
  }).onOk(async () => {
    try {
      await authStore.logout()

      $q.notify({
        type: 'info',
        message: 'Déconnexion réussie',
        position: 'top',
        timeout: 2000
      })

      router.push('/auth/login')
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error)
    }
  })
}
```

**Flux de déconnexion :**
1. Affiche un dialog de confirmation
2. Si confirmé :
   - Appelle `authStore.logout()` (nettoie tokens et état)
   - Affiche notification de succès
   - Redirige vers `/auth/login`
3. Si annulé : rien ne se passe

#### handleSync()

```javascript
function handleSync() {
  $q.notify({
    type: 'info',
    message: 'Synchronisation en cours...',
    position: 'top',
    timeout: 2000
  })

  // TODO: Implémenter la logique de synchronisation
  // - Envoyer les données en attente vers le serveur
  // - Récupérer les nouvelles données du serveur
  // - Mettre à jour pendingSyncCount
}
```

**À implémenter :**
- Synchronisation des données locales (IndexedDB/LocalStorage) vers le serveur
- Récupération des nouvelles données
- Mise à jour du compteur `pendingSyncCount`
- Gestion des erreurs réseau

#### showHelp()

```javascript
function showHelp() {
  $q.dialog({
    title: 'Aide',
    message: 'Documentation et support technique à venir. Pour toute question, contactez l\'administrateur.',
    ok: {
      label: 'Fermer',
      color: 'primary'
    }
  })

  // TODO: Créer une page d'aide complète ou ouvrir un lien vers la documentation
}
```

**Options futures :**
- Créer une route `/help` avec documentation complète
- Ouvrir un lien externe vers la documentation en ligne
- Afficher un panneau contextuel d'aide selon la page actuelle

### Utilitaires

#### getUserInitials()

```javascript
function getUserInitials() {
  const fullName = authStore.userFullName
  if (!fullName) return 'U'

  const names = fullName.split(' ')
  if (names.length >= 2) {
    return (names[0][0] + names[1][0]).toUpperCase()
  }
  return fullName.substring(0, 2).toUpperCase()
}
```

**Logique :**
- Si nom complet vide : retourne "U"
- Si au moins 2 mots : retourne initiales (ex: "John Doe" → "JD")
- Sinon : retourne 2 premiers caractères en majuscules

#### getNotificationColor(type)

```javascript
function getNotificationColor(type) {
  const colors = {
    info: 'info',
    success: 'positive',
    warning: 'warning',
    error: 'negative'
  }
  return colors[type] || 'grey'
}
```

Retourne la couleur Quasar appropriée selon le type.

#### getNotificationIcon(type)

```javascript
function getNotificationIcon(type) {
  const icons = {
    info: 'info',
    success: 'check_circle',
    warning: 'warning',
    error: 'error'
  }
  return icons[type] || 'notifications'
}
```

Retourne l'icône Material appropriée selon le type.

## Styles SCSS

### Variables

```scss
$primary-color: #ea1d31;
$drawer-width: 260px;
```

### Header

```scss
.q-header {
  border-bottom: 1px solid #E0E0E0;
}

.user-menu-btn {
  :deep(.q-btn__content) {
    padding: 4px 8px;
  }
}
```

### Drawer

```scss
.main-drawer {
  .drawer-header {
    background: linear-gradient(135deg, $primary-color 0%, darken($primary-color, 10%) 100%);
  }

  .drawer-footer {
    border-top: 1px solid #E0E0E0;
  }
}
```

### Menu Items

```scss
.menu-list {
  .q-item {
    border-radius: 8px;
    margin: 4px 8px;
    transition: all 200ms ease-out;

    &:hover:not(.q-item--disabled) {
      background-color: rgba($primary-color, 0.05);
    }

    &.active-menu-item {
      background-color: rgba($primary-color, 0.1);
      color: $primary-color;
      font-weight: 600;

      :deep(.q-icon) {
        color: $primary-color;
      }
    }

    &.q-item--disabled {
      opacity: 0.5;
    }
  }
}
```

### Responsive

```scss
@media (max-width: 1023px) {
  .main-drawer {
    .drawer-footer {
      display: none;  // Cache le footer sur mobile
    }
  }
}
```

## Responsive Behavior

### Breakpoints Quasar

| Breakpoint | Taille | Comportement Sidebar |
|------------|--------|---------------------|
| xs | 0-599px | Overlay (swipe pour ouvrir) |
| sm | 600-1023px | Overlay (bouton menu requis) |
| md | 1024-1439px | Visible par défaut |
| lg | 1440-1919px | Visible par défaut |
| xl | 1920px+ | Visible par défaut |

### Classes Utilitaires Responsive

```vue
<!-- Visible uniquement sur écrans > xs (≥ 600px) -->
<div class="gt-xs">
  <div class="text-body2">{{ authStore.userFullName }}</div>
  <div class="text-caption">{{ authStore.userRole }}</div>
</div>
```

**Classes disponibles :**
- `gt-xs` : Affiche sur écrans > xs (≥ 600px)
- `lt-md` : Affiche sur écrans < md (< 1024px)
- `gt-md` : Affiche sur écrans > md (≥ 1024px)

## Intégration avec authStore

Le MainLayout dépend fortement du store d'authentification :

```javascript
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()
```

**Propriétés utilisées :**

| Propriété | Type | Usage |
|-----------|------|-------|
| `authStore.userFullName` | String | Nom complet de l'utilisateur |
| `authStore.userRole` | String | Rôle de l'utilisateur |
| `authStore.user` | Object | Objet utilisateur complet |
| `authStore.user.email` | String | Email de l'utilisateur |
| `authStore.hasAdminRights` | Boolean | Vérifie si SUPERADMIN ou ADMIN |
| `authStore.logout()` | Function | Déconnecte l'utilisateur |

## TODO - Fonctionnalités à Implémenter

### 1. Synchronisation des Données

```javascript
// Créer un store de synchronisation
const useSyncStore = defineStore('sync', {
  state: () => ({
    pendingItems: [],
    isSyncing: false
  }),

  getters: {
    pendingCount: (state) => state.pendingItems.length
  },

  actions: {
    async syncAll() {
      this.isSyncing = true
      try {
        // Envoyer les données en attente
        await Promise.all(
          this.pendingItems.map(item => apiService.sync.upload(item))
        )

        // Récupérer les nouvelles données
        await apiService.sync.download()

        this.pendingItems = []
      } catch (error) {
        console.error('Sync error:', error)
      } finally {
        this.isSyncing = false
      }
    }
  }
})

// Dans MainLayout.vue
const syncStore = useSyncStore()
const pendingSyncCount = computed(() => syncStore.pendingCount)

function handleSync() {
  syncStore.syncAll()
}
```

### 2. Notifications en Temps Réel

```javascript
// Créer un store de notifications
const useNotificationStore = defineStore('notifications', {
  state: () => ({
    items: [],
    unreadCount: 0
  }),

  actions: {
    async fetchNotifications() {
      const response = await apiService.notifications.list()
      this.items = response.data
      this.updateUnreadCount()
    },

    async markAsRead(id) {
      await apiService.notifications.markAsRead(id)
      const notification = this.items.find(n => n.id === id)
      if (notification) {
        notification.read = true
        this.updateUnreadCount()
      }
    },

    async markAllAsRead() {
      await apiService.notifications.markAllAsRead()
      this.items.forEach(n => n.read = true)
      this.updateUnreadCount()
    },

    updateUnreadCount() {
      this.unreadCount = this.items.filter(n => !n.read).length
    }
  }
})

// Dans MainLayout.vue
const notificationStore = useNotificationStore()
const notifications = computed(() => notificationStore.items)
const unreadNotificationsCount = computed(() => notificationStore.unreadCount)

onMounted(() => {
  notificationStore.fetchNotifications()

  // Polling toutes les 30 secondes
  setInterval(() => {
    notificationStore.fetchNotifications()
  }, 30000)
})
```

### 3. Page de Paramètres

Créer `src/pages/SettingsPage.vue` :

```vue
<template>
  <q-page class="settings-page q-pa-md">
    <div class="page-header q-mb-lg">
      <h4 class="page-title">Paramètres</h4>
    </div>

    <div class="row q-col-gutter-md">
      <!-- Configuration générale -->
      <!-- Gestion des utilisateurs -->
      <!-- Configuration des modules -->
      <!-- Paramètres système -->
    </div>
  </q-page>
</template>
```

Ajouter la route dans `routes.js` :

```javascript
{
  path: 'settings',
  name: 'settings',
  component: () => import('pages/SettingsPage.vue'),
  meta: {
    title: 'Paramètres',
    icon: 'settings',
    roles: ['SUPERADMIN', 'ADMIN']
  }
}
```

Ajouter un guard de rôle dans `router/index.js` :

```javascript
Router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiredRoles = to.meta.roles

  if (requiredRoles && !requiredRoles.includes(authStore.userRole)) {
    $q.notify({
      type: 'negative',
      message: 'Accès non autorisé'
    })
    next('/dashboard')
  } else {
    next()
  }
})
```

### 4. Page d'Aide

Créer `src/pages/HelpPage.vue` avec :
- Guide d'utilisation de chaque module
- Vidéos tutoriels
- FAQ
- Contact support

## Tests Recommandés

### Test 1 : Navigation

```
1. Se connecter avec un utilisateur standard
2. Vérifier que "Paramètres" n'est PAS visible dans le menu utilisateur
3. Se connecter avec un admin
4. Vérifier que "Paramètres" EST visible
5. Cliquer sur chaque menu de navigation
6. Vérifier que l'item actif est bien surligné
```

### Test 2 : Notifications

```
1. Charger la page avec des notifications non lues
2. Vérifier que le badge affiche le bon nombre
3. Ouvrir le panneau de notifications
4. Cliquer sur une notification
5. Vérifier qu'elle passe à l'état "lu" (fond blanc)
6. Vérifier que le compteur diminue de 1
7. Cliquer sur "Tout marquer comme lu"
8. Vérifier que toutes les notifications sont marquées lues
9. Vérifier que le badge disparaît
```

### Test 3 : Déconnexion

```
1. Cliquer sur "Se déconnecter"
2. Vérifier que le dialog de confirmation s'affiche
3. Cliquer sur "Annuler"
4. Vérifier qu'on reste sur la page
5. Cliquer à nouveau sur "Se déconnecter"
6. Cliquer sur "Déconnexion"
7. Vérifier la notification de succès
8. Vérifier la redirection vers /auth/login
9. Vérifier que localStorage est vidé
```

### Test 4 : Responsive

```
1. Ouvrir l'application sur desktop (>1024px)
2. Vérifier que la sidebar est visible par défaut
3. Réduire la fenêtre à 800px
4. Vérifier que la sidebar disparaît
5. Cliquer sur le bouton menu
6. Vérifier que la sidebar s'affiche en overlay
7. Cliquer en dehors
8. Vérifier que la sidebar se ferme
9. Tester sur mobile réel (< 600px)
10. Vérifier que le nom/rôle utilisateur disparaît (gt-xs)
```

## Ressources

- [Quasar Layout Documentation](https://quasar.dev/layout/layout)
- [Quasar Drawer Documentation](https://quasar.dev/layout/drawer)
- [Quasar Dialog Documentation](https://quasar.dev/quasar-plugins/dialog)
- [Vue Router Navigation Guards](https://router.vuejs.org/guide/advanced/navigation-guards.html)

## Changelog

**v1.0.0 - 2025-11-14**
- ✅ Header avec logo, sync, notifications, user menu
- ✅ Sidebar avec navigation (Dashboard actif)
- ✅ Menu utilisateur avec profil, paramètres (admin), aide, déconnexion
- ✅ Panneau de notifications avec gestion read/unread
- ✅ Déconnexion avec confirmation
- ✅ Design responsive
- ⏸️ Synchronisation des données (à implémenter)
- ⏸️ Notifications temps réel (à implémenter)
- ⏸️ Page de paramètres (à créer)
- ⏸️ Page d'aide (à créer)
