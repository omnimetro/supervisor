/**
 * Store Pinia unifié pour le module Deployment - SUPERVISOR V2.0
 *
 * Ce store regroupe tous les sous-stores du module deployment :
 * - Opérateurs
 * - BOQ (Catégories et Articles)
 * - Définitions de tâches
 * - Sous-traitants
 * - Techniciens
 * - Projets et Plannings
 * - Rapports journaliers
 * - Cartographie
 * - Livraison et Corrections
 *
 * Chaque sous-module expose les méthodes CRUD standard :
 * - list(), get(id), create(data), update(id, data), patch(id, data), delete(id)
 * - Actions personnalisées selon le modèle
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiService } from 'src/services/api'
import { Notify } from 'quasar'

/**
 * Factory pour créer un store CRUD générique
 * @param {String} resourceName - Nom de la ressource (ex: 'operators', 'projects')
 * @param {Object} apiMethods - Méthodes API du service
 * @param {String} displayName - Nom d'affichage pour les notifications
 */
function createCRUDStore(resourceName, apiMethods, displayName) {
  // State
  const items = ref([])
  const selectedItem = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    page: 1,
    rowsPerPage: 20,
    rowsNumber: 0
  })

  // Actions
  async function list(params = {}) {
    loading.value = true
    error.value = null

    try {
      console.log(`[${resourceName}] Calling API list with params:`, params)
      const response = await apiMethods.list(params)
      console.log(`[${resourceName}] API response:`, response)
      console.log(`[${resourceName}] response.data:`, response.data)

      items.value = response.data.results || response.data
      console.log(`[${resourceName}] items.value set to:`, items.value)

      // Gérer la pagination si présente
      if (response.data.count) {
        pagination.value.rowsNumber = response.data.count
        console.log(`[${resourceName}] Pagination count:`, response.data.count)
      }

      return items.value
    } catch (err) {
      error.value = err.response?.data?.message || `Erreur lors du chargement des ${displayName}`
      console.error(`Erreur list ${resourceName}:`, err)

      Notify.create({
        type: 'negative',
        message: error.value,
        position: 'top'
      })

      throw err
    } finally {
      loading.value = false
      console.log(`[${resourceName}] Loading complete. items.value:`, items.value)
    }
  }

  async function get(id) {
    loading.value = true
    error.value = null

    try {
      const response = await apiMethods.get(id)
      selectedItem.value = response.data
      return selectedItem.value
    } catch (err) {
      error.value = err.response?.data?.message || `Erreur lors du chargement de ${displayName}`
      console.error(`Erreur get ${resourceName}:`, err)

      Notify.create({
        type: 'negative',
        message: error.value,
        position: 'top'
      })

      throw err
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    loading.value = true
    error.value = null

    try {
      const response = await apiMethods.create(data)
      const newItem = response.data

      // Ajouter à la liste locale
      items.value.push(newItem)

      Notify.create({
        type: 'positive',
        message: `${displayName} créé avec succès`,
        position: 'top'
      })

      return newItem
    } catch (err) {
      error.value = err.response?.data?.message || `Erreur lors de la création de ${displayName}`
      console.error(`Erreur create ${resourceName}:`, err)

      Notify.create({
        type: 'negative',
        message: error.value,
        position: 'top'
      })

      throw err
    } finally {
      loading.value = false
    }
  }

  async function update(id, data) {
    loading.value = true
    error.value = null

    try {
      const response = await apiMethods.update(id, data)
      const updatedItem = response.data

      // Mettre à jour dans la liste locale
      const index = items.value.findIndex(item => item.id === id)
      if (index !== -1) {
        items.value[index] = updatedItem
      }

      if (selectedItem.value?.id === id) {
        selectedItem.value = updatedItem
      }

      Notify.create({
        type: 'positive',
        message: `${displayName} modifié avec succès`,
        position: 'top'
      })

      return updatedItem
    } catch (err) {
      error.value = err.response?.data?.message || `Erreur lors de la modification de ${displayName}`
      console.error(`Erreur update ${resourceName}:`, err)

      Notify.create({
        type: 'negative',
        message: error.value,
        position: 'top'
      })

      throw err
    } finally {
      loading.value = false
    }
  }

  async function patch(id, data) {
    loading.value = true
    error.value = null

    try {
      const response = await apiMethods.patch(id, data)
      const updatedItem = response.data

      const index = items.value.findIndex(item => item.id === id)
      if (index !== -1) {
        items.value[index] = updatedItem
      }

      if (selectedItem.value?.id === id) {
        selectedItem.value = updatedItem
      }

      Notify.create({
        type: 'positive',
        message: `${displayName} modifié avec succès`,
        position: 'top'
      })

      return updatedItem
    } catch (err) {
      error.value = err.response?.data?.message || `Erreur lors de la modification de ${displayName}`
      console.error(`Erreur patch ${resourceName}:`, err)

      Notify.create({
        type: 'negative',
        message: error.value,
        position: 'top'
      })

      throw err
    } finally {
      loading.value = false
    }
  }

  async function remove(id) {
    loading.value = true
    error.value = null

    try {
      await apiMethods.delete(id)

      // Retirer de la liste locale
      const index = items.value.findIndex(item => item.id === id)
      if (index !== -1) {
        items.value.splice(index, 1)
      }

      if (selectedItem.value?.id === id) {
        selectedItem.value = null
      }

      Notify.create({
        type: 'positive',
        message: `${displayName} supprimé avec succès`,
        position: 'top'
      })
    } catch (err) {
      error.value = err.response?.data?.message || `Erreur lors de la suppression de ${displayName}`
      console.error(`Erreur remove ${resourceName}:`, err)

      Notify.create({
        type: 'negative',
        message: error.value,
        position: 'top'
      })

      throw err
    } finally {
      loading.value = false
    }
  }

  function select(item) {
    selectedItem.value = item
  }

  function clearSelection() {
    selectedItem.value = null
  }

  function reset() {
    items.value = []
    selectedItem.value = null
    loading.value = false
    error.value = null
    pagination.value = {
      page: 1,
      rowsPerPage: 20,
      rowsNumber: 0
    }
  }

  return {
    items,
    selectedItem,
    loading,
    error,
    pagination,
    list,
    get,
    create,
    update,
    patch,
    remove,
    select,
    clearSelection,
    reset
  }
}

