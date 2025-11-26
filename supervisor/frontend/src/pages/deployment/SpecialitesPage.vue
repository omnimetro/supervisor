<template>
  <q-page class="q-pa-md">
    <!--En-tête de page -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h4 text-weight-bold text-primary">Spécialités Techniques</div>
        <div class="text-subtitle2 text-grey-7">Gestion des spécialités des techniciens AIV</div>
      </div>
      <q-btn
        color="primary"
        icon="add"
        label="Nouvelle Spécialité"
        @click="openCreateDialog"
        unelevated
      />
    </div>

    <!-- Statistiques -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-md-4">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-primary">{{ stats.total }}</div>
            <div class="text-caption text-grey-7">Total Spécialités</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-4">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-positive">{{ stats.actives }}</div>
            <div class="text-caption text-grey-7">Actives</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-4">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-accent">{{ stats.techniciens }}</div>
            <div class="text-caption text-grey-7">Techniciens Affectés</div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Recherche -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <q-input
              v-model="searchQuery"
              outlined
              dense
              placeholder="Rechercher une spécialité..."
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
          <div class="col-12 col-md-3 text-right">
            <q-btn
              flat
              dense
              icon="refresh"
              label="Actualiser"
              @click="fetchSpecialites"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Table des spécialités -->
    <q-card>
      <q-card-section>
        <q-table
          :rows="specialites"
          :columns="columns"
          row-key="id"
          :loading="loading"
          :pagination="pagination"
          @request="onRequest"
          binary-state-sort
          flat
        >
          <!-- Couleur -->
          <template v-slot:body-cell-couleur="props">
            <q-td :props="props">
              <div
                :style="{ backgroundColor: props.value, width: '50px', height: '25px', border: '1px solid #ccc', borderRadius: '4px' }"
              ></div>
            </q-td>
          </template>

          <!-- Techniciens count -->
          <template v-slot:body-cell-technicians_count="props">
            <q-td :props="props">
              <q-badge color="primary">{{ props.value }}</q-badge>
            </q-td>
          </template>

          <!-- Statut -->
          <template v-slot:body-cell-is_active="props">
            <q-td :props="props">
              <q-badge :color="props.value ? 'positive' : 'negative'">
                {{ props.value ? 'Active' : 'Inactive' }}
              </q-badge>
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
                @click="openEditDialog(props.row)"
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
                @click="confirmDelete(props.row)"
              >
                <q-tooltip>Supprimer</q-tooltip>
              </q-btn>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Dialog Créer/Modifier -->
    <q-dialog v-model="showDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center bg-primary text-white">
          <div class="text-h6">{{ dialogMode === 'create' ? 'Nouvelle Spécialité' : 'Modifier Spécialité' }}</div>
          <q-space />
          <q-btn flat dense round icon="close" v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="handleSubmit" class="q-gutter-md">
            <q-input
              v-model="formData.code"
              label="Code *"
              outlined
              dense
              :rules="[val => !!val || 'Le code est requis']"
            />

            <q-input
              v-model="formData.nom"
              label="Nom *"
              outlined
              dense
              :rules="[val => !!val || 'Le nom est requis']"
            />

            <q-input
              v-model="formData.description"
              label="Description"
              outlined
              dense
              type="textarea"
              rows="3"
            />

            <q-input
              v-model="formData.couleur"
              label="Couleur *"
              outlined
              dense
              :rules="[val => !!val || 'La couleur est requise']"
            >
              <template v-slot:append>
                <q-icon name="colorize" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-color v-model="formData.couleur" />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>

            <q-input
              v-model.number="formData.ordre"
              label="Ordre d'affichage *"
              outlined
              dense
              type="number"
              :rules="[val => val !== null && val !== '' || 'L\'ordre est requis']"
            />

            <q-toggle
              v-model="formData.is_active"
              label="Active"
              color="positive"
            />

            <div class="row justify-end q-gutter-sm q-mt-md">
              <q-btn label="Annuler" flat color="grey-7" v-close-popup />
              <q-btn type="submit" label="Enregistrer" color="primary" unelevated :loading="submitting" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog Confirmation Suppression -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="warning" color="negative" text-color="white" />
          <span class="q-ml-sm">Voulez-vous vraiment supprimer cette spécialité ?</span>
        </q-card-section>

        <q-card-section v-if="itemToDelete">
          <div class="text-body2 text-grey-8">
            <strong>{{ itemToDelete.nom }}</strong> ({{ itemToDelete.code }})
          </div>
          <div v-if="itemToDelete.technicians_count > 0" class="text-caption text-negative q-mt-sm">
            Attention : {{ itemToDelete.technicians_count }} technicien(s) utilisent cette spécialité.
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn label="Annuler" flat color="grey-7" v-close-popup />
          <q-btn label="Supprimer" color="negative" unelevated @click="handleDelete" :loading="deleting" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { apiService } from 'src/services/api'

