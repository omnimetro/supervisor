<template>
  <q-page class="login-page">
    <div class="login-container">
      <!-- Logo AI Venture -->
      <div class="logo-container">
        <img
          :src="logoAiVenture"
          alt="AI Venture"
          class="logo"
        />
      </div>

      <!-- Titre -->
      <div class="login-header">
        <h1 class="login-title">Connexion à Supervisor</h1>
        <p class="login-subtitle">Gestion des chantiers AI Venture</p>
      </div>

      <!-- Formulaire de connexion -->
      <q-card class="login-card" flat bordered>
        <q-card-section>
          <q-form @submit.prevent="handleLogin" class="login-form">
            <!-- Champ Email/Username -->
            <q-input
              v-model="credentials.username"
              type="text"
              label="Email ou nom d'utilisateur"
              outlined
              autocomplete="username"
              :rules="[
                val => !!val || 'Ce champ est requis',
                val => val.length >= 3 || 'Minimum 3 caractères'
              ]"
              lazy-rules
              :disable="loading"
              class="q-mb-md"
            >
              <template v-slot:prepend>
                <q-icon name="person" color="primary" />
              </template>
            </q-input>

            <!-- Champ Mot de passe -->
            <q-input
              v-model="credentials.password"
              :type="showPassword ? 'text' : 'password'"
              label="Mot de passe"
              outlined
              autocomplete="current-password"
              :rules="[
                val => !!val || 'Ce champ est requis',
                val => val.length >= 4 || 'Minimum 4 caractères'
              ]"
              lazy-rules
              :disable="loading"
              class="q-mb-sm"
              @keyup.enter="handleLogin"
            >
              <template v-slot:prepend>
                <q-icon name="lock" color="primary" />
              </template>
              <template v-slot:append>
                <q-icon
                  :name="showPassword ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  color="grey-6"
                  @click="showPassword = !showPassword"
                />
              </template>
            </q-input>

            <!-- Lien Mot de passe oublié -->
            <div class="row justify-end q-mb-md">
              <q-btn
                flat
                dense
                no-caps
                label="Mot de passe oublié ?"
                color="primary"
                size="sm"
                class="forgot-password-btn"
                :disable="loading"
                @click="handleForgotPassword"
              />
            </div>

            <!-- Message d'erreur -->
            <q-banner
              v-if="errorMessage"
              class="bg-negative text-white q-mb-md"
              rounded
              dense
            >
              <template v-slot:avatar>
                <q-icon name="error" color="white" />
              </template>
              {{ errorMessage }}
            </q-banner>

            <!-- Bouton Se connecter -->
            <q-btn
              type="submit"
              label="Se connecter"
              color="primary"
              size="lg"
              class="full-width login-btn"
              :loading="loading"
              :disable="loading || !isFormValid"
              unelevated
              no-caps
            >
              <template v-slot:loading>
                <q-spinner-dots color="white" />
              </template>
            </q-btn>
          </q-form>
        </q-card-section>
      </q-card>

      <!-- Footer -->
      <div class="login-footer">
        <p class="text-grey-6">
          SUPERVISOR V2.0 &copy; {{ currentYear }} AI Venture
        </p>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import logoAiVenture from 'src/assets/aiventure.jpg'

// ============================================
// Composables et Stores
// ============================================

const router = useRouter()
const route = useRoute()
const $q = useQuasar()
const authStore = useAuthStore()

// ============================================
// State
// ============================================

const credentials = ref({
  username: '',
  password: ''
})

const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const logoExists = ref(true)
const currentYear = new Date().getFullYear()

// ============================================
// Computed
// ============================================

/**
 * Vérifie si le formulaire est valide
 */
const isFormValid = computed(() => {
  return (
    credentials.value.username.length >= 3 &&
    credentials.value.password.length >= 4
  )
})

// ============================================
// Methods
// ============================================

/**
 * Gère la soumission du formulaire de connexion
 */
