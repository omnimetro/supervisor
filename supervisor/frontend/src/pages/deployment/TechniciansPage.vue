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

    <!-- Dialog de gestion des spécialités -->
    <q-dialog v-model="showSpecialitesDialog" persistent>
      <q-card style="min-width: 800px; max-width: 90vw">
        <q-card-section class="row items-center bg-primary text-white">
          <q-icon name="school" size="sm" class="q-mr-sm" />
          <div class="text-h6">Gestion des Spécialités</div>
          <q-space />
          <q-btn
            flat
            dense
            round
            icon="add"
            @click="openSpecialiteForm"
            color="white"
          >
            <q-tooltip>Nouvelle spécialité</q-tooltip>
          </q-btn>
          <q-btn flat dense round icon="close" v-close-popup color="white" />
        </q-card-section>

        <q-card-section style="max-height: 60vh" class="scroll">
          <q-table
            :rows="specialites"
            :columns="specialitesColumns"
            row-key="id"
            flat
            :loading="loadingSpecialites"
            hide-pagination
            :rows-per-page-options="[0]"
          >
            <!-- Couleur -->
            <template v-slot:body-cell-couleur="props">
              <q-td :props="props">
                <div
                  :style="{
                    backgroundColor: props.value,
                    width: '40px',
                    height: '20px',
                    border: '1px solid #ccc',
                    borderRadius: '4px'
                  }"
                ></div>
              </q-td>
            </template>

            <!-- Techniciens count -->
            <template v-slot:body-cell-technicians_count="props">
              <q-td :props="props">
                <q-badge color="primary">{{ props.value || 0 }}</q-badge>
              </q-td>
            </template>

            <!-- Actions -->
            <template v-slot:body-cell-actions="props">
              <q-td :props="props">
                <q-btn
                  flat
                  dense
                  round
                  icon="edit"
                  color="primary"
                  size="sm"
                  @click="editSpecialite(props.row)"
                >
                  <q-tooltip>Modifier</q-tooltip>
                </q-btn>
                <q-btn
                  flat
                  dense
                  round
                  icon="delete"
                  color="negative"
                  size="sm"
                  @click="confirmDeleteSpecialite(props.row)"
                  :disable="props.row.technicians_count > 0"
                >
                  <q-tooltip>
                    {{ props.row.technicians_count > 0 ? 'Impossible de supprimer (techniciens affectés)' : 'Supprimer' }}
                  </q-tooltip>
                </q-btn>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog Formulaire Spécialité -->
    <q-dialog v-model="showSpecialiteFormDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center bg-secondary text-white">
          <div class="text-h6">{{ isEditingSpecialite ? 'Modifier' : 'Nouvelle' }} Spécialité</div>
          <q-space />
          <q-btn flat dense round icon="close" v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveSpecialite" class="q-gutter-md">
            <q-input
              v-model="specialiteFormData.code"
              label="Code *"
              outlined
              dense
              :rules="[val => !!val || 'Le code est requis']"
              :disable="isEditingSpecialite"
            />

            <q-input
              v-model="specialiteFormData.nom"
              label="Nom *"
              outlined
              dense
              :rules="[val => !!val || 'Le nom est requis']"
            />

            <q-input
              v-model="specialiteFormData.description"
              label="Description"
              outlined
              dense
              type="textarea"
              rows="2"
            />

            <q-input
              v-model="specialiteFormData.couleur"
              label="Couleur *"
              outlined
              dense
              :rules="[val => !!val || 'La couleur est requise']"
            >
              <template v-slot:append>
                <q-icon name="colorize" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-color v-model="specialiteFormData.couleur" />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>

            <q-input
              v-model.number="specialiteFormData.ordre"
              label="Ordre d'affichage *"
              outlined
              dense
              type="number"
              :rules="[val => val !== null && val !== '' || 'L\'ordre est requis']"
            />

            <q-toggle
              v-model="specialiteFormData.is_active"
              label="Active"
              color="positive"
            />

            <div class="row justify-end q-gutter-sm q-mt-md">
              <q-btn label="Annuler" flat color="grey-7" v-close-popup />
              <q-btn
                type="submit"
                label="Enregistrer"
                color="primary"
                unelevated
                :loading="submittingSpecialite"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog Confirmation Suppression Spécialité -->
    <q-dialog v-model="showDeleteSpecialiteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="warning" color="negative" text-color="white" />
          <span class="q-ml-sm">Voulez-vous vraiment supprimer cette spécialité ?</span>
        </q-card-section>

        <q-card-section v-if="specialiteToDelete">
          <div class="text-body2 text-grey-8">
            <strong>{{ specialiteToDelete.nom }}</strong> ({{ specialiteToDelete.code }})
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn label="Annuler" flat color="grey-7" v-close-popup />
          <q-btn
            label="Supprimer"
            color="negative"
            unelevated
            @click="deleteSpecialite"
            :loading="deletingSpecialite"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useDeploymentStore } from 'src/stores/deployment'
