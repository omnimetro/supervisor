import { LocalStorage } from 'quasar'

/**
 * Utilitaires pour le stockage local
 */

export const storage = {
  /**
   * Sauvegarder un token JWT
   */
  saveToken(token) {
    LocalStorage.set('auth_token', token)
  },

  /**
   * Récupérer le token JWT
   */
  getToken() {
    return LocalStorage.getItem('auth_token')
  },

  /**
   * Supprimer le token JWT
   */
  removeToken() {
    LocalStorage.remove('auth_token')
  },

  /**
   * Sauvegarder le refresh token
   */
  saveRefreshToken(refreshToken) {
    LocalStorage.set('refresh_token', refreshToken)
  },

  /**
   * Récupérer le refresh token
   */
  getRefreshToken() {
    return LocalStorage.getItem('refresh_token')
  },

  /**
   * Supprimer le refresh token
   */
  removeRefreshToken() {
    LocalStorage.remove('refresh_token')
  },

  /**
   * Sauvegarder les informations utilisateur
   */
  saveUser(user) {
    LocalStorage.set('user', user)
  },

  /**
   * Récupérer les informations utilisateur
   */
  getUser() {
    return LocalStorage.getItem('user')
  },

  /**
   * Supprimer les informations utilisateur
   */
  removeUser() {
    LocalStorage.remove('user')
  },

  /**
   * Vider tout le stockage
   */
  clear() {
    LocalStorage.clear()
  }
}

export default storage
