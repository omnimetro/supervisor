/**
 * Store Pinia pour l'authentification - SUPERVISOR V2.0
 *
 * Gère l'état d'authentification de l'utilisateur côté frontend :
 * - Connexion / Déconnexion
 * - Rafraîchissement du token JWT
 * - Profil utilisateur
 * - Permissions et rôles
 * - Persistance dans localStorage
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from 'src/services/api'
import { storage } from 'src/utils/storage'

export const useAuthStore = defineStore('auth', () => {
  // ============================================
  // STATE
  // ============================================

  /**
   * Informations de l'utilisateur connecté
   * Structure : { id, username, email, profile: { code, nom, prenoms, role, fonction, ... } }
   */
  const user = ref(storage.getUser() || null)

  /**
   * Token d'accès JWT (durée de vie courte : 2h par défaut)
   */
  const accessToken = ref(storage.getToken() || null)

  /**
   * Token de rafraîchissement JWT (durée de vie longue : 7 jours par défaut)
   */
  const refreshToken = ref(storage.getRefreshToken() || null)

  /**
   * Computed : Utilisateur authentifié ou non
   */
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

  // ============================================
  // GETTERS
  // ============================================

  /**
   * Rôle de l'utilisateur
   * @returns {String|null} - 'SUPERADMIN', 'ADMIN', 'COORDONNATEUR', 'STOCKMAN', 'SUPERVISEUR'
   */
  const userRole = computed(() => {
    return user.value?.profile?.role || null
  })

  /**
   * Nom complet de l'utilisateur
   * @returns {String} - "NOM Prénoms"
   */
  const userFullName = computed(() => {
    if (!user.value?.profile) return ''
    const { nom, prenoms } = user.value.profile
    return `${nom} ${prenoms}`.trim()
  })

  /**
   * Vérifie si l'utilisateur est Super Administrateur
   * @returns {Boolean}
   */
  const isSuperAdmin = computed(() => {
    return userRole.value === 'SUPERADMIN'
  })

  /**
   * Vérifie si l'utilisateur est Administrateur
   * @returns {Boolean}
   */
  const isAdmin = computed(() => {
    return userRole.value === 'ADMIN'
  })

  /**
   * Vérifie si l'utilisateur est Coordonnateur
   * @returns {Boolean}
   */
  const isCoordonnateur = computed(() => {
    return userRole.value === 'COORDONNATEUR'
  })

  /**
   * Vérifie si l'utilisateur est Stockman
   * @returns {Boolean}
   */
  const isStockman = computed(() => {
    return userRole.value === 'STOCKMAN'
  })

  /**
   * Vérifie si l'utilisateur est Superviseur
   * @returns {Boolean}
   */
  const isSuperviseur = computed(() => {
    return userRole.value === 'SUPERVISEUR'
  })

  /**
   * Vérifie si l'utilisateur a les droits d'administration (SUPERADMIN ou ADMIN)
   * @returns {Boolean}
   */
  const hasAdminRights = computed(() => {
    return isSuperAdmin.value || isAdmin.value
  })

  /**
   * Vérifie si l'utilisateur a une permission personnalisée
   * @param {String} permissionCode - Code de la permission
   * @returns {Boolean}
   */
  const hasPermission = (permissionCode) => {
    if (!user.value?.profile) return false

    // Super admin a toutes les permissions
    if (isSuperAdmin.value) return true

    // Vérifier dans les permissions personnalisées
    const customPermissions = user.value.profile.custom_permissions || []
    return customPermissions.some(perm => perm.code === permissionCode)
  }

  // ============================================
  // ACTIONS
  // ============================================

  /**
   * Connexion de l'utilisateur
   * @param {Object} credentials - { username, password }
   * @throws {Error} Si les identifiants sont incorrects
   * @returns {Promise<Object>} Données de l'utilisateur connecté
   */
  async function login(credentials) {
    try {
      const response = await apiService.auth.login(credentials)
      const { access, refresh, user: userData } = response.data

      // Stocker les tokens et l'utilisateur
      accessToken.value = access
      refreshToken.value = refresh
      user.value = userData

      // Persister dans localStorage
      storage.saveToken(access)
      storage.saveRefreshToken(refresh)
      storage.saveUser(userData)

      return userData
    } catch (error) {
      // Nettoyer en cas d'erreur
      await logout()
      throw error
    }
  }

  /**
   * Déconnexion de l'utilisateur
   * Envoie une requête au backend pour blacklister le refresh token
   * @returns {Promise<void>}
   */
  async function logout() {
    try {
      // Envoyer le refresh token au backend pour le blacklister
      if (refreshToken.value) {
        await apiService.auth.logout({ refresh: refreshToken.value })
      }
    } catch (error) {
      // Ignorer les erreurs de déconnexion (token déjà expiré, etc.)
      console.warn('Erreur lors de la déconnexion:', error)
    } finally {
      // Toujours nettoyer l'état local
      user.value = null
      accessToken.value = null
      refreshToken.value = null

      // Nettoyer le localStorage
      storage.removeToken()
      storage.removeRefreshToken()
      storage.removeUser()
    }
  }

  /**
   * Rafraîchir le token d'accès avec le refresh token
   * Appelé automatiquement par l'intercepteur Axios en cas de 401
   * @throws {Error} Si le refresh token est invalide/expiré
   * @returns {Promise<String>} Nouveau access token
   */
  async function refreshAccessToken() {
    try {
      if (!refreshToken.value) {
        throw new Error('Aucun refresh token disponible')
      }

      const response = await apiService.auth.refresh(refreshToken.value)
      const { access, refresh: newRefresh } = response.data

      // Mettre à jour l'access token
      accessToken.value = access
      storage.saveToken(access)

      // Si un nouveau refresh token est fourni (rotation activée)
      if (newRefresh) {
        refreshToken.value = newRefresh
        storage.saveRefreshToken(newRefresh)
      }

      return access
    } catch (error) {
      // Si le refresh échoue, déconnecter l'utilisateur
      await logout()
      throw error
    }
  }

  /**
   * Récupérer les informations complètes de l'utilisateur connecté
   * Utile après un rafraîchissement de page ou une mise à jour du profil
   * @returns {Promise<Object>} Données complètes de l'utilisateur
   */
  async function fetchCurrentUser() {
    try {
      const response = await apiService.auth.getProfile()
      user.value = response.data
      storage.saveUser(response.data)
      return response.data
    } catch (error) {
      // Si l'utilisateur n'est plus authentifié
      if (error.response?.status === 401) {
        await logout()
      }
      throw error
    }
  }

  /**
   * Mettre à jour le profil de l'utilisateur
   * @param {Object} profileData - Données du profil à mettre à jour
   * @returns {Promise<Object>} Profil mis à jour
   */
  async function updateUserProfile(profileData) {
    const response = await apiService.auth.updateProfile(profileData)
    user.value = response.data
    storage.saveUser(response.data)
    return response.data
  }

  /**
   * Changer le mot de passe de l'utilisateur
   * @param {Object} passwordData - { old_password, new_password }
   * @throws {Error} Si l'ancien mot de passe est incorrect
   * @returns {Promise<void>}
   */
  async function changePassword(passwordData) {
    await apiService.auth.changePassword(passwordData)
    // Le mot de passe a été changé avec succès
    // Pas besoin de mettre à jour le state
  }

  /**
   * Initialiser le store au chargement de l'application
   * Charge les données depuis localStorage
   * @returns {Promise<void>}
   */
  async function initializeStore() {
    // Charger depuis localStorage
    const storedToken = storage.getToken()
    const storedRefreshToken = storage.getRefreshToken()
    const storedUser = storage.getUser()

    if (storedToken && storedRefreshToken && storedUser) {
      accessToken.value = storedToken
      refreshToken.value = storedRefreshToken
      user.value = storedUser

      // Optionnel : Rafraîchir les données utilisateur au démarrage
      try {
        await fetchCurrentUser()
      } catch {
        // Si l'utilisateur n'est plus authentifié, nettoyer
        console.warn('Session expirée, déconnexion automatique')
        await logout()
      }
    }
  }

  /**
   * Vérifier si le token d'accès est valide
   * Utile pour les guards de navigation
   * @returns {Boolean}
   */
  function isTokenValid() {
    return !!accessToken.value && !!user.value
  }

  // ============================================
  // RETOUR DU STORE
  // ============================================

  return {
    // State
    user,
    accessToken,
    refreshToken,
    isAuthenticated,

    // Getters
    userRole,
    userFullName,
    isSuperAdmin,
    isAdmin,
    isCoordonnateur,
    isStockman,
    isSuperviseur,
    hasAdminRights,
    hasPermission,

    // Actions
    login,
    logout,
    refreshAccessToken,
    fetchCurrentUser,
    updateUserProfile,
    changePassword,
    initializeStore,
    isTokenValid
  }
})
