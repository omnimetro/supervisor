<template>
  <q-page class="q-pa-md">
    <!-- En-tête de page -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h4 text-weight-bold text-primary">Techniciens</div>
        <div class="text-subtitle2 text-grey-7">Gestion des techniciens de terrain</div>
      </div>
      <q-btn
        color="primary"
        icon="add"
        label="Nouveau Technicien"
        @click="openCreateDialog"
        unelevated
      />
    </div>

    <!-- Statistiques -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-md-3">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-primary">{{ stats.total }}</div>
            <div class="text-caption text-grey-7">Total Techniciens</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-positive">{{ stats.actifs }}</div>
            <div class="text-caption text-grey-7">Actifs</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-6">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-caption text-grey-7 q-mb-xs">Répartition par spécialité</div>
            <div class="row q-gutter-xs">
              <q-chip
                v-for="(count, specialiteId) in stats.bySpecialite"
                :key="specialiteId"
                :style="{ backgroundColor: getSpecialiteColor(specialiteId) }"
                text-color="white"
                size="sm"
              >
                {{ getSpecialiteLabel(specialiteId) }}: {{ count }}
              </q-chip>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Filtres et recherche -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-4">
            <q-input
              v-model="searchQuery"
              outlined
              dense
              placeholder="Rechercher un technicien..."
              clearable
              @update:model-value="onSearch"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
          <div class="col-12 col-md-3">
            <q-select
              v-model="filterSpecialite"
              outlined
              dense
              :options="specialiteOptions"
              emit-value
              map-options
              label="Spécialité"
              clearable
              @update:model-value="onFilter"
            />
          </div>
          <div class="col-12 col-md-2">
            <q-select
              v-model="filterStatus"
              outlined
              dense
              :options="statusOptions"
              emit-value
              map-options
              label="Statut"
              clearable
              @update:model-value="onFilter"
            />
          </div>
          <div class="col-12 col-md-3">
            <q-btn
              color="secondary"
              icon="refresh"
              label="Actualiser"
              @click="loadTechnicians"
              outline
              class="full-width"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Tableau des techniciens -->
    <q-card>
      <q-card-section>
        <q-table
          :rows="technicians"
          :columns="columns"
          :loading="loading"
          row-key="id"
          flat
          :pagination="pagination"
          @request="onTableRequest"
          binary-state-sort
        >
          <!-- Slot personnalisé pour le nom complet -->
          <template v-slot:body-cell-nom="props">
            <q-td :props="props">
              <div>
                <div class="text-weight-medium">{{ props.row.nom }} {{ props.row.prenoms }}</div>
                <div class="text-caption text-grey-7">Mat: {{ props.row.matricule }}</div>
              </div>
            </q-td>
          </template>

          <!-- Slot personnalisé pour la spécialité -->
          <template v-slot:body-cell-specialite="props">
            <q-td :props="props">
              <q-badge
                :style="{ backgroundColor: getSpecialiteColor(props.row.specialite) }"
                text-color="white"
              >
                {{ getSpecialiteLabel(props.row.specialite) }}
              </q-badge>
            </q-td>
          </template>

          <!-- Slot personnalisé pour le statut -->
          <template v-slot:body-cell-is_active="props">
            <q-td :props="props">
              <q-badge
                :color="props.row.is_active ? 'positive' : 'negative'"
                :label="props.row.is_active ? 'Actif' : 'Inactif'"
              />
            </q-td>
          </template>

          <!-- Slot personnalisé pour les actions -->
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn
                flat
                dense
                round
                color="primary"
                icon="edit"
                @click="editTechnician(props.row)"
              >
                <q-tooltip>Modifier</q-tooltip>
              </q-btn>
              <q-btn
                flat
                dense
                round
                color="negative"
                icon="delete"
                @click="confirmDelete(props.row)"
              >
                <q-tooltip>Supprimer</q-tooltip>
              </q-btn>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Dialog de formulaire technicien -->
    <q-dialog v-model="showFormDialog" persistent>
      <q-card style="min-width: 700px">
        <q-card-section class="row items-center">
          <div class="text-h6">{{ isEditing ? 'Modifier' : 'Créer' }} un technicien</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 70vh" class="scroll">
          <q-form @submit="saveTechnician" class="q-gutter-md">
            <q-input
              v-model="formData.matricule"
              label="Matricule *"
              outlined
              :rules="[val => !!val || 'Le matricule est requis']"
            />

            <div class="row q-col-gutter-md">
              <div class="col-6">
                <q-input
                  v-model="formData.nom"
                  label="Nom *"
                  outlined
                  :rules="[val => !!val || 'Le nom est requis']"
                />
              </div>
              <div class="col-6">
                <q-input
                  v-model="formData.prenoms"
                  label="Prénoms *"
                  outlined
                  :rules="[val => !!val || 'Les prénoms sont requis']"
                />
              </div>
            </div>

            <q-input
              v-model="formData.telephone"
              label="Téléphone *"
              outlined
              :rules="[val => !!val || 'Le téléphone est requis']"
            />

            <!-- Spécialité avec bouton de gestion -->
            <div class="row q-col-gutter-sm">
              <div class="col-10">
                <q-select
                  v-model="formData.specialite"
                  outlined
                  :options="specialiteOptions"
                  emit-value
                  map-options
                  label="Spécialité *"
                  :rules="[val => !!val || 'La spécialité est requise']"
                />
              </div>
              <div class="col-2">
                <q-btn
                  type="button"
                  icon="settings"
                  color="secondary"
                  outline
                  style="height: 56px; width: 100%"
                  @click="openSpecialitesDialog"
                >
                  <q-tooltip>Gérer les spécialités</q-tooltip>
                </q-btn>
              </div>
            </div>

            <q-input
              v-model="formData.date_embauche"
              label="Date d'embauche"
              type="date"
              outlined
            />

            <q-toggle
              v-model="formData.is_active"
              label="Technicien actif"
              color="positive"
            />
          </q-form>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            :label="isEditing ? 'Modifier' : 'Créer'"
            color="primary"
            @click="saveTechnician"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog de confirmation de suppression technicien -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="warning" color="negative" text-color="white" />
          <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer ce technicien ?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            label="Supprimer"
            color="negative"
            @click="deleteTechnician"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { useDeploymentStore } from 'src/stores/deployment'
