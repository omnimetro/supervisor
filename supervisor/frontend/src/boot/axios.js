/**
 * Configuration Axios pour SUPERVISOR V2.0
 * Communication avec l'API Django Backend
 *
 * Intercepteurs configurés :
 * - Request : Ajoute automatiquement le token JWT dans les headers
 * - Response : Gère les erreurs d'authentification et refresh automatique du token
 */

import { defineBoot } from '#q-app/wrappers'
import axios from 'axios'
import { Notify } from 'quasar'
import { storage } from 'src/utils/storage'
import { API_BASE_URL, API_TIMEOUT } from 'src/utils/constants'

// Variable pour stocker le router (sera initialisé dans le boot)
let router = null

// ============================================
// Configuration de l'Instance Axios
// ============================================

/**
 * Instance Axios principale pour les appels API
 * Singleton partagé dans toute l'application
 */
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: false // Pas de cookies (utilise JWT)
})

// ============================================
// Intercepteur de Requête (Request)
// ============================================

/**
 * Intercepte toutes les requêtes sortantes pour :
 * - Ajouter automatiquement le token JWT dans les headers Authorization
 * - Logger les requêtes en mode développement
 *
 * Note : Utilise directement storage.getToken() pour éviter les dépendances circulaires
 * avec le store Pinia (le store utilise cette instance axios pour ses appels API)
 */
api.interceptors.request.use(
  (config) => {
    // Récupérer le token JWT depuis le stockage local
    const token = storage.getToken()

    // Ajouter le token aux headers si disponible
    // Format : Authorization: Bearer {token}
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // Logger les requêtes en mode développement
    if (process.env.DEV) {
      console.log('📤 API Request:', {
        method: config.method?.toUpperCase(),
        url: config.url,
        data: config.data,
        params: config.params,
        hasAuth: !!token
      })
    }

    return config
  },
  (error) => {
    // Gérer les erreurs de configuration de requête
    console.error('❌ Request Configuration Error:', error)
    return Promise.reject(error)
  }
)

// ============================================
// Intercepteur de Réponse (Response)
// ============================================

/**
 * Intercepte toutes les réponses pour :
 * - Gérer les erreurs d'authentification (401)
 * - Rafraîchir le token JWT automatiquement
 * - Afficher les notifications d'erreur
 * - Logger les réponses en dev
 */
api.interceptors.response.use(
  (response) => {
    // Logger les réponses en mode développement
    if (process.env.DEV) {
      console.log('📥 API Response:', {
        status: response.status,
        url: response.config.url,
        data: response.data
      })
    }

    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Logger les erreurs en mode développement
    if (process.env.DEV) {
      console.error('❌ API Error:', {
        status: error.response?.status,
        url: error.config?.url,
        message: error.message,
        data: error.response?.data
      })
    }

    // ----------------------------------------
    // Gestion des erreurs par code HTTP
    // ----------------------------------------

    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 400: // Bad Request
          Notify.create({
            type: 'negative',
            message: data?.message || data?.detail || 'Requête invalide',
            caption: 'Vérifiez les données envoyées',
            position: 'top-right'
          })
          break

        case 401: // Unauthorized - Token expiré ou invalide
          // Tentative de rafraîchissement automatique du token
          // Ne tente qu'une seule fois (flag _retry) pour éviter les boucles infinies
          if (!originalRequest._retry) {
            originalRequest._retry = true

            try {
              const refreshToken = storage.getRefreshToken()

              if (!refreshToken) {
                // Pas de refresh token disponible, déconnecter
                console.warn('No refresh token available')
                handleLogout()
                return Promise.reject(error)
              }

              // Appeler l'endpoint de refresh du backend Django
              const response = await axios.post(
                `${API_BASE_URL}/token/refresh/`,
                { refresh: refreshToken }
              )

              const newAccessToken = response.data.access
              const newRefreshToken = response.data.refresh // Rotation activée dans Django

              // Sauvegarder le nouveau access token
              storage.saveToken(newAccessToken)

              // Si un nouveau refresh token est fourni (rotation activée), le sauvegarder aussi
              if (newRefreshToken) {
                storage.saveRefreshToken(newRefreshToken)

                if (process.env.DEV) {
                  console.log('🔄 Token rotated: New refresh token received')
                }
              }

              if (process.env.DEV) {
                console.log('✅ Access token refreshed successfully')
              }

              // Réessayer la requête originale avec le nouveau access token
              originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
              return api(originalRequest)
            } catch (refreshError) {
              // Échec du refresh : le refresh token est probablement expiré ou invalide
              console.error('❌ Token refresh failed:', refreshError)
              handleLogout()
              return Promise.reject(refreshError)
            }
          } else {
            // Déjà tenté de rafraîchir mais échec, déconnecter l'utilisateur
            console.warn('Token refresh already attempted, logging out')
            handleLogout()
          }
          break

        case 403: // Forbidden
          Notify.create({
            type: 'negative',
            message: 'Accès refusé',
            caption: 'Vous n\'avez pas les permissions nécessaires',
            position: 'top-right'
          })
          break

        case 404: // Not Found
          Notify.create({
            type: 'warning',
            message: 'Ressource non trouvée',
            caption: data?.detail || 'La ressource demandée n\'existe pas',
            position: 'top-right'
          })
          break

        case 422: { // Unprocessable Entity (Validation Error)
          const validationErrors = data?.errors || data?.detail
          Notify.create({
            type: 'negative',
            message: 'Erreur de validation',
            caption: typeof validationErrors === 'string'
              ? validationErrors
              : 'Vérifiez les données du formulaire',
            position: 'top-right'
          })
          break
        }

        case 429: // Too Many Requests
          Notify.create({
            type: 'warning',
            message: 'Trop de requêtes',
            caption: 'Veuillez patienter quelques instants',
            position: 'top-right'
          })
          break

        case 500: // Internal Server Error
          Notify.create({
            type: 'negative',
            message: 'Erreur serveur',
            caption: 'Une erreur s\'est produite côté serveur',
            position: 'top-right'
          })
          break

        case 503: // Service Unavailable
          Notify.create({
            type: 'negative',
            message: 'Service indisponible',
            caption: 'Le serveur est temporairement indisponible',
            position: 'top-right'
          })
          break

        default:
          // Erreur non gérée
          Notify.create({
            type: 'negative',
            message: data?.message || data?.detail || `Erreur ${status}`,
            caption: 'Une erreur s\'est produite',
            position: 'top-right'
          })
      }
    } else if (error.request) {
      // Requête envoyée mais pas de réponse reçue (problème réseau)
      Notify.create({
        type: 'negative',
        message: 'Erreur de connexion',
        caption: 'Impossible de contacter le serveur. Vérifiez votre connexion internet.',
        position: 'top-right',
        timeout: 5000
      })
    } else {
      // Erreur de configuration de la requête
      Notify.create({
        type: 'negative',
        message: 'Erreur de configuration',
        caption: error.message,
        position: 'top-right'
      })
    }

    return Promise.reject(error)
  }
)

