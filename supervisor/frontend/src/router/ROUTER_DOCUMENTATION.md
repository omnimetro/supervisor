# Documentation du Router - SUPERVISOR V2.0

Ce document décrit la configuration complète du router Vue Router pour l'application SUPERVISOR.

## Vue d'ensemble

Le router est configuré avec :
- **Navigation guards** pour l'authentification
- **Lazy loading** des composants pour optimiser les performances
- **Méta-données** des routes pour le titre, icônes, et permissions
- **Redirection automatique** selon l'état d'authentification

## Structure des Fichiers

```
src/router/
├── index.js           # Configuration principale du router + guards
├── routes.js          # Définition de toutes les routes
└── ROUTER_DOCUMENTATION.md  # Ce fichier
```

## Configuration Principale (`index.js`)

### Création du Router

```javascript
import { defineRouter } from '#q-app/wrappers'
import { useAuthStore } from 'src/stores/auth'

export default defineRouter(function () {
  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createWebHistory(process.env.VUE_ROUTER_BASE)
  })

  // Navigation Guards
  Router.beforeEach((to, from, next) => {
    // ... (voir ci-dessous)
  })

  return Router
})
```

### Navigation Guards

#### Guard `beforeEach`

Vérifie l'authentification avant chaque navigation :

```javascript
Router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Vérifier si la route nécessite une authentification
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

  if (requiresAuth && !authStore.isAuthenticated) {
    // Rediriger vers login avec l'URL de redirection
    next({
      path: '/auth/login',
      query: { redirect: to.fullPath }
    })
  }
  else if (to.path === '/auth/login' && authStore.isAuthenticated) {
    // Utilisateur déjà connecté, rediriger vers page demandée ou accueil
    next(to.query.redirect || '/')
  }
  else {
    // Autoriser la navigation
    next()
  }
})
```

**Scénarios gérés :**

| Scénario | Action |
|----------|--------|
| Utilisateur non connecté → route protégée | Redirect → `/auth/login?redirect=/route` |
| Utilisateur connecté → `/auth/login` | Redirect → `/` ou query.redirect |
| Route publique | Autoriser |
| Route protégée + authentifié | Autoriser |

#### Guard `afterEach`

Logging des navigations en mode développement :

```javascript
Router.afterEach((to, from) => {
  if (process.env.DEV) {
    console.log('🧭 Navigation:', from.path, '→', to.path)
  }
})
```

## Routes Définies (`routes.js`)

### 1. Routes Publiques (Authentification)

```javascript
{
  path: '/auth',
  component: () => import('layouts/AuthLayout.vue'),
  children: [
    {
      path: 'login',
      name: 'login',
      component: () => import('pages/auth/LoginPage.vue'),
      meta: { requiresAuth: false }
    }
  ]
}
```

**URLs :**
- `/auth/login` - Page de connexion
- `/login` (alias) → redirige vers `/auth/login`

**Caractéristiques :**
- Layout AuthLayout (minimal, sans navigation)
- meta.requiresAuth: false (route publique)

### 2. Routes Protégées (Application Principale)

```javascript
{
  path: '/',
  component: () => import('layouts/MainLayout.vue'),
  meta: { requiresAuth: true },
  children: [
    {
      path: '',
      name: 'home',
      redirect: '/dashboard'
    },
    {
      path: 'dashboard',
      name: 'dashboard',
      component: () => import('pages/DashboardPage.vue'),
      meta: {
        title: 'Tableau de Bord',
        icon: 'dashboard'
      }
    },
    {
      path: 'profile',
      name: 'profile',
      component: () => import('pages/ProfilePage.vue'),
      meta: {
        title: 'Mon Profil',
        icon: 'person'
      }
    }
  ]
}
```

**URLs Actives :**
- `/` → Redirect → `/dashboard`
- `/dashboard` - Tableau de bord
- `/profile` - Profil utilisateur