async function handleLogin() {
  // Validation finale
  if (!isFormValid.value) {
    return
  }

  // Réinitialiser le message d'erreur
  errorMessage.value = ''
  loading.value = true

  try {
    // Appel du store d'authentification
    await authStore.login({
      username: credentials.value.username,
      password: credentials.value.password
    })

    // Notification de succès
    $q.notify({
      type: 'positive',
      message: `Bienvenue ${authStore.userFullName || authStore.user?.username} !`,
      caption: 'Connexion réussie',
      position: 'top',
      timeout: 2000,
      icon: 'check_circle'
    })

    // Attendre que Vue mette à jour la réactivité avant la redirection
    await nextTick()

    // Redirection vers le dashboard
    const redirectTo = route.query.redirect || '/dashboard'
    await router.push(redirectTo)
  } catch (error) {
    // Gestion des erreurs
    console.error('Erreur de connexion:', error)

    // Message d'erreur personnalisé selon le type d'erreur
    if (error.response) {
      switch (error.response.status) {
        case 401:
          errorMessage.value = 'Identifiants incorrects. Veuillez réessayer.'
          break
        case 400:
          errorMessage.value = error.response.data?.detail || 'Données invalides.'
          break
        case 403:
          errorMessage.value = 'Votre compte est désactivé. Contactez l\'administrateur.'
          break
        case 429:
          errorMessage.value = 'Trop de tentatives. Veuillez patienter quelques instants.'
          break
        case 500:
          errorMessage.value = 'Erreur serveur. Veuillez réessayer plus tard.'
          break
        default:
          errorMessage.value = 'Une erreur est survenue. Veuillez réessayer.'
      }
    } else if (error.request) {
      errorMessage.value = 'Impossible de contacter le serveur. Vérifiez votre connexion internet.'
    } else {
      errorMessage.value = 'Une erreur inattendue est survenue.'
    }

    // Notification d'erreur
    $q.notify({
      type: 'negative',
      message: errorMessage.value,
      position: 'top',
      timeout: 4000,
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}

/**
 * Gère le clic sur "Mot de passe oublié"
 * (Non fonctionnel pour l'instant)
 */
function handleForgotPassword() {
  $q.notify({
    type: 'info',
    message: 'Fonctionnalité bientôt disponible',
    caption: 'Contactez l\'administrateur pour réinitialiser votre mot de passe',
    position: 'top',
    timeout: 3000,
    icon: 'info'
  })
}

/**
 * Vérifie si le logo existe
 */
function checkLogoExists() {
  // Pour l'instant, le logo n'existe pas
  // Quand il sera ajouté, cette fonction pourra vérifier son existence
  logoExists.value = false
}

// ============================================
// Lifecycle
// ============================================

onMounted(() => {
  // Vérifier si l'utilisateur est déjà connecté
  if (authStore.isAuthenticated) {
    router.push('/')
  }

  // Vérifier l'existence du logo
  checkLogoExists()

  // Pré-remplir le username en mode développement (optionnel)
  if (process.env.DEV && process.env.AUTO_FILL_LOGIN) {
    credentials.value.username = 'admin'
    credentials.value.password = ''
  }
})
</script>

<style lang="scss" scoped>
// ============================================
// Variables (depuis le design system)
// ============================================

$primary-color: #ea1d31;
$bg-light: #F5F7F9;
$text-dark: #263238;
$text-secondary: #546E7A;
$border-color: #E0E0E0;
$shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
$shadow-md: 0 4px 12px rgba(0, 0, 0, 0.15);
$border-radius: 12px;
$transition-standard: 200ms ease-out;

// ============================================
// Layout Principal
// ============================================

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, $bg-light 0%, #ffffff 100%);
  padding: 24px;

  // Pattern de fond subtil
  background-image:
    radial-gradient(circle at 20% 50%, rgba($primary-color, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba($primary-color, 0.03) 0%, transparent 50%);
}

.login-container {
  width: 100%;
  max-width: 420px;
  animation: fadeInUp $transition-standard;
}

// ============================================
// Logo
// ============================================

.logo-container {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  max-width: 180px;
  height: auto;
  transition: transform $transition-standard;

  &:hover {
    transform: scale(1.05);
  }
}

.logo-placeholder {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, rgba($primary-color, 0.1) 0%, rgba($primary-color, 0.05) 100%);
  border-radius: 50%;
  margin: 0 auto;
  transition: transform $transition-standard;

  &:hover {
    transform: scale(1.05);
  }
}

// ============================================
// Header
// ============================================

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: $text-dark;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.login-subtitle {
  font-size: 15px;
  color: $text-secondary;
  margin: 0;
  font-weight: 400;
}

// ============================================
// Card
// ============================================

.login-card {
  border-radius: $border-radius;
  border: 1px solid $border-color;
  box-shadow: $shadow-md;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
  transition: box-shadow $transition-standard, transform $transition-standard;

  &:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    transform: translateY(-2px);
  }
}

// ============================================
// Formulaire
// ============================================

.login-form {
  :deep(.q-field) {
    .q-field__control {
      border-radius: 8px;
      transition: all $transition-standard;

      &:hover {
        border-color: rgba($primary-color, 0.5);
      }
    }

    .q-field__label {
      color: $text-secondary;
      font-weight: 500;
    }

    &.q-field--focused {
      .q-field__control {
        border-color: $primary-color;
        box-shadow: 0 0 0 3px rgba($primary-color, 0.1);
      }
    }
  }

  :deep(.q-icon) {
    transition: color $transition-standard;
  }
}

.forgot-password-btn {
  font-size: 13px;
  transition: all $transition-standard;

  &:hover {
    transform: translateX(2px);
  }
}

// ============================================
// Bouton de connexion
// ============================================

.login-btn {
  height: 48px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: all $transition-standard;
  box-shadow: $shadow-sm;

  &:hover:not(:disabled) {
    box-shadow: 0 4px 12px rgba($primary-color, 0.3);
    transform: translateY(-2px);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.6;
  }
}

// ============================================
// Footer
// ============================================

.login-footer {
  text-align: center;
  margin-top: 24px;

  p {
    font-size: 13px;
    margin: 0;
  }
}

// ============================================
// Animations
// ============================================

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

// ============================================
// Responsive
// ============================================

@media (max-width: 600px) {
  .login-page {
    padding: 16px;
    background: #ffffff;
  }

  .login-container {
    max-width: 100%;
  }

  .login-title {
    font-size: 24px;
  }

  .login-subtitle {
    font-size: 14px;
  }

  .logo {
    max-width: 140px;
  }

  .logo-placeholder {
    width: 100px;
    height: 100px;

    :deep(.q-icon) {
      font-size: 48px;
    }
  }

  .login-card {
    box-shadow: none;
    border: none;
    background: #ffffff;
  }
}

// ============================================
// Dark Mode Support (optionnel)
// ============================================

body.body--dark {
  .login-page {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  }

  .login-title {
    color: #ffffff;
  }

  .login-subtitle {
    color: #b0b0b0;
  }

  .login-card {
    background: rgba(45, 45, 45, 0.95);
    border-color: #404040;
  }

  .login-footer p {
    color: #b0b0b0;
  }
}
</style>
