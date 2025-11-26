/**
 * Service API pour SUPERVISOR V2.0
 * Centralise tous les appels au backend Django avec méthodes helpers
 */

import { api } from 'boot/axios'
import { API_ENDPOINTS } from 'src/utils/constants'

// ============================================
// Fonctions Utilitaires Internes
// ============================================

/**
 * Formater les paramètres de requête pour l'URL
 * @param {Object} params - Paramètres de la requête
 * @returns {Object} Paramètres formatés
 */
const formatParams = (params) => {
  if (!params) return {}

  // Supprimer les paramètres undefined ou null
  return Object.keys(params).reduce((acc, key) => {
    if (params[key] !== undefined && params[key] !== null) {
      acc[key] = params[key]
    }
    return acc
  }, {})
}

/**
 * Créer un objet FormData à partir d'un objet
 * Utile pour les uploads de fichiers
 * @param {Object} data - Données à convertir
 * @returns {FormData}
 */
const createFormData = (data) => {
  const formData = new FormData()

  Object.keys(data).forEach(key => {
    const value = data[key]

    // Gérer les fichiers
    if (value instanceof File) {
      formData.append(key, value)
    }
    // Gérer les tableaux de fichiers
    else if (Array.isArray(value) && value[0] instanceof File) {
      value.forEach((file, index) => {
        formData.append(`${key}[${index}]`, file)
      })
    }
    // Gérer les objets (les convertir en JSON)
    else if (typeof value === 'object' && value !== null) {
      formData.append(key, JSON.stringify(value))
    }
    // Gérer les valeurs primitives
    else if (value !== undefined && value !== null) {
      formData.append(key, value)
    }
  })

  return formData
}

// ============================================
// Service API Principal
// ============================================