import { apiService } from 'src/services/api'

const $q = useQuasar()
const router = useRouter()

// ============================================
// STORE
// ============================================

const deploymentStore = useDeploymentStore()

// ============================================
// STATE - TECHNICIENS
// ============================================

const showFormDialog = ref(false)
const showDeleteDialog = ref(false)
const isEditing = ref(false)
const selectedTechnician = ref(null)

const searchQuery = ref('')
const filterSpecialite = ref(null)
const filterStatus = ref(null)

const technicians = ref([])
const loading = ref(false)

const formData = ref({
  matricule: '',
  nom: '',
  prenoms: '',
  telephone: '',
  specialite: null,
  date_embauche: '',
  is_active: true
})

const pagination = ref({
  sortBy: 'nom',
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

// ============================================
// STATE - SPÉCIALITÉS
// ============================================

const specialites = ref([])
const loadingSpecialites = ref(false)

// ============================================
// COMPUTED
// ============================================

const stats = computed(() => {
  const total = technicians.value.length
  const actifs = technicians.value.filter(t => t.is_active).length
  const bySpecialite = {}

  technicians.value.forEach(t => {
    if (!bySpecialite[t.specialite]) {
      bySpecialite[t.specialite] = 0
    }
    bySpecialite[t.specialite]++
  })

  return { total, actifs, bySpecialite }
})

const specialiteOptions = computed(() => {
  if (!Array.isArray(specialites.value)) {
    return []
  }
  return specialites.value
    .filter(s => s.is_active)
    .map(s => ({
      label: s.nom,
      value: s.id
    }))
})

const statusOptions = [
  { label: 'Tous', value: null },
  { label: 'Actif', value: true },
  { label: 'Inactif', value: false }
]

const columns = [
  {
    name: 'nom',
    label: 'Nom / Matricule',
    field: 'nom',
    align: 'left',
    sortable: true
  },
  {
    name: 'telephone',
    label: 'Téléphone',
    field: 'telephone',
    align: 'left'
  },
  {
    name: 'specialite',
    label: 'Spécialité',
    field: 'specialite',
    align: 'center',
    sortable: true
  },
  {
    name: 'date_embauche',
    label: 'Date embauche',
    field: 'date_embauche',
    align: 'center',
    sortable: true,
    format: val => val ? new Date(val).toLocaleDateString('fr-FR') : '-'
  },
  {
    name: 'is_active',
    label: 'Statut',
    field: 'is_active',
    align: 'center',
    sortable: true
  },
  {
    name: 'actions',
    label: 'Actions',
    field: 'actions',
    align: 'center'
  }
]

// ============================================
// METHODS - UTILS
// ============================================

function getSpecialiteLabel(specialiteId) {
  if (!Array.isArray(specialites.value)) {
    return 'Non défini'
  }
  const specialite = specialites.value.find(s => s.id === specialiteId)
  return specialite ? specialite.nom : 'Non défini'
}

function getSpecialiteColor(specialiteId) {
  if (!Array.isArray(specialites.value)) {
    return '#999999'
  }
  const specialite = specialites.value.find(s => s.id === specialiteId)
  return specialite ? specialite.couleur : '#999999'
}

// ============================================
// METHODS - SPÉCIALITÉS
// ============================================

async function loadSpecialites() {
  loadingSpecialites.value = true
  try {
    const response = await apiService.deployment.specialites.list()
    // L'API retourne un objet paginé avec {count, next, previous, results}
    // ou directement un tableau si pas de pagination
    if (response.data.results) {
      specialites.value = response.data.results
    } else if (Array.isArray(response.data)) {
      specialites.value = response.data
    } else {
      specialites.value = []
    }
  } catch (error) {
    console.error('Erreur chargement spécialités:', error)
    specialites.value = [] // Initialiser comme tableau vide en cas d'erreur
    $q.notify({
      type: 'negative',
      message: 'Erreur lors du chargement des spécialités',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    loadingSpecialites.value = false
  }
}

function openSpecialitesDialog() {
  // Naviguer vers la page de gestion des spécialités
  router.push({ name: 'specialites' })
}

// ============================================
// METHODS - TECHNICIENS
// ============================================

async function loadTechnicians(params = {}) {
  loading.value = true
  try {
    const result = await deploymentStore.technicians.list(params)
    technicians.value = Array.isArray(result) ? result : []

    if (deploymentStore.technicians?.pagination?.value?.rowsNumber !== undefined) {
      pagination.value.rowsNumber = deploymentStore.technicians.pagination.value.rowsNumber
    }
  } catch (error) {
    console.error('Erreur chargement techniciens:', error)
    $q.notify({
      type: 'negative',
      message: 'Erreur lors du chargement des techniciens',
      caption: error.response?.data?.detail || error.message
    })
    technicians.value = []
  } finally {
    loading.value = false
  }
}

async function onTableRequest(props) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  const params = {
    page,
    page_size: rowsPerPage,
    ordering: (descending ? '-' : '') + sortBy
  }

  if (searchQuery.value) {
    params.search = searchQuery.value
  }

  if (filterSpecialite.value) {
    params.specialite = filterSpecialite.value
  }

  if (filterStatus.value !== null) {
    params.is_active = filterStatus.value
  }

  await loadTechnicians(params)
  pagination.value = props.pagination
}

function onSearch() {
  loadTechnicians({
    search: searchQuery.value,
    specialite: filterSpecialite.value,
    is_active: filterStatus.value
  })
}

function onFilter() {
  loadTechnicians({
    search: searchQuery.value,
    specialite: filterSpecialite.value,
    is_active: filterStatus.value
  })
}

function openCreateDialog() {
  resetForm()
  showFormDialog.value = true
}

function editTechnician(technician) {
  isEditing.value = true
  selectedTechnician.value = technician
  formData.value = { ...technician }
  showFormDialog.value = true
}

function resetForm() {
  isEditing.value = false
  selectedTechnician.value = null
  formData.value = {
    matricule: '',
    nom: '',
    prenoms: '',
    telephone: '',
    specialite: null,
    date_embauche: '',
    is_active: true
  }
}

async function saveTechnician() {
  try {
    if (isEditing.value) {
      await deploymentStore.technicians.update(selectedTechnician.value.id, formData.value)
      $q.notify({
        type: 'positive',
        message: 'Technicien modifié avec succès'
      })
    } else {
      await deploymentStore.technicians.create(formData.value)
      $q.notify({
        type: 'positive',
        message: 'Technicien créé avec succès'
      })
    }

    showFormDialog.value = false
    resetForm()
    await loadTechnicians()
  } catch (error) {
    console.error('Erreur sauvegarde technicien:', error)
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de l\'enregistrement',
      caption: error.response?.data?.detail || error.message
    })
  }
}

function confirmDelete(technician) {
  selectedTechnician.value = technician
  showDeleteDialog.value = true
}

async function deleteTechnician() {
  try {
    await deploymentStore.technicians.remove(selectedTechnician.value.id)
    $q.notify({
      type: 'positive',
      message: 'Technicien supprimé avec succès'
    })
    showDeleteDialog.value = false
    selectedTechnician.value = null
    await loadTechnicians()
  } catch (error) {
    console.error('Erreur suppression technicien:', error)
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de la suppression',
      caption: error.response?.data?.detail || error.message
    })
  }
}

// ============================================
// LIFECYCLE
// ============================================

onMounted(async () => {
  await loadSpecialites()
  await loadTechnicians()
})
</script>

<style scoped>
.q-table th {
  font-weight: 600;
}
</style>
