# Charte Graphique SUPERVISOR V2.0

Documentation complète du système de design et des styles SCSS pour l'application SUPERVISOR V2.0.

## 📁 Structure des Fichiers

```
src/css/
├── variables.scss        # Toutes les variables de design (couleurs, espacements, etc.)
├── typography.scss       # Hiérarchie typographique et styles de texte
├── animations.scss       # Transitions, keyframes et animations
├── app.scss             # Fichier principal avec imports et utilitaires
└── quasar.variables.scss # Variables Quasar (couleurs de marque)
```

## 🎨 Palette de Couleurs

### Couleurs Primaires
| Variable | Valeur | Usage |
|----------|--------|-------|
| `$primary` | #ea1d31 | Rouge de marque AIV |
| `$secondary` | #cc4b5a | Rose saumon |
| `$accent` | #00BFA5 | Bleu sarcelle (teal) |

### Couleurs Fonctionnelles
| Variable | Valeur | Usage |
|----------|--------|-------|
| `$success` | #43A047 | Messages de succès |
| `$error` | #E53935 | Messages d'erreur |
| `$warning` | #FFD54F | Avertissements |
| `$info` | #31CCEC | Informations |

### Couleurs de Fond
| Variable | Valeur | Usage |
|----------|--------|-------|
| `$bg-white` | #FFFFFF | Fond blanc principal |
| `$bg-light` | #F5F7F9 | Gris clair |
| `$bg-dark` | #263238 | Gris foncé (mode sombre) |

## 📏 Système d'Espacement

Basé sur un multiple de 4dp :

```scss
$space-micro: 4px;     // Micro espacement
$space-xs: 8px;        // Très petit
$space-sm: 12px;       // Petit
$space-base: 16px;     // Défaut
$space-md: 24px;       // Moyen
$space-lg: 32px;       // Grand
$space-xl: 48px;       // Très grand
$space-2xl: 64px;      // Énorme
```

### Classes Utilitaires d'Espacement

**Margins :**
- `.m-{size}` : margin sur tous les côtés
- `.mt-{size}`, `.mb-{size}`, `.ml-{size}`, `.mr-{size}` : margin top/bottom/left/right
- `.mx-{size}` : margin horizontal
- `.my-{size}` : margin vertical

**Paddings :**
- `.p-{size}` : padding sur tous les côtés
- `.pt-{size}`, `.pb-{size}`, `.pl-{size}`, `.pr-{size}` : padding top/bottom/left/right
- `.px-{size}` : padding horizontal
- `.py-{size}` : padding vertical

Tailles disponibles : `0, xs, sm, base, md, lg, xl`

## ✍️ Typographie

### Hiérarchie des Titres

```scss
H1 : 28px / Bold (700)
H2 : 24px / Bold (700)
H3 : 20px / Semi-bold (600)
H4 : 18px / Semi-bold (600)
```

### Corps de Texte

```scss
Body Large : 17px / Regular (400)
Body : 15px / Regular (400)
Small : 13px / Regular (400)
Caption : 12px / Regular (400)
```

### Classes de Texte

```html
<!-- Titres -->
<h1>Titre H1</h1>
<div class="h2">Titre H2</div>
<p class="text-h3">Titre H3</p>

<!-- Corps -->
<p class="text-body-large">Corps large</p>
<p class="text-body">Corps normal</p>
<p class="text-small">Petit texte</p>
<p class="text-caption">Légende</p>

<!-- Poids -->
<p class="font-light">Texte léger</p>
<p class="font-bold">Texte gras</p>

<!-- Couleurs -->
<p class="text-primary">Texte primaire</p>
<p class="text-brand">Texte rouge AIV</p>
<p class="text-success">Texte vert</p>
```

## 🎬 Animations

### Durées

```scss
$duration-fast: 150ms      // Micro-interactions
$duration-base: 200ms      // Standard
$duration-medium: 300ms    // Accent
$duration-slow: 400ms      // Lent
```

### Fonctions d'Ease

```scss
$ease-out: ease-out
$ease-in-out: ease-in-out
$ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1)
$ease-emphasized: cubic-bezier(0.0, 0, 0.2, 1)
```

### Classes d'Animation

```html
<!-- Fade -->
<div class="animate-fade-in">Apparition en fondu</div>
<div class="animate-fade-out">Disparition en fondu</div>

<!-- Slide -->
<div class="animate-slide-in-left">Glissement depuis la gauche</div>
<div class="animate-slide-in-right">Glissement depuis la droite</div>

<!-- Scale -->
<div class="animate-scale-in">Zoom entrant</div>
<div class="animate-pulse">Pulsation</div>

<!-- Rotation -->
<div class="animate-spin">Rotation continue</div>

<!-- États interactifs -->
<button class="hover-elevate">Bouton avec élévation</button>
<button class="hover-scale">Bouton avec scale</button>
```

## 🧩 Composants

### Boutons

```scss
// Dimensions
$button-height: 48px
$button-height-small: 36px
$button-height-large: 56px
$button-padding-x: 24px
$border-radius-button: 8px
```