/**
 * Store principal Deployment
 */
export const useDeploymentStore = defineStore('deployment', () => {
  // ============================================
  // SOUS-STORES POUR CHAQUE RESSOURCE
  // ============================================

  const operators = createCRUDStore(
    'operators',
    apiService.deployment.operators,
    'l\'opérateur'
  )

  const boqCategories = createCRUDStore(
    'boqCategories',
    apiService.deployment.boqCategories,
    'la catégorie BOQ'
  )

  const boqItems = createCRUDStore(
    'boqItems',
    apiService.deployment.boqItems,
    'l\'article BOQ'
  )

  const taskDefinitions = createCRUDStore(
    'taskDefinitions',
    apiService.deployment.taskDefinitions,
    'la définition de tâche'
  )

  const subcontractors = createCRUDStore(
    'subcontractors',
    apiService.deployment.subcontractors,
    'le sous-traitant'
  )

  const technicians = createCRUDStore(
    'technicians',
    apiService.deployment.technicians,
    'le technicien'
  )

  const projects = createCRUDStore(
    'projects',
    apiService.deployment.projects,
    'le projet'
  )

  const projectPlannings = createCRUDStore(
    'projectPlannings',
    apiService.deployment.projectPlannings,
    'le planning projet'
  )

  const taskPlannings = createCRUDStore(
    'taskPlannings',
    apiService.deployment.taskPlannings,
    'le planning tâche'
  )

  const dailyReports = createCRUDStore(
    'dailyReports',
    apiService.deployment.dailyReports,
    'le rapport journalier'
  )

  const cartographyPoints = createCRUDStore(
    'cartographyPoints',
    apiService.deployment.cartographyPoints,
    'le point de cartographie'
  )

  const deliveryPhases = createCRUDStore(
    'deliveryPhases',
    apiService.deployment.deliveryPhases,
    'la phase de livraison'
  )

  const corrections = createCRUDStore(
    'corrections',
    apiService.deployment.corrections,
    'la correction'
  )

  // ============================================
  // ACTIONS PERSONNALISÉES
  // ============================================

  /**
   * Récupérer les opérateurs actifs uniquement
   */
  async function fetchActiveOperators() {
    operators.loading.value = true
    try {
      const response = await apiService.deployment.operators.active()
      operators.items.value = response.data.results || response.data
      return operators.items.value
    } catch (err) {
      console.error('Erreur fetchActiveOperators:', err)
      throw err
    } finally {
      operators.loading.value = false
    }
  }

  /**
   * Récupérer les sous-traitants actifs uniquement
   */
  async function fetchActiveSubcontractors() {
    subcontractors.loading.value = true
    try {
      const response = await apiService.deployment.subcontractors.active()
      subcontractors.items.value = response.data.results || response.data
      return subcontractors.items.value
    } catch (err) {
      console.error('Erreur fetchActiveSubcontractors:', err)
      throw err
    } finally {
      subcontractors.loading.value = false
    }
  }

  /**
   * Récupérer les techniciens actifs uniquement
   */
  async function fetchActiveTechnicians() {
    technicians.loading.value = true
    try {
      const response = await apiService.deployment.technicians.active()
      technicians.items.value = response.data.results || response.data
      return technicians.items.value
    } catch (err) {
      console.error('Erreur fetchActiveTechnicians:', err)
      throw err
    } finally {
      technicians.loading.value = false
    }
  }

  /**
   * Récupérer les techniciens par spécialité
   */
  async function fetchTechniciansBySpecialite() {
    technicians.loading.value = true
    try {
      const response = await apiService.deployment.technicians.bySpecialite()
      return response.data
    } catch (err) {
      console.error('Erreur fetchTechniciansBySpecialite:', err)
      throw err
    } finally {
      technicians.loading.value = false
    }
  }

  /**
   * Récupérer les projets actifs/en cours uniquement
   */
  async function fetchActiveProjects() {
    projects.loading.value = true
    try {
      const response = await apiService.deployment.projects.active()
      projects.items.value = response.data.results || response.data
      return projects.items.value
    } catch (err) {
      console.error('Erreur fetchActiveProjects:', err)
      throw err
    } finally {
      projects.loading.value = false
    }
  }

  /**
   * Récupérer les projets en retard
   */
  async function fetchDelayedProjects() {
    projects.loading.value = true
    try {
      const response = await apiService.deployment.projects.delayed()
      return response.data.results || response.data
    } catch (err) {
      console.error('Erreur fetchDelayedProjects:', err)
      throw err
    } finally {
      projects.loading.value = false
    }
  }

  /**
   * Récupérer les statistiques d'un projet
   * @param {Number} projectId
   */
  async function fetchProjectStatistics(projectId) {
    try {
      const response = await apiService.deployment.projects.statistics(projectId)
      return response.data
    } catch (err) {
      console.error('Erreur fetchProjectStatistics:', err)
      throw err
    }
  }

  /**
   * Récupérer les tâches en retard
   */
  async function fetchDelayedTasks() {
    taskPlannings.loading.value = true
    try {
      const response = await apiService.deployment.taskPlannings.delayed()
      return response.data.results || response.data
    } catch (err) {
      console.error('Erreur fetchDelayedTasks:', err)
      throw err
    } finally {
      taskPlannings.loading.value = false
    }
  }

  /**
   * Récupérer les rapports journaliers d'un projet
   * @param {Number} projectId
   */
  async function fetchDailyReportsByProject(projectId) {
    dailyReports.loading.value = true
    try {
      const response = await apiService.deployment.dailyReports.byProject(projectId)
      return response.data.results || response.data
    } catch (err) {
      console.error('Erreur fetchDailyReportsByProject:', err)
      throw err
    } finally {
      dailyReports.loading.value = false
    }
  }

  /**
   * Récupérer les rapports journaliers par date
   * @param {String} date - Format YYYY-MM-DD
   */
  async function fetchDailyReportsByDate(date) {
    dailyReports.loading.value = true
    try {
      const response = await apiService.deployment.dailyReports.byDate(date)
      return response.data.results || response.data
    } catch (err) {
      console.error('Erreur fetchDailyReportsByDate:', err)
      throw err
    } finally {
      dailyReports.loading.value = false
    }
  }

  /**
   * Récupérer les points de cartographie d'un projet
   * @param {Number} projectId
   */
  async function fetchCartographyPointsByProject(projectId) {
    cartographyPoints.loading.value = true
    try {
      const response = await apiService.deployment.cartographyPoints.byProject(projectId)
      return response.data.results || response.data
    } catch (err) {
      console.error('Erreur fetchCartographyPointsByProject:', err)
      throw err
    } finally {
      cartographyPoints.loading.value = false
    }
  }

  // ============================================
  // RETURN (EXPOSER L'API DU STORE)
  // ============================================

  return {
    // Sous-stores
    operators,
    boqCategories,
    boqItems,
    taskDefinitions,
    subcontractors,
    technicians,
    projects,
    projectPlannings,
    taskPlannings,
    dailyReports,
    cartographyPoints,
    deliveryPhases,
    corrections,

    // Actions personnalisées
    fetchActiveOperators,
    fetchActiveSubcontractors,
    fetchActiveTechnicians,
    fetchTechniciansBySpecialite,
    fetchActiveProjects,
    fetchDelayedProjects,
    fetchProjectStatistics,
    fetchDelayedTasks,
    fetchDailyReportsByProject,
    fetchDailyReportsByDate,
    fetchCartographyPointsByProject
  }
})