**Caractéristiques :**
- Layout MainLayout (avec header + sidebar)
- meta.requiresAuth: true (par défaut pour la route parente)
- meta.title: Titre de la page
- meta.icon: Icône pour le menu

### 3. Routes Futures (Commentées)

Routes préparées pour les modules à venir :

**Utilisateurs** (SUPERADMIN/ADMIN uniquement)
```javascript
{
  path: 'users',
  name: 'users',
  component: () => import('pages/users/UsersPage.vue'),
  meta: {
    title: 'Utilisateurs',
    icon: 'people',
    roles: ['SUPERADMIN', 'ADMIN']  // Restriction par rôle
  }
}
```

**Chantiers (Déploiement)**
```javascript
{
  path: 'deployment',
  children: [
    {
      path: '',
      name: 'deployment',
      component: () => import('pages/deployment/ProjectsPage.vue'),
      meta: { title: 'Chantiers', icon: 'construction' }
    },
    {
      path: ':id',
      name: 'deployment-detail',
      component: () => import('pages/deployment/ProjectDetailPage.vue'),
      meta: { title: 'Détail Chantier' }
    }
  ]
}
```

**B2B**
```javascript
{
  path: 'b2b',
  children: [
    {
      path: '',
      name: 'b2b',
      component: () => import('pages/b2b/InterventionsPage.vue'),
      meta: { title: 'B2B', icon: 'business_center' }
    }
  ]
}
```

**Stocks, Dépenses, Cartographie** - Structure similaire

### 4. Page 404

```javascript
{
  path: '/:catchAll(.*)*',
  component: () => import('pages/ErrorNotFound.vue')
}
```

**Caractéristiques :**
- Doit toujours être en dernier dans le tableau des routes
- Capture toutes les URLs non définies
- Affiche ErrorNotFound.vue

## Méta-données des Routes

### Propriétés `meta` Disponibles

| Propriété | Type | Description | Exemple |
|-----------|------|-------------|---------|
| `requiresAuth` | Boolean | Route nécessite authentification | `true` (défaut) / `false` |
| `title` | String | Titre de la page | `"Tableau de Bord"` |
| `icon` | String | Icône Material (pour menu) | `"dashboard"` |
| `roles` | Array | Rôles autorisés | `['SUPERADMIN', 'ADMIN']` |
| `permissions` | Array | Permissions requises | `['users.view']` |

### Exemples d'Utilisation

**Route publique :**
```javascript
{
  path: 'login',
  meta: { requiresAuth: false }
}
```

**Route avec restriction de rôle :**
```javascript
{
  path: 'admin',
  meta: {
    title: 'Administration',
    icon: 'settings',
    roles: ['SUPERADMIN', 'ADMIN']
  }
}
```

**Route avec permissions :**
```javascript
{
  path: 'users',
  meta: {
    permissions: ['users.view', 'users.create']
  }
}
```

## Layouts

### AuthLayout

**Fichier** : `src/layouts/AuthLayout.vue`

**Utilisé pour** :
- Page de connexion
- Page d'inscription (future)
- Réinitialisation mot de passe (future)

**Caractéristiques** :
- Pas de header
- Pas de sidebar
- Fond plein écran
- Contenu centré

### MainLayout

**Fichier** : `src/layouts/MainLayout.vue`

**Utilisé pour** :
- Dashboard
- Profil
- Toutes les pages de l'application

**Composants** :
- **Header** :
  - Logo "SUPERVISOR V2.0"
  - Bouton menu (toggle sidebar)
  - Menu utilisateur (avatar + dropdown)
    - Mon Profil
    - Déconnexion

