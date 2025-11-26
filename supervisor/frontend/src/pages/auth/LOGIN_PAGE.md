# Documentation de la Page de Connexion - SUPERVISOR V2.0

## Vue d'ensemble

La page de connexion (`LoginPage.vue`) est le point d'entrée de l'application SUPERVISOR V2.0. Elle permet aux utilisateurs de s'authentifier avec leurs identifiants pour accéder à l'application.

## Emplacement

```
frontend/src/pages/auth/LoginPage.vue
```

## URLs d'accès

- Route principale : `/auth/login`
- Alias : `/login` (redirige vers `/auth/login`)

## Fonctionnalités

### 1. Formulaire de Connexion

**Champs disponibles :**

- **Email/Username** :
  - Type : text
  - Validation : minimum 3 caractères, requis
  - Autocomplete : username
  - Icône : person

- **Mot de passe** :
  - Type : password (avec bouton show/hide)
  - Validation : minimum 4 caractères, requis
  - Autocomplete : current-password
  - Icône : lock
  - Bouton de visibilité : visibility/visibility_off

### 2. Validation

**Validation en temps réel :**
- Les champs sont validés lors de la saisie (lazy-rules)
- Le bouton "Se connecter" est désactivé si le formulaire n'est pas valide
- Messages d'erreur affichés sous les champs invalides

**Règles de validation :**
```javascript
// Username/Email
val => !!val || 'Ce champ est requis'
val => val.length >= 3 || 'Minimum 3 caractères'

// Mot de passe
val => !!val || 'Ce champ est requis'
val => val.length >= 4 || 'Minimum 4 caractères'
```

### 3. Gestion des Erreurs

**Types d'erreurs gérées :**

| Code HTTP | Message                                                                 |
|-----------|-------------------------------------------------------------------------|
| **401**   | "Identifiants incorrects. Veuillez réessayer."                         |
| **400**   | Message du backend ou "Données invalides."                             |
| **403**   | "Votre compte est désactivé. Contactez l'administrateur."             |
| **429**   | "Trop de tentatives. Veuillez patienter quelques instants."           |
| **500**   | "Erreur serveur. Veuillez réessayer plus tard."                        |
| **Network** | "Impossible de contacter le serveur. Vérifiez votre connexion internet." |

**Affichage des erreurs :**
- Banner rouge (q-banner) au-dessus du bouton
- Notification Quasar (toast) en haut de l'écran
- Icône d'erreur pour une meilleure visibilité

### 4. États de Chargement

**Pendant la connexion :**
- Bouton "Se connecter" affiche un spinner (q-spinner-dots)
- Tous les champs sont désactivés
- Le bouton "Mot de passe oublié ?" est désactivé

### 5. Redirections

**Après connexion réussie :**
```javascript
// Si l'URL contient un paramètre redirect
/auth/login?redirect=/users → Redirige vers /users

// Sinon, redirige vers la page d'accueil
/auth/login → Redirige vers /
```

**Si déjà connecté :**
```javascript
// Si l'utilisateur essaie d'accéder à /auth/login alors qu'il est déjà connecté
→ Redirige automatiquement vers /
```

## Design System

### Couleurs

Utilise la charte graphique SUPERVISOR :

```scss
$primary-color: #ea1d31;     // Rouge AI Venture
$bg-light: #F5F7F9;          // Fond clair
$text-dark: #263238;         // Texte principal
$text-secondary: #546E7A;    // Texte secondaire
$border-color: #E0E0E0;      // Bordures
```

### Typographie

```scss
.login-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.login-subtitle {
  font-size: 15px;
  font-weight: 400;
}
```

### Animations

```scss
$transition-standard: 200ms ease-out;

// Animation d'entrée de la page
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Layout

**Desktop :**
- Centré verticalement et horizontalement
- Card de 420px de largeur maximale
- Fond dégradé avec pattern subtil
- Ombres et effets de profondeur

**Mobile (< 600px) :**
- Plein écran
- Fond blanc
- Pas d'ombre sur la card
- Logo plus petit
- Titre et subtitle plus petits

### Interactions

**Effets au survol :**
- Card : élévation légère (translateY -2px)
- Bouton de connexion : ombre accentuée
- Champs : bordure primaire au focus

**Effets au clic :**
- Bouton : retour à la position initiale (translateY 0)

## Intégration avec le Store

### Appel du Store d'Authentification

```javascript
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()

async function handleLogin() {
  await authStore.login({
    username: credentials.value.username,
    password: credentials.value.password
  })
}
```

### Flux d'Authentification

```
1. User remplit formulaire
   ↓