const $q = useQuasar()

// État
const loading = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const specialites = ref([])
const searchQuery = ref('')
const filterStatus = ref(null)

// Statistiques
const stats = computed(() => {
  if (!Array.isArray(specialites.value)) {
    return {
      total: 0,
      actives: 0,
      techniciens: 0
    }
  }
  return {
    total: specialites.value.length,
    actives: specialites.value.filter(s => s.is_active).length,
    techniciens: specialites.value.reduce((sum, s) => sum + (s.technicians_count || 0), 0)
  }
})

// Configuration table
const columns = [
  { name: 'code', label: 'Code', field: 'code', align: 'left', sortable: true },
  { name: 'nom', label: 'Nom', field: 'nom', align: 'left', sortable: true },
  { name: 'description', label: 'Description', field: 'description', align: 'left' },
  { name: 'couleur', label: 'Couleur', field: 'couleur', align: 'center' },
  { name: 'ordre', label: 'Ordre', field: 'ordre', align: 'center', sortable: true },
  { name: 'technicians_count', label: 'Techniciens', field: 'technicians_count', align: 'center', sortable: true },
  { name: 'is_active', label: 'Statut', field: 'is_active', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const pagination = ref({
  sortBy: 'ordre',
  descending: false,
  page: 1,
  rowsPerPage: 20
})

// Options
const statusOptions = [
  { label: 'Active', value: true },
  { label: 'Inactive', value: false }
]

// Dialog
const showDialog = ref(false)
const dialogMode = ref('create') // 'create' ou 'edit'
const formData = ref({
  code: '',
  nom: '',
  description: '',
  couleur: '#000000',
  ordre: 0,
  is_active: true
})

const showDeleteDialog = ref(false)
const itemToDelete = ref(null)

// Méthodes
const fetchSpecialites = async () => {
  loading.value = true
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
    loading.value = false
  }
}

const onRequest = (props) => {
  pagination.value = props.pagination
}

const onSearch = () => {
  fetchSpecialites()
}

const onFilter = () => {
  fetchSpecialites()
}

const openCreateDialog = () => {
  dialogMode.value = 'create'
  formData.value = {
    code: '',
    nom: '',
    description: '',
    couleur: '#000000',
    ordre: specialites.value.length,
    is_active: true
  }
  showDialog.value = true
}

const openEditDialog = (specialite) => {
  dialogMode.value = 'edit'
  formData.value = { ...specialite }
  showDialog.value = true
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    if (dialogMode.value === 'create') {
      await apiService.deployment.specialites.create(formData.value)
      $q.notify({
        type: 'positive',
        message: 'Spécialité créée avec succès'
      })
    } else {
      await apiService.deployment.specialites.update(formData.value.id, formData.value)
      $q.notify({
        type: 'positive',
        message: 'Spécialité modifiée avec succès'
      })
    }
    showDialog.value = false
    fetchSpecialites()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de l\'enregistrement',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    submitting.value = false
  }
}

const confirmDelete = (specialite) => {
  itemToDelete.value = specialite
  showDeleteDialog.value = true
}

const handleDelete = async () => {
  deleting.value = true
  try {
    await apiService.deployment.specialites.delete(itemToDelete.value.id)
    $q.notify({
      type: 'positive',
      message: 'Spécialité supprimée avec succès'
    })
    showDeleteDialog.value = false
    fetchSpecialites()
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de la suppression',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    deleting.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchSpecialites()
})
</script>

<style scoped>
.q-table th {
  font-weight: 600;
}
</style>