export const apiService = {

  // ============================================
  // MODULE AUTHENTIFICATION
  // ============================================

  auth: {
    /**
     * Connexion utilisateur
     * @param {Object} credentials - { username, password }
     * @returns {Promise} { access, refresh, user }
     */
    login: (credentials) => api.post(API_ENDPOINTS.AUTH.LOGIN, credentials),

    /**
     * Rafraîchir le token JWT
     * @param {String} refreshToken - Token de rafraîchissement
     * @returns {Promise} { access }
     */
    refresh: (refreshToken) => api.post(API_ENDPOINTS.AUTH.REFRESH, { refresh: refreshToken }),

    /**
     * Déconnexion utilisateur
     * @returns {Promise}
     */
    logout: () => api.post(API_ENDPOINTS.AUTH.LOGOUT),

    /**
     * Inscription d'un nouvel utilisateur
     * @param {Object} userData - Données d'inscription
     * @returns {Promise}
     */
    register: (userData) => api.post(API_ENDPOINTS.AUTH.REGISTER, userData),

    /**
     * Récupérer le profil utilisateur connecté
     * @returns {Promise}
     */
    getProfile: () => api.get(API_ENDPOINTS.AUTH.PROFILE),

    /**
     * Mettre à jour le profil utilisateur
     * @param {Object} data - Données du profil
     * @returns {Promise}
     */
    updateProfile: (data) => api.put(API_ENDPOINTS.AUTH.PROFILE, data),

    /**
     * Changer le mot de passe
     * @param {Object} data - { old_password, new_password }
     * @returns {Promise}
     */
    changePassword: (data) => api.post(API_ENDPOINTS.AUTH.CHANGE_PASSWORD, data)
  },

  // ============================================
  // MODULE DÉPLOIEMENT (CHANTIERS)
  // ============================================

  deployment: {
    // ============================================
    // OPÉRATEURS ET BOQ
    // ============================================

    // --- Opérateurs (Orange, Moov, etc.) ---
    operators: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.OPERATORS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.OPERATORS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.OPERATORS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.OPERATORS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.OPERATORS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.OPERATORS}${id}/`),

      // Action personnalisée
      active: () => api.get(`${API_ENDPOINTS.DEPLOYMENT.OPERATORS}active/`)
    },

    // --- Catégories BOQ ---
    boqCategories: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.BOQ_CATEGORIES, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.BOQ_CATEGORIES}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.BOQ_CATEGORIES, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.BOQ_CATEGORIES}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.BOQ_CATEGORIES}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.BOQ_CATEGORIES}${id}/`)
    },

    // --- Articles BOQ ---
    boqItems: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.BOQ_ITEMS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.BOQ_ITEMS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.BOQ_ITEMS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.BOQ_ITEMS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.BOQ_ITEMS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.BOQ_ITEMS}${id}/`)
    },

    // --- Définitions de Tâches ---
    taskDefinitions: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.TASK_DEFINITIONS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.TASK_DEFINITIONS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.TASK_DEFINITIONS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.TASK_DEFINITIONS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.TASK_DEFINITIONS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.TASK_DEFINITIONS}${id}/`)
    },

    // ============================================
    // RESSOURCES HUMAINES
    // ============================================

    // --- Sous-traitants ---
    subcontractors: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.SUBCONTRACTORS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.SUBCONTRACTORS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.SUBCONTRACTORS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.SUBCONTRACTORS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.SUBCONTRACTORS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.SUBCONTRACTORS}${id}/`),

      // Action personnalisée
      active: () => api.get(`${API_ENDPOINTS.DEPLOYMENT.SUBCONTRACTORS}active/`)
    },

    // --- Spécialités techniques ---
    specialites: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.SPECIALITES, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.SPECIALITES}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.SPECIALITES, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.SPECIALITES}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.SPECIALITES}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.SPECIALITES}${id}/`),

      // Action personnalisée
      active: () => api.get(`${API_ENDPOINTS.DEPLOYMENT.SPECIALITES}active/`)
    },

    // --- Techniciens ---
    technicians: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.TECHNICIANS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.TECHNICIANS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.TECHNICIANS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.TECHNICIANS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.TECHNICIANS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.TECHNICIANS}${id}/`),

      // Actions personnalisées
      active: () => api.get(`${API_ENDPOINTS.DEPLOYMENT.TECHNICIANS}active/`),
      bySpecialite: () => api.get(`${API_ENDPOINTS.DEPLOYMENT.TECHNICIANS}by_specialite/`)
    },

    // ============================================
    // PROJETS ET PLANNINGS
    // ============================================

    // --- Projets ---
    projects: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.PROJECTS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.PROJECTS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.PROJECTS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.PROJECTS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.PROJECTS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.PROJECTS}${id}/`),

      // Actions personnalisées
      active: () => api.get(`${API_ENDPOINTS.DEPLOYMENT.PROJECTS}active/`),
      delayed: () => api.get(`${API_ENDPOINTS.DEPLOYMENT.PROJECTS}delayed/`),
      statistics: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.PROJECTS}${id}/statistics/`)
    },

    // --- Plannings de Projet ---
    projectPlannings: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.PROJECT_PLANNINGS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.PROJECT_PLANNINGS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.PROJECT_PLANNINGS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.PROJECT_PLANNINGS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.PROJECT_PLANNINGS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.PROJECT_PLANNINGS}${id}/`)
    },

    // --- Plannings de Tâche ---
    taskPlannings: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.TASK_PLANNINGS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.TASK_PLANNINGS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.TASK_PLANNINGS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.TASK_PLANNINGS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.TASK_PLANNINGS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.TASK_PLANNINGS}${id}/`),

      // Action personnalisée
      delayed: () => api.get(`${API_ENDPOINTS.DEPLOYMENT.TASK_PLANNINGS}delayed/`)
    },

    // ============================================
    // SUIVI TERRAIN
    // ============================================

    // --- Rapports Journaliers ---
    dailyReports: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS}${id}/`),

      // Actions personnalisées
      byProject: (projectId) => api.get(`${API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS}by_project/`, {
        params: { project_id: projectId }
      }),
      byDate: (date) => api.get(`${API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS}by_date/`, {
        params: { date }
      }),

      // Upload de photos
      uploadPhotos: (id, files) => {
        const formData = createFormData({ photos: files })
        return api.post(`${API_ENDPOINTS.DEPLOYMENT.DAILY_REPORTS}${id}/photos/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }
    },

    // --- Points de Cartographie ---
    cartographyPoints: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.CARTOGRAPHY_POINTS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.CARTOGRAPHY_POINTS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.CARTOGRAPHY_POINTS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.CARTOGRAPHY_POINTS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.CARTOGRAPHY_POINTS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.CARTOGRAPHY_POINTS}${id}/`),

      // Action personnalisée
      byProject: (projectId) => api.get(`${API_ENDPOINTS.DEPLOYMENT.CARTOGRAPHY_POINTS}by_project/`, {
        params: { project_id: projectId }
      })
    },

    // ============================================
    // LIVRAISON ET CORRECTIONS
    // ============================================

    // --- Phases de Livraison ---
    deliveryPhases: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.DELIVERY_PHASES, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.DELIVERY_PHASES}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.DELIVERY_PHASES, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.DELIVERY_PHASES}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.DELIVERY_PHASES}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.DELIVERY_PHASES}${id}/`),

      // Upload de fichiers
      uploadFiles: (id, files) => {
        const formData = createFormData({ files })
        return api.post(`${API_ENDPOINTS.DEPLOYMENT.DELIVERY_PHASES}${id}/files/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }
    },

    // --- Corrections ---
    corrections: {
      list: (params) => api.get(API_ENDPOINTS.DEPLOYMENT.CORRECTIONS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.DEPLOYMENT.CORRECTIONS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.DEPLOYMENT.CORRECTIONS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.DEPLOYMENT.CORRECTIONS}${id}/`, data),
      patch: (id, data) => api.patch(`${API_ENDPOINTS.DEPLOYMENT.CORRECTIONS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.DEPLOYMENT.CORRECTIONS}${id}/`),

      // Upload de photos de correction
      uploadPhotos: (id, files) => {
        const formData = createFormData({ photos: files })
        return api.post(`${API_ENDPOINTS.DEPLOYMENT.CORRECTIONS}${id}/photos/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }
    }
  },

  // ============================================
  // MODULE B2B (RACCORDEMENTS ET MAINTENANCES)
  // ============================================

  b2b: {
    // --- Équipes B2B ---
    teams: {
      list: (params) => api.get(API_ENDPOINTS.B2B.TEAMS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.B2B.TEAMS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.B2B.TEAMS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.B2B.TEAMS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.B2B.TEAMS}${id}/`)
    },

    // --- Études de raccordement ---
    studies: {
      list: (params) => api.get(API_ENDPOINTS.B2B.STUDIES, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.B2B.STUDIES}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.B2B.STUDIES, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.B2B.STUDIES}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.B2B.STUDIES}${id}/`),

      // Approuver une étude
      approve: (id, data) => api.post(`${API_ENDPOINTS.B2B.STUDIES}${id}/approve/`, data),

      // Générer rapport d'étude
      generateReport: (id) =>
        api.get(`${API_ENDPOINTS.B2B.STUDIES}${id}/report/`, { responseType: 'blob' })
    },

    // --- Raccordements ---
    connections: {
      list: (params) => api.get(API_ENDPOINTS.B2B.CONNECTIONS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.B2B.CONNECTIONS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.B2B.CONNECTIONS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.B2B.CONNECTIONS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.B2B.CONNECTIONS}${id}/`),

      // Planifier un raccordement
      schedule: (id, date) => api.post(`${API_ENDPOINTS.B2B.CONNECTIONS}${id}/schedule/`, { date }),

      // Marquer comme complété
      complete: (id, data) => api.post(`${API_ENDPOINTS.B2B.CONNECTIONS}${id}/complete/`, data)
    },

    // --- Maintenances ---
    maintenances: {
      list: (params) => api.get(API_ENDPOINTS.B2B.MAINTENANCES, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.B2B.MAINTENANCES}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.B2B.MAINTENANCES, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.B2B.MAINTENANCES}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.B2B.MAINTENANCES}${id}/`),

      // Assigner à une équipe
      assign: (id, teamId) => api.post(`${API_ENDPOINTS.B2B.MAINTENANCES}${id}/assign/`, { team_id: teamId })
    },

    // --- Interventions B2B ---
    interventions: {
      list: (params) => api.get(API_ENDPOINTS.B2B.INTERVENTIONS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.B2B.INTERVENTIONS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.B2B.INTERVENTIONS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.B2B.INTERVENTIONS}${id}/`, data),

      // Upload de photos d'intervention
      uploadPhotos: (id, files) => {
        const formData = createFormData({ photos: files })
        return api.post(`${API_ENDPOINTS.B2B.INTERVENTIONS}${id}/photos/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }
    }
  },

  // ============================================
  // MODULE GESTION DES STOCKS
  // ============================================

  inventory: {
    // --- Matériels ---
    materials: {
      list: (params) => api.get(API_ENDPOINTS.INVENTORY.MATERIALS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.INVENTORY.MATERIALS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.INVENTORY.MATERIALS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.INVENTORY.MATERIALS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.INVENTORY.MATERIALS}${id}/`),

      // Obtenir les statistiques d'un matériel
      stats: (id) => api.get(`${API_ENDPOINTS.INVENTORY.MATERIALS}${id}/stats/`)
    },

    // --- Mouvements de stock ---
    movements: {
      list: (params) => api.get(API_ENDPOINTS.INVENTORY.STOCK_MOVEMENTS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.INVENTORY.STOCK_MOVEMENTS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.INVENTORY.STOCK_MOVEMENTS, data),

      // Historique des mouvements d'un matériel
      history: (materialId) =>
        api.get(API_ENDPOINTS.INVENTORY.STOCK_MOVEMENTS, { params: { material_id: materialId } })
    },

    // --- Affectations ---
    allocations: {
      list: (params) => api.get(API_ENDPOINTS.INVENTORY.ALLOCATIONS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.INVENTORY.ALLOCATIONS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.INVENTORY.ALLOCATIONS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.INVENTORY.ALLOCATIONS}${id}/`, data),

      // Retourner une affectation
      return: (id, data) => api.post(`${API_ENDPOINTS.INVENTORY.ALLOCATIONS}${id}/return/`, data)
    },

    // --- Retours de matériel ---
    returns: {
      list: (params) => api.get(API_ENDPOINTS.INVENTORY.RETURNS, { params: formatParams(params) }),
      create: (data) => api.post(API_ENDPOINTS.INVENTORY.RETURNS, data)
    },

    // --- Rapports de stock ---
    reports: {
      current: () => api.get(`${API_ENDPOINTS.INVENTORY.REPORTS}current/`),
      lowStock: () => api.get(`${API_ENDPOINTS.INVENTORY.REPORTS}low-stock/`),
      exportExcel: () => api.get(`${API_ENDPOINTS.INVENTORY.REPORTS}export/`, { responseType: 'blob' })
    }
  },

  // ============================================
  // MODULE GESTION DES DÉPENSES
  // ============================================

  expenses: {
    // --- Dépenses ---
    list: (params) => api.get(API_ENDPOINTS.EXPENSES.LIST, { params: formatParams(params) }),
    get: (id) => api.get(`${API_ENDPOINTS.EXPENSES.LIST}${id}/`),
    create: (data) => api.post(API_ENDPOINTS.EXPENSES.LIST, data),
    update: (id, data) => api.put(`${API_ENDPOINTS.EXPENSES.LIST}${id}/`, data),
    delete: (id) => api.delete(`${API_ENDPOINTS.EXPENSES.LIST}${id}/`),

    // Upload de justificatif
    uploadReceipt: (id, file) => {
      const formData = createFormData({ receipt: file })
      return api.post(`${API_ENDPOINTS.EXPENSES.LIST}${id}/receipt/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    },

    // --- Catégories de dépenses ---
    categories: {
      list: () => api.get(API_ENDPOINTS.EXPENSES.CATEGORIES),
      get: (id) => api.get(`${API_ENDPOINTS.EXPENSES.CATEGORIES}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.EXPENSES.CATEGORIES, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.EXPENSES.CATEGORIES}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.EXPENSES.CATEGORIES}${id}/`)
    },

    // --- Rapports de dépenses ---
    reports: {
      summary: (params) => api.get(`${API_ENDPOINTS.EXPENSES.REPORTS}summary/`, { params: formatParams(params) }),
      byCategory: (params) => api.get(`${API_ENDPOINTS.EXPENSES.REPORTS}by-category/`, { params: formatParams(params) }),
      byProject: (projectId) => api.get(`${API_ENDPOINTS.EXPENSES.REPORTS}by-project/${projectId}/`),
      exportExcel: (params) =>
        api.get(`${API_ENDPOINTS.EXPENSES.REPORTS}export/`, { params: formatParams(params), responseType: 'blob' })
    },

    // --- Approbation des dépenses ---
    approval: {
      approve: (id, comment) => api.post(`${API_ENDPOINTS.EXPENSES.APPROVAL}${id}/approve/`, { comment }),
      reject: (id, reason) => api.post(`${API_ENDPOINTS.EXPENSES.APPROVAL}${id}/reject/`, { reason }),
      pending: () => api.get(`${API_ENDPOINTS.EXPENSES.APPROVAL}pending/`)
    }
  },

  // ============================================
  // MODULE CARTOGRAPHIE ET TRACKING GPS
  // ============================================

  mapping: {
    // --- Localisations ---
    locations: {
      list: (params) => api.get(API_ENDPOINTS.MAPPING.LOCATIONS, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.MAPPING.LOCATIONS}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.MAPPING.LOCATIONS, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.MAPPING.LOCATIONS}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.MAPPING.LOCATIONS}${id}/`),

      // Extraction GPS depuis photos NoteCam
      extractFromPhotos: (files) => {
        const formData = createFormData({ photos: files })
        return api.post(`${API_ENDPOINTS.MAPPING.LOCATIONS}extract-gps/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }
    },

    // --- Infrastructures (poteaux, équipements, chambres) ---
    infrastructure: {
      list: (params) => api.get(API_ENDPOINTS.MAPPING.INFRASTRUCTURE, { params: formatParams(params) }),
      get: (id) => api.get(`${API_ENDPOINTS.MAPPING.INFRASTRUCTURE}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.MAPPING.INFRASTRUCTURE, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.MAPPING.INFRASTRUCTURE}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.MAPPING.INFRASTRUCTURE}${id}/`),

      // Import KMZ
      importKMZ: (file) => {
        const formData = createFormData({ kmz_file: file })
        return api.post(`${API_ENDPOINTS.MAPPING.INFRASTRUCTURE}import-kmz/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }
    },

    // --- Véhicules ---
    vehicles: {
      list: () => api.get(API_ENDPOINTS.MAPPING.VEHICLES),
      get: (id) => api.get(`${API_ENDPOINTS.MAPPING.VEHICLES}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.MAPPING.VEHICLES, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.MAPPING.VEHICLES}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.MAPPING.VEHICLES}${id}/`)
    },

    // --- Tracking GPS en temps réel ---
    gpsTracking: {
      current: (vehicleId) => api.get(`${API_ENDPOINTS.MAPPING.GPS_TRACKING}${vehicleId}/current/`),
      history: (vehicleId, params) =>
        api.get(`${API_ENDPOINTS.MAPPING.GPS_TRACKING}${vehicleId}/history/`, { params: formatParams(params) }),
      livePositions: () => api.get(`${API_ENDPOINTS.MAPPING.GPS_TRACKING}live/`)
    }
  },

  // ============================================
  // MODULE UTILISATEURS ET PERMISSIONS
  // ============================================

  users: {
    // --- Utilisateurs ---
    list: (params) => api.get(API_ENDPOINTS.USERS.LIST, { params: formatParams(params) }),
    get: (id) => api.get(`${API_ENDPOINTS.USERS.LIST}${id}/`),
    create: (data) => api.post(API_ENDPOINTS.USERS.LIST, data),
    update: (id, data) => api.put(`${API_ENDPOINTS.USERS.LIST}${id}/`, data),
    delete: (id) => api.delete(`${API_ENDPOINTS.USERS.LIST}${id}/`),

    // Activer/Désactiver un utilisateur
    activate: (id) => api.post(`${API_ENDPOINTS.USERS.LIST}${id}/activate/`),
    deactivate: (id) => api.post(`${API_ENDPOINTS.USERS.LIST}${id}/deactivate/`),

    // --- Rôles ---
    roles: {
      list: () => api.get(API_ENDPOINTS.USERS.ROLES),
      get: (id) => api.get(`${API_ENDPOINTS.USERS.ROLES}${id}/`),
      create: (data) => api.post(API_ENDPOINTS.USERS.ROLES, data),
      update: (id, data) => api.put(`${API_ENDPOINTS.USERS.ROLES}${id}/`, data),
      delete: (id) => api.delete(`${API_ENDPOINTS.USERS.ROLES}${id}/`)
    },

    // --- Permissions ---
    permissions: {
      list: () => api.get(API_ENDPOINTS.USERS.PERMISSIONS),
      getForUser: (userId) => api.get(`${API_ENDPOINTS.USERS.PERMISSIONS}user/${userId}/`),
      assignToUser: (userId, permissions) =>
        api.post(`${API_ENDPOINTS.USERS.PERMISSIONS}assign/`, { user_id: userId, permissions })
    },

    // --- Journal d'activité ---
    activityLog: {
      list: (params) => api.get(API_ENDPOINTS.USERS.ACTIVITY_LOG, { params: formatParams(params) }),
      getForUser: (userId, params) =>
        api.get(`${API_ENDPOINTS.USERS.ACTIVITY_LOG}user/${userId}/`, { params: formatParams(params) })
    }
  },

  // ============================================
  // MÉTHODES GÉNÉRIQUES UTILITAIRES
  // ============================================

  /**
   * Upload de fichiers génériques
   * @param {String} endpoint - Endpoint de destination
   * @param {File|Array} files - Fichier(s) à uploader
   * @param {Object} additionalData - Données supplémentaires
   * @returns {Promise}
   */
  uploadFile: (endpoint, files, additionalData = {}) => {
    const data = { ...additionalData }

    if (Array.isArray(files)) {
      data.files = files
    } else {
      data.file = files
    }

    const formData = createFormData(data)
    return api.post(endpoint, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  /**
   * Télécharger un fichier
   * @param {String} endpoint - Endpoint du fichier
   * @param {String} filename - Nom du fichier à télécharger
   * @returns {Promise}
   */
  downloadFile: async (endpoint, filename) => {
    const response = await api.get(endpoint, { responseType: 'blob' })

    // Créer un lien de téléchargement temporaire
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    return response
  },

  /**
   * Opération batch (suppression, mise à jour multiple)
   * @param {String} endpoint - Endpoint de l'opération
   * @param {Array} ids - IDs des éléments
   * @param {String} action - Action à effectuer (delete, update, etc.)
   * @param {Object} data - Données pour l'action
   * @returns {Promise}
   */
  batchOperation: (endpoint, ids, action, data = {}) => {
    return api.post(`${endpoint}batch/${action}/`, {
      ids,
      ...data
    })
  }
}

// ============================================
// Export par défaut
// ============================================

export default apiService