2. Validation des champs
   ↓
3. handleLogin() appelé
   ↓
4. authStore.login(credentials)
   ↓
5. apiService.auth.login() → Backend /api/auth/login/
   ↓
6. Backend retourne { access, refresh, user }
   ↓
7. Store sauvegarde tokens dans localStorage
   ↓
8. Notification de succès
   ↓
9. Redirection vers la page demandée
```

## Navigation Guards

### Protection des Routes

Le router vérifie automatiquement si l'utilisateur est connecté :

```javascript
// router/index.js
Router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

  if (requiresAuth && !authStore.isAuthenticated) {
    next({
      path: '/auth/login',
      query: { redirect: to.fullPath }
    })
  } else if (to.path === '/auth/login' && authStore.isAuthenticated) {
    next(to.query.redirect || '/')
  } else {
    next()
  }
})
```

### Scénarios de Navigation

**Utilisateur non connecté accède à une route protégée :**
```
/users → /auth/login?redirect=/users
```

**Utilisateur connecté accède à /auth/login :**
```
/auth/login → /
```

**Après connexion réussie avec redirect :**
```
/auth/login?redirect=/dashboard → /dashboard
```

## Logo AI Venture

### Implémentation Actuelle

La page utilise un placeholder en attendant le logo officiel :

```vue
<div v-if="logoExists">
  <img src="~assets/aiventure.jpg" alt="AI Venture" class="logo" />
</div>
<div v-else class="logo-placeholder">
  <q-icon name="business" size="64px" color="primary" />
</div>
```

### Ajout du Logo

Pour ajouter le logo officiel :

1. **Placer l'image** dans `frontend/src/assets/aiventure.jpg`
2. **Mettre à jour la fonction** `checkLogoExists()` dans LoginPage.vue :
   ```javascript
   function checkLogoExists() {
     logoExists.value = true
   }
   ```

**Formats recommandés :**
- JPG, PNG ou SVG
- Dimensions recommandées : 400x200px (ratio 2:1)
- Poids : < 100 KB

## Accessibilité

### Conformité WCAG

- **Labels explicites** : Tous les champs ont des labels clairs
- **Autocomplete** : Attributs autocomplete pour faciliter la saisie
- **Contraste** : Ratio de contraste conforme WCAG AA
- **Navigation clavier** : Tous les éléments sont accessibles au clavier
- **Annonces** : Messages d'erreur annoncés aux lecteurs d'écran

### Attributs ARIA (via Quasar)

Quasar ajoute automatiquement les attributs ARIA nécessaires :
- `aria-label`
- `aria-required`
- `aria-invalid`
- `aria-describedby`

## Mode Développement

### Auto-fill (Optionnel)

Pour faciliter les tests en développement :

```javascript
// .env
AUTO_FILL_LOGIN=true