```html
<button class="btn btn-primary">Bouton primaire</button>
<button class="btn btn-secondary">Bouton secondaire</button>
<button class="btn btn-outline">Bouton outlined</button>
```

### Cartes

```scss
// Dimensions
$card-padding: 16px
$border-radius-card: 12px
$shadow-card: 0 2px 4px rgba(0, 0, 0, 0.1)
```

```html
<div class="card-container">
  <h3>Titre de carte</h3>
  <p>Contenu de la carte</p>
</div>

<div class="card-container card-elevated">Carte élevée</div>
<div class="card-container card-flat">Carte plate</div>
```

### Champs de Saisie

```scss
$input-height: 56px
$input-padding-x: 16px
$border-radius-input: 8px
```

## 🌓 Mode Sombre

Le mode sombre est automatiquement appliqué quand la classe `body--dark` est ajoutée au `<body>`.

```scss
// Variables Mode Sombre
$dark-bg-primary: #121212
$dark-bg-secondary: #1E1E1E
$dark-text-primary: #FFFFFF
$dark-text-secondary: #B0B0B0
```

## 🛠️ Classes Utilitaires

### Display

```html
<div class="d-flex">Display flex</div>
<div class="d-grid">Display grid</div>
<div class="d-none">Caché</div>
```

### Flexbox

```html
<div class="d-flex justify-center align-center">
  Contenu centré
</div>

<div class="d-flex justify-between">
  <div>Gauche</div>
  <div>Droite</div>
</div>
```

### Borders & Shadows

```html
<div class="border rounded">Avec bordure arrondie</div>
<div class="shadow-md">Avec ombre</div>
<div class="rounded-lg shadow-lg">Grande bordure et ombre</div>
```

### Backgrounds

```html
<div class="bg-white">Fond blanc</div>
<div class="bg-primary text-white">Fond rouge</div>
<div class="bg-accent">Fond teal</div>
```

## 📱 Responsive

Breakpoints :

```scss
$breakpoint-xs: 0       // Mobile
$breakpoint-sm: 600px   // Tablette portrait
$breakpoint-md: 960px   // Tablette paysage
$breakpoint-lg: 1280px  // Desktop
$breakpoint-xl: 1920px  // Large desktop
```

## 💡 Exemples d'Usage

### Exemple 1 : Page avec Header et Contenu

```vue
<template>
  <div class="page-container bg-light">
    <div class="container">
      <h1 class="text-h1 text-brand mb-md">Mon Titre</h1>

      <div class="card-container mb-base">
        <h2 class="text-h3 mb-sm">Section</h2>
        <p class="text-body">Contenu de la section</p>
      </div>

      <button class="btn btn-primary hover-elevate">
        Action Principale
      </button>
    </div>
  </div>
</template>
```

### Exemple 2 : Liste avec Animations

```vue
<template>
  <div class="d-flex flex-column">
    <div
      v-for="item in items"
      :key="item.id"
      class="card-container mb-sm animate-fade-in-up"
    >
      <h3 class="text-h4 mb-xs">{{ item.title }}</h3>
      <p class="text-body text-secondary">{{ item.description }}</p>
    </div>
  </div>
</template>
```

### Exemple 3 : Formulaire Stylisé

```vue
<template>
  <form class="p-md bg-white rounded-lg shadow-md">
    <h2 class="text-h2 mb-md">Connexion</h2>

    <div class="mb-base">
      <label class="text-body font-medium mb-xs d-block">Email</label>
      <input
        type="email"
        class="w-full border rounded px-base py-sm"
      />
    </div>

    <button
      type="submit"
      class="btn btn-primary w-full transition-accent"
    >
      Se connecter
    </button>
  </form>
</template>
```

## 🔧 Mixins Disponibles

### Typography

```scss
// Créer un style de titre personnalisé
@include heading(20px, $font-weight-bold);

// Créer un style de corps de texte
@include body-text(15px, $font-weight-regular);

// Tronquer sur plusieurs lignes
@include truncate-lines(3);
```

### Animations

```scss
// Transition personnalisée
@include custom-transition(opacity transform, 300ms, $ease-out);

// Animation avec keyframes
@include animate(fadeIn, 200ms, $ease-out);
```

## ⚡ Performance

### Optimisations Appliquées

1. **Préférence réduite de mouvement** : Les animations sont réduites pour les utilisateurs ayant activé cette préférence d'accessibilité
2. **Will-change** : Utilisé avec parcimonie pour améliorer les performances d'animation
3. **Transform/Opacity** : Privilégiés pour les animations GPU-accelerated

### Best Practices

- Utiliser `transform` plutôt que `top/left` pour les animations
- Préférer `opacity` pour les effets de fondu
- Limiter l'utilisation de `box-shadow` dans les animations
- Utiliser `will-change` uniquement quand nécessaire

## 📚 Ressources

- [Quasar Framework Docs](https://quasar.dev)
- [SASS Documentation](https://sass-lang.com/documentation)
- [Material Design Guidelines](https://material.io/design)

---

**Version** : 2.0.0
**Dernière mise à jour** : 2025-11-12
**Mainteneur** : Équipe SUPERVISOR AIV