- **Sidebar** (260px) :
  - Header dégradé rouge
  - Menu de navigation :
    - Dashboard (actif)
    - Chantiers (désactivé pour l'instant)
    - B2B (désactivé)
    - Stocks (désactivé)
    - Dépenses (désactivé)
    - Cartographie (désactivé)
    - Administration (si SUPERADMIN/ADMIN)
  - Footer avec copyright

- **Page Container** :
  - `<router-view />` pour afficher le contenu

### Menu de Navigation

**Item actif** :
- Fond primaire léger (#ea1d31 à 10% d'opacité)
- Texte en couleur primaire
- Icône en couleur primaire
- Font-weight: 600

**Items désactivés** (futures fonctionnalités) :
- Opacité: 0.5
- Non cliquables
- Attribut `disable`

**Administration** :
- Visible uniquement si `authStore.hasAdminRights`
- Rôles autorisés : SUPERADMIN, ADMIN

## Navigation Programmatique

### Dans les Composants

```javascript
import { useRouter } from 'vue-router'

const router = useRouter()

// Navigation simple
router.push('/dashboard')

// Navigation avec nom de route
router.push({ name: 'profile' })

// Navigation avec paramètres
router.push({
  name: 'deployment-detail',
  params: { id: 123 }
})

// Navigation avec query
router.push({
  path: '/users',
  query: { page: 2, filter: 'active' }
})

// Remplacer l'entrée d'historique (pas de "back")
router.replace('/login')

// Retour arrière
router.go(-1) // ou router.back()
```

### Dans les Templates

```vue
<!-- Liens simples -->
<router-link to="/dashboard">Dashboard</router-link>

<!-- Avec nom de route -->
<router-link :to="{ name: 'profile' }">Mon Profil</router-link>

<!-- Avec paramètres -->
<router-link :to="{ name: 'deployment-detail', params: { id: project.id } }">
  Voir détails
</router-link>

<!-- Classes actives automatiques -->
<router-link to="/dashboard" active-class="active">
  Dashboard
</router-link>
```

## Gestion de la Déconnexion

### Flux de Déconnexion

```
1. USER CLIQUE SUR "DÉCONNEXION"
   ↓
2. DIALOGUE DE CONFIRMATION (Quasar Dialog)
   Titre: "Déconnexion"
   Message: "Êtes-vous sûr de vouloir vous déconnecter ?"
   Boutons: [Annuler] [Déconnexion]
   ↓
3. SI CONFIRMATION → authStore.logout()
   - Appel API /api/auth/logout/ (blacklist refresh token)
   - storage.clear() (nettoyer localStorage)
   - authStore state réinitialisé
   ↓
4. NOTIFICATION "Déconnexion réussie"
   ↓
5. REDIRECTION → /auth/login
```

### Code Exemple

```javascript
async function handleLogout() {
  $q.dialog({
    title: 'Déconnexion',
    message: 'Êtes-vous sûr de vouloir vous déconnecter ?',
    cancel: { label: 'Annuler', flat: true },
    ok: { label: 'Déconnexion', color: 'negative' },
    persistent: true
  }).onOk(async () => {
    try {
      await authStore.logout()
      $q.notify({
        type: 'info',
        message: 'Déconnexion réussie',
        position: 'top'
      })
      router.push('/auth/login')
    } catch (error) {
      console.error('Erreur déconnexion:', error)
    }
  })
}
```

## Lazy Loading et Code Splitting

Toutes les routes utilisent le lazy loading pour optimiser les performances :

```javascript
// Route avec lazy loading
{
  path: 'dashboard',
  component: () => import('pages/DashboardPage.vue')
}

// Résultat : chunks séparés au build
// - chunk-vendors.js (dépendances)
// - app.js (code principal)
// - DashboardPage.[hash].js (chargé à la demande)
```

**Avantages** :
- Bundle initial plus petit
- Temps de chargement initial réduit
- Chargement des pages à la demande

## Guards Avancés (Future)

### Guard de Vérification des Rôles

```javascript
Router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiredRoles = to.meta.roles

  if (requiredRoles && !requiredRoles.includes(authStore.userRole)) {
    next('/unauthorized')
  } else {
    next()
  }
})
```

### Guard de Vérification des Permissions

```javascript
Router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiredPermissions = to.meta.permissions

  if (requiredPermissions) {
    const hasAllPermissions = requiredPermissions.every(
      perm => authStore.hasPermission(perm)
    )

    if (!hasAllPermissions) {
      next('/forbidden')
    } else {
      next()
    }
  } else {
    next()
  }
})
```

## Scroll Behavior

Comportement configuré : retour en haut de page à chaque navigation.

```javascript
const Router = createRouter({
  scrollBehavior: () => ({ left: 0, top: 0 }),
  routes
})
```

**Personnalisation possible :**

```javascript
scrollBehavior(to, from, savedPosition) {
  // Si navigation "back", revenir à la position sauvegardée
  if (savedPosition) {
    return savedPosition
  }

  // Si ancre dans l'URL (#section), scroller vers l'ancre
  if (to.hash) {
    return { el: to.hash, behavior: 'smooth' }
  }

  // Sinon, retour en haut
  return { left: 0, top: 0 }
}
```

## Tests Recommandés

### Test 1 : Navigation Publique/Protégée
```
1. Ouvrir /dashboard (non connecté) → Redirect → /auth/login?redirect=/dashboard
2. Se connecter → Redirect → /dashboard
3. Accéder à /profile → OK
4. Se déconnecter → Redirect → /auth/login
5. Essayer /profile (non connecté) → Redirect → /auth/login?redirect=/profile
```

### Test 2 : Lazy Loading
```
1. Ouvrir DevTools → Network
2. Charger l'application
3. Naviguer vers /dashboard
4. Vérifier qu'un nouveau chunk est chargé (DashboardPage.[hash].js)
5. Naviguer vers /profile
6. Vérifier qu'un nouveau chunk est chargé (ProfilePage.[hash].js)
```

### Test 3 : Déconnexion
```
1. Se connecter
2. Cliquer sur avatar → Déconnexion
3. Vérifier dialogue de confirmation
4. Annuler → rester sur la page
5. Cliquer Déconnexion à nouveau → Confirmer
6. Vérifier notification "Déconnexion réussie"
7. Vérifier redirection vers /auth/login
8. Vérifier localStorage vidé
```

### Test 4 : Menu de Navigation
```
1. Se connecter
2. Vérifier highlight sur "Tableau de Bord"
3. Cliquer sur avatar → Mon Profil
4. Vérifier changement de page
5. Vérifier highlight disparu de Dashboard
6. Retour Dashboard via menu
7. Vérifier highlight restauré
```

## Dépannage

### Problème : Redirect Loop Infini

**Cause** : Guard mal configuré ou state d'authentification incohérent

**Solution** :
```javascript
// Vérifier qu'il n'y a pas de boucle dans les guards
if (requiresAuth && !authStore.isAuthenticated) {
  // S'assurer de ne pas rediriger si déjà sur /auth/login
  if (to.path !== '/auth/login') {
    next('/auth/login')
  } else {
    next()
  }
}
```

### Problème : Page 404 au Refresh

**Cause** : Mode history sans configuration serveur

**Solution** : Configurer le serveur pour servir `index.html` pour toutes les routes

**Django** :
```python
# urls.py
from django.views.generic import TemplateView

urlpatterns = [
    # ... autres URLs
    path('', TemplateView.as_view(template_name='index.html')),
]
```

### Problème : Lazy Loading Échoue

**Cause** : Chunk non trouvé ou erreur dans le composant

**Solution** : Vérifier la console pour les erreurs de chargement

```javascript
// Ajouter error handling
{
  path: 'dashboard',
  component: () => import('pages/DashboardPage.vue')
    .catch(err => {
      console.error('Failed to load Dashboard:', err)
      return import('pages/ErrorPage.vue')
    })
}
```

## Ressources

- [Vue Router Documentation](https://router.vuejs.org/)
- [Quasar Router Integration](https://quasar.dev/quasar-cli-vite/routing)
- [Navigation Guards Guide](https://router.vuejs.org/guide/advanced/navigation-guards.html)
- [Lazy Loading Routes](https://router.vuejs.org/guide/advanced/lazy-loading.html)