import { apiService } from 'src/services/api'

const $q = useQuasar()

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
const showSpecialitesDialog = ref(false)
const showSpecialiteFormDialog = ref(false)
const showDeleteSpecialiteDialog = ref(false)
const isEditingSpecialite = ref(false)
const submittingSpecialite = ref(false)
const deletingSpecialite = ref(false)
const specialiteToDelete = ref(null)

const specialiteFormData = ref({
  code: '',
  nom: '',
  description: '',
  couleur: '#000000',
  ordre: 0,
  is_active: true
})

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

const specialitesColumns = [
  { name: 'code', label: 'Code', field: 'code', align: 'left', sortable: true },
  { name: 'nom', label: 'Nom', field: 'nom', align: 'left', sortable: true },
  { name: 'couleur', label: 'Couleur', field: 'couleur', align: 'center' },
  { name: 'ordre', label: 'Ordre', field: 'ordre', align: 'center', sortable: true },
  { name: 'technicians_count', label: 'Techniciens', field: 'technicians_count', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

// ============================================
// METHODS - UTILS
// ============================================

function getSpecialiteLabel(specialiteId) {
  const specialite = specialites.value.find(s => s.id === specialiteId)
  return specialite ? specialite.nom : 'Non défini'
}

function getSpecialiteColor(specialiteId) {
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
    specialites.value = response.data
  } catch (error) {
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
  showSpecialitesDialog.value = true
  loadSpecialites()
}

function openSpecialiteForm() {
  isEditingSpecialite.value = false
  specialiteFormData.value = {
    code: '',
    nom: '',
    description: '',
    couleur: '#000000',
    ordre: specialites.value.length,
    is_active: true
  }
  showSpecialiteFormDialog.value = true
}

function editSpecialite(specialite) {
  isEditingSpecialite.value = true
  specialiteFormData.value = { ...specialite }
  showSpecialiteFormDialog.value = true
}

async function saveSpecialite() {
  submittingSpecialite.value = true
  try {
    if (isEditingSpecialite.value) {
      await apiService.deployment.specialites.update(specialiteFormData.value.id, specialiteFormData.value)
      $q.notify({
        type: 'positive',
        message: 'Spécialité modifiée avec succès'
      })
    } else {
      await apiService.deployment.specialites.create(specialiteFormData.value)
      $q.notify({
        type: 'positive',
        message: 'Spécialité créée avec succès'
      })
    }
    showSpecialiteFormDialog.value = false
    await loadSpecialites()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de l\'enregistrement',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    submittingSpecialite.value = false
  }
}

function confirmDeleteSpecialite(specialite) {
  specialiteToDelete.value = specialite
  showDeleteSpecialiteDialog.value = true
}

async function deleteSpecialite() {
  deletingSpecialite.value = true
  try {
    await apiService.deployment.specialites.delete(specialiteToDelete.value.id)
    $q.notify({
      type: 'positive',
      message: 'Spécialité supprimée avec succès'
    })
    showDeleteSpecialiteDialog.value = false
    await loadSpecialites()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de la suppression',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    deletingSpecialite.value = false
  }
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