// ============================================
// Fonctions Utilitaires
// ============================================

/**
 * Déconnecter l'utilisateur en cas d'échec d'authentification
 * Appelé automatiquement quand :
 * - Le refresh token a expiré ou est invalide
 * - L'utilisateur a été désactivé côté serveur
 * - Une erreur 401 persiste après tentative de refresh
 */
function handleLogout() {
  // Nettoyer complètement le stockage local
  storage.clear()

  // Éviter de rediriger si on est déjà sur la page de login
  const currentPath = window.location.pathname

  if (currentPath !== '/login' && !currentPath.startsWith('/auth')) {
    // Notifier l'utilisateur de l'expiration de session
    Notify.create({
      type: 'warning',
      message: 'Session expirée',
      caption: 'Veuillez vous reconnecter',
      position: 'top-right',
      timeout: 3000
    })

    // Redirection vers la page de login
    // Utiliser le router Quasar si disponible, sinon fallback sur window.location
    if (router) {
      setTimeout(() => {
        router.push({ path: '/login', query: { redirect: currentPath } })
      }, 1500)
    } else {
      // Fallback si le router n'est pas encore disponible
      setTimeout(() => {
        window.location.href = '/#/login'
      }, 1500)
    }
  }
}

/**
 * Fonction pour définir le router depuis le boot
 * @param {Object} routerInstance - Instance du router Quasar
 */
export function setRouter(routerInstance) {
  router = routerInstance
}

// ============================================
// Export du Boot File Quasar
// ============================================

/**
 * Boot file Quasar pour configurer Axios
 * Chargé automatiquement au démarrage de l'application
 *
 * @param {Object} context - Contexte du boot file Quasar
 * @param {Object} context.app - Instance de l'application Vue
 * @param {Object} context.router - Instance du router Vue Router
 */
export default defineBoot(({ app, router: routerInstance }) => {
  // Rendre Axios disponible globalement dans les composants Vue
  // Options API : this.$axios (instance native) et this.$api (instance configurée)
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api

  // Stocker le router pour l'utiliser dans handleLogout()
  if (routerInstance) {
    router = routerInstance
  }

  // Logger la configuration en mode développement
  if (process.env.DEV) {
    console.log('✅ Axios configured:', {
      baseURL: API_BASE_URL,
      timeout: API_TIMEOUT,
      interceptors: {
        request: 'JWT Token injection',
        response: 'Auto refresh + Error handling'
      }
    })
  }
})

// ============================================
// Export de l'Instance API
// ============================================

/**
 * Instance Axios configurée à utiliser dans les services
 * Import : import { api } from 'boot/axios'
 */
export { api }