// LoginPage.vue
onMounted(() => {
  if (process.env.DEV && process.env.AUTO_FILL_LOGIN) {
    credentials.value.username = 'admin'
    credentials.value.password = ''
  }
})
```

### Logs de Debug

En mode développement, les logs suivants sont affichés :

```javascript
console.log('✅ Connexion réussie')
console.log('📦 Token sauvegardé dans localStorage')
console.log('🔒 Prochaines requêtes auront automatiquement le token')
```

## Tests Recommandés

### Tests Manuels

1. **Connexion réussie**
   - Entrer identifiants valides
   - Vérifier redirection vers /
   - Vérifier notification de succès

2. **Connexion échouée**
   - Entrer identifiants invalides
   - Vérifier message d'erreur
   - Vérifier que le formulaire reste accessible

3. **Validation des champs**
   - Laisser les champs vides
   - Entrer moins de 3 caractères pour username
   - Vérifier que le bouton est désactivé

4. **Show/Hide Password**
   - Cliquer sur l'icône de visibilité
   - Vérifier le changement de type (text/password)

5. **Mot de passe oublié**
   - Cliquer sur "Mot de passe oublié ?"
   - Vérifier la notification info

6. **Redirection après connexion**
   - Accéder à /auth/login?redirect=/users
   - Se connecter
   - Vérifier redirection vers /users

7. **Utilisateur déjà connecté**
   - Se connecter
   - Essayer d'accéder à /auth/login
   - Vérifier redirection automatique vers /

8. **Responsive**
   - Tester sur desktop (1920x1080)
   - Tester sur tablet (768x1024)
   - Tester sur mobile (375x667)

### Tests Automatisés (Cypress - À implémenter)

```javascript
describe('Login Page', () => {
  it('should display login form', () => {
    cy.visit('/auth/login')
    cy.get('input[type="text"]').should('be.visible')
    cy.get('input[type="password"]').should('be.visible')
    cy.get('button[type="submit"]').should('be.visible')
  })

  it('should login successfully', () => {
    cy.visit('/auth/login')
    cy.get('input[type="text"]').type('admin')
    cy.get('input[type="password"]').type('password123')
    cy.get('button[type="submit"]').click()
    cy.url().should('eq', Cypress.config().baseUrl + '/')
  })

  it('should show error on invalid credentials', () => {
    cy.visit('/auth/login')
    cy.get('input[type="text"]').type('invalid')
    cy.get('input[type="password"]').type('wrong')
    cy.get('button[type="submit"]').click()
    cy.contains('Identifiants incorrects').should('be.visible')
  })
})
```

## Dépendances

### Vue 3
- Composition API (script setup)
- Reactive refs
- Computed properties
- Lifecycle hooks (onMounted)

### Quasar Components
- q-page
- q-card
- q-form
- q-input
- q-btn
- q-icon
- q-banner
- q-spinner-dots
- Notify plugin

### Vue Router
- useRouter (navigation programmatique)
- useRoute (accès aux paramètres de route)

### Pinia
- useAuthStore (gestion d'état authentification)

## Performance

### Optimisations

1. **Lazy Loading** : La page est chargée à la demande (route-level code splitting)
2. **Validation Lazy** : Validation déclenchée seulement après interaction
3. **Debounce** : Pas de debounce nécessaire (formulaire simple)
4. **Images Optimisées** : Logo chargé uniquement si disponible

### Métriques Cibles

- **First Contentful Paint** : < 1s
- **Time to Interactive** : < 2s
- **Bundle Size** : ~15-20 KB (page seule)

## Sécurité

### Bonnes Pratiques Implémentées

1. **Autocomplete** : Utilise les attributs standards (username, current-password)
2. **Masquage du mot de passe** : Par défaut en type password
3. **Pas de stockage en clair** : Les tokens sont gérés par le store
4. **HTTPS requis** : En production (configuré côté serveur)
5. **Protection CSRF** : Gérée par Django (tokens JWT)
6. **Rate Limiting** : Géré côté backend (erreur 429)

### Ce qui N'est PAS fait (et ne devrait pas l'être côté client)

- ❌ Validation de la force du mot de passe (login, pas registration)
- ❌ Captcha (à implémenter côté backend si nécessaire)
- ❌ 2FA (fonctionnalité future)

## Évolutions Futures

### À Court Terme

1. **Ajouter le logo officiel** AI Venture
2. **Implémenter "Mot de passe oublié"**
3. **Ajouter une page d'inscription** (si nécessaire)

### À Moyen Terme

4. **Support 2FA** (Two-Factor Authentication)
5. **Remember Me** (rester connecté)
6. **Social Login** (Google, Microsoft)

### À Long Terme

7. **Biométrie** (empreinte, FaceID) pour mobile
8. **SSO** (Single Sign-On) pour entreprises

## Dépannage

### Problème : "Impossible de contacter le serveur"

**Cause** : Backend Django non démarré ou problème de CORS

**Solution** :
1. Vérifier que le backend est lancé : `python manage.py runserver`
2. Vérifier CORS dans Django settings.py
3. Vérifier API_BASE_URL dans constants.js

### Problème : "Identifiants incorrects" même avec bons identifiants

**Cause** : Endpoint d'authentification incorrect ou utilisateur n'existe pas

**Solution** :
1. Vérifier l'endpoint : `http://localhost:8000/api/auth/login/`
2. Créer un superuser : `python manage.py createsuperuser`
3. Vérifier les logs backend Django

### Problème : Redirection infinie entre / et /auth/login

**Cause** : Store d'authentification non initialisé ou tokens corrompus

**Solution** :
1. Vider localStorage : `localStorage.clear()`
2. Actualiser la page
3. Se reconnecter

### Problème : Page blanche au chargement

**Cause** : Erreur JavaScript ou dépendance manquante

**Solution** :
1. Ouvrir la console développeur (F12)
2. Vérifier les erreurs
3. Relancer `npm install`
4. Redémarrer le serveur de dev : `quasar dev`

## Ressources

- [Documentation Vue 3](https://vuejs.org/)
- [Documentation Quasar](https://quasar.dev/)
- [Documentation Pinia](https://pinia.vuejs.org/)
- [Documentation Vue Router](https://router.vuejs.org/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
