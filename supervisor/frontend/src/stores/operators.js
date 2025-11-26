/**
 * Store Pinia pour la gestion des Opérateurs - SUPERVISOR V2.0
 *
 * Gère les opérateurs télécoms (Orange, Moov, etc.) :
 * - Liste des opérateurs
 * - Création / Modification / Suppression
 * - Opérateurs actifs
 * - Cache local
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from 'src/services/api'
import { Notify } from 'quasar'

export const useOperatorsStore = defineStore('operators', () => {
  // ============================================
  // STATE
  // ============================================

  /**
   * Liste complète des opérateurs
   */
  const operators = ref([])

  /**
   * Opérateur sélectionné pour édition
   */
  const selectedOperator = ref(null)

  /**
   * État de chargement
   */
  const loading = ref(false)

  /**
   * État d'erreur
   */
  const error = ref(null)

  // ============================================
  // GETTERS
  // ============================================

  /**
   * Opérateurs actifs uniquement
   */
  const activeOperators = computed(() => {
    return operators.value.filter(op => op.actif)
  })

  /**
   * Nombre total d'opérateurs
   */
  const totalOperators = computed(() => {
    return operators.value.length
  })

  /**
   * Nombre d'opérateurs actifs
   */
  const totalActiveOperators = computed(() => {
    return activeOperators.value.length
  })

  /**
   * Rechercher un opérateur par ID
   * @param {Number} id - ID de l'opérateur
   * @returns {Object|null}
   */
  const getOperatorById = computed(() => (id) => {
    return operators.value.find(op => op.id === id) || null
  })

  /**
   * Rechercher un opérateur par nom
   * @param {String} nom - Nom de l'opérateur
   * @returns {Object|null}
   */
  const getOperatorByName = computed(() => (nom) => {
    return operators.value.find(op =>
      op.nom.toLowerCase() === nom.toLowerCase()
    ) || null
  })

  // ============================================
  // ACTIONS
  // ============================================

  /**
   * Récupérer la liste complète des opérateurs
   * @param {Object} params - Paramètres de filtrage optionnels
   */
  async function fetchOperators(params = {}) {
    loading.value = true
    error.value = null

    try {
      const response = await apiService.deployment.operators.list(params)
      operators.value = response.data.results || response.data
      return operators.value
    } catch (err) {
      error.value = err.response?.data?.message || 'Erreur lors du chargement des opérateurs'
      console.error('Erreur fetchOperators:', err)

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

  /**
   * Récupérer uniquement les opérateurs actifs
   */
  async function fetchActiveOperators() {
    loading.value = true
    error.value = null

    try {
      const response = await apiService.deployment.operators.active()
      operators.value = response.data.results || response.data
      return operators.value
    } catch (err) {
      error.value = err.response?.data?.message || 'Erreur lors du chargement des opérateurs actifs'
      console.error('Erreur fetchActiveOperators:', err)

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

  /**
   * Récupérer un opérateur par son ID
   * @param {Number} id - ID de l'opérateur
   */
  async function fetchOperator(id) {
    loading.value = true
    error.value = null

    try {
      const response = await apiService.deployment.operators.get(id)
      selectedOperator.value = response.data
      return selectedOperator.value
    } catch (err) {
      error.value = err.response?.data?.message || 'Erreur lors du chargement de l\'opérateur'
      console.error('Erreur fetchOperator:', err)

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

  /**
   * Créer un nouvel opérateur
   * @param {Object} data - Données de l'opérateur
   */
  async function createOperator(data) {
    loading.value = true
    error.value = null

    try {
      const response = await apiService.deployment.operators.create(data)
      const newOperator = response.data

      // Ajouter à la liste locale
      operators.value.push(newOperator)

      Notify.create({
        type: 'positive',
        message: 'Opérateur créé avec succès',
        position: 'top'
      })

      return newOperator
    } catch (err) {
      error.value = err.response?.data?.message || 'Erreur lors de la création de l\'opérateur'
      console.error('Erreur createOperator:', err)

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

  /**
   * Mettre à jour un opérateur existant
   * @param {Number} id - ID de l'opérateur
   * @param {Object} data - Données modifiées
   */
  async function updateOperator(id, data) {
    loading.value = true
    error.value = null

    try {
      const response = await apiService.deployment.operators.update(id, data)
      const updatedOperator = response.data

      // Mettre à jour dans la liste locale
      const index = operators.value.findIndex(op => op.id === id)
      if (index !== -1) {
        operators.value[index] = updatedOperator
      }

      // Mettre à jour l'opérateur sélectionné si c'est le même
      if (selectedOperator.value?.id === id) {
        selectedOperator.value = updatedOperator
      }

      Notify.create({
        type: 'positive',
        message: 'Opérateur modifié avec succès',
        position: 'top'
      })

      return updatedOperator
    } catch (err) {
      error.value = err.response?.data?.message || 'Erreur lors de la modification de l\'opérateur'
      console.error('Erreur updateOperator:', err)

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

  /**
   * Mettre à jour partiellement un opérateur
   * @param {Number} id - ID de l'opérateur
   * @param {Object} data - Données partielles à modifier
   */
  async function patchOperator(id, data) {
    loading.value = true
    error.value = null

    try {
      const response = await apiService.deployment.operators.patch(id, data)
      const updatedOperator = response.data

      // Mettre à jour dans la liste locale
      const index = operators.value.findIndex(op => op.id === id)
      if (index !== -1) {
        operators.value[index] = updatedOperator
      }

      // Mettre à jour l'opérateur sélectionné si c'est le même
      if (selectedOperator.value?.id === id) {
        selectedOperator.value = updatedOperator
      }

      Notify.create({
        type: 'positive',
        message: 'Opérateur modifié avec succès',
        position: 'top'
      })

      return updatedOperator
    } catch (err) {
      error.value = err.response?.data?.message || 'Erreur lors de la modification de l\'opérateur'
      console.error('Erreur patchOperator:', err)

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

  /**
   * Supprimer un opérateur
   * @param {Number} id - ID de l'opérateur
   */
  async function deleteOperator(id) {
    loading.value = true
    error.value = null

    try {
      await apiService.deployment.operators.delete(id)

      // Retirer de la liste locale
      const index = operators.value.findIndex(op => op.id === id)
      if (index !== -1) {
        operators.value.splice(index, 1)
      }

      // Réinitialiser l'opérateur sélectionné si c'est celui qui a été supprimé
      if (selectedOperator.value?.id === id) {
        selectedOperator.value = null
      }

      Notify.create({
        type: 'positive',
        message: 'Opérateur supprimé avec succès',
        position: 'top'
      })
    } catch (err) {
      error.value = err.response?.data?.message || 'Erreur lors de la suppression de l\'opérateur'
      console.error('Erreur deleteOperator:', err)

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

  /**
   * Sélectionner un opérateur pour édition
   * @param {Object} operator - Opérateur à sélectionner
   */
  function selectOperator(operator) {
    selectedOperator.value = operator
  }

  /**
   * Désélectionner l'opérateur actuel
   */
  function clearSelection() {
    selectedOperator.value = null
  }

  /**
   * Réinitialiser le store
   */
  function reset() {
    operators.value = []
    selectedOperator.value = null
    loading.value = false
    error.value = null
  }

  // ============================================
  // RETURN (EXPOSER L'API DU STORE)
  // ============================================

  return {
    // State
    operators,
    selectedOperator,
    loading,
    error,

    // Getters
    activeOperators,
    totalOperators,
    totalActiveOperators,
    getOperatorById,
    getOperatorByName,

    // Actions
    fetchOperators,
    fetchActiveOperators,
    fetchOperator,
    createOperator,
    updateOperator,
    patchOperator,
    deleteOperator,
    selectOperator,
    clearSelection,
    reset
  }
})
