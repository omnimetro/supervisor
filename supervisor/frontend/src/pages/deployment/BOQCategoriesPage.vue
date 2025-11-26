<template>
  <q-page class="q-pa-md">
    <!-- En-tête de page -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h4 text-weight-bold text-primary">Catégories BOQ</div>
        <div class="text-subtitle2 text-grey-7">Regroupement des travaux (GC, FO, Réseau...)</div>
      </div>
      <q-btn
        color="primary"
        icon="add"
        label="Nouvelle Catégorie"
        @click="openCreateDialog"
        unelevated
      />
    </div>

    <!-- Filtres et recherche -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <q-input
              v-model="searchQuery"
              outlined
              dense
              placeholder="Rechercher une catégorie..."
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
          <div class="col-12 col-md-3">
            <q-btn
              color="secondary"
              icon="refresh"
              label="Actualiser"
              @click="loadCategories"
              outline
              class="full-width"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Tableau des catégories -->
    <q-card>
      <q-card-section>
        <q-table
          :rows="categories"
          :columns="columns"
          :loading="loading"
          row-key="id"
          flat
          :pagination="pagination"
          @request="onTableRequest"
          binary-state-sort
        >
          <!-- Slot personnalisé pour le statut -->
          <template v-slot:body-cell-is_active="props">
            <q-td :props="props">
              <q-badge
                :color="props.row.is_active ? 'positive' : 'negative'"
                :label="props.row.is_active ? 'Active' : 'Inactive'"
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
                icon="visibility"
                @click="viewCategory(props.row)"
              >
                <q-tooltip>Voir</q-tooltip>
              </q-btn>
              <q-btn
                flat
                dense
                round
                color="primary"
                icon="edit"
                @click="editCategory(props.row)"
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

    <!-- Dialog de formulaire -->
    <q-dialog v-model="showFormDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center">
          <div class="text-h6">{{ isEditing ? 'Modifier' : 'Créer' }} une catégorie BOQ</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section class="q-gutter-md">
          <q-input
            v-model="formData.code"
            label="Code *"
            outlined
            maxlength="20"
            hint="Ex: GC, FO, RESEAU"
            :rules="[val => !!val || 'Le code est requis']"
          />

          <q-input
            v-model="formData.nom"
            label="Nom de la catégorie *"
            outlined
            hint="Ex: Travaux Génie Civil"
            :rules="[val => !!val || 'Le nom est requis']"
          />

          <q-input
            v-model="formData.description"
            label="Description"
            type="textarea"
            outlined
            rows="3"
          />

          <q-toggle
            v-model="formData.is_active"
            label="Catégorie active"
            color="positive"
          />
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            :label="isEditing ? 'Modifier' : 'Créer'"
            color="primary"
            @click="saveCategory"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog de visualisation -->
    <q-dialog v-model="showViewDialog">
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center">
          <div class="text-h6">Détails de la catégorie</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section v-if="selectedCategory" class="q-gutter-md">
          <div>
            <div class="text-caption text-grey-7">Code</div>
            <div class="text-body1 text-weight-medium">{{ selectedCategory.code }}</div>
          </div>
          <div>
            <div class="text-caption text-grey-7">Nom</div>
            <div class="text-body1">{{ selectedCategory.nom }}</div>
          </div>
          <div v-if="selectedCategory.description">
            <div class="text-caption text-grey-7">Description</div>
            <div class="text-body1">{{ selectedCategory.description }}</div>
          </div>
          <div>
            <div class="text-caption text-grey-7">Statut</div>
            <q-badge
              :color="selectedCategory.is_active ? 'positive' : 'negative'"
              :label="selectedCategory.is_active ? 'Active' : 'Inactive'"
            />
          </div>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat label="Fermer" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog de confirmation de suppression -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="warning" color="negative" text-color="white" />
          <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer cette catégorie ?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            label="Supprimer"
            color="negative"
            @click="deleteCategory"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDeploymentStore } from 'src/stores/deployment'

// ============================================
// STORE
// ============================================

const deploymentStore = useDeploymentStore()

// ============================================
// STATE
// ============================================

const showFormDialog = ref(false)
const showViewDialog = ref(false)
const showDeleteDialog = ref(false)
const isEditing = ref(false)
const selectedCategory = ref(null)

const searchQuery = ref('')
const filterStatus = ref(null)

const formData = ref({
  code: '',
  nom: '',
  description: '',
  is_active: true
})

const pagination = ref({
  sortBy: 'nom',
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

// État local pour les données
const categories = ref([])
const loading = ref(false)

// ============================================
// OPTIONS
// ============================================

const statusOptions = [
  { label: 'Tous', value: null },
  { label: 'Active', value: true },
  { label: 'Inactive', value: false }
]

const columns = [
  {
    name: 'code',
    label: 'Code',
    field: 'code',
    align: 'left',
    sortable: true
  },
  {
    name: 'nom',
    label: 'Nom',
    field: 'nom',
    align: 'left',
    sortable: true
  },
  {
    name: 'description',
    label: 'Description',
    field: 'description',
    align: 'left',
    format: val => val ? (val.length > 60 ? val.substring(0, 60) + '...' : val) : '-'
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
// METHODS
// ============================================

async function loadCategories(params = {}) {
  loading.value = true
  try {
    const result = await deploymentStore.boqCategories.list(params)
    categories.value = Array.isArray(result) ? result : []

    if (deploymentStore.boqCategories?.pagination?.value?.rowsNumber !== undefined) {
      pagination.value.rowsNumber = deploymentStore.boqCategories.pagination.value.rowsNumber
    }
  } catch (error) {
    console.error('Erreur chargement catégories BOQ:', error)
    categories.value = []
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

  if (filterStatus.value !== null) {
    params.is_active = filterStatus.value
  }

  await loadCategories(params)
  pagination.value = props.pagination
}

function onSearch() {
  loadCategories({
    search: searchQuery.value,
    is_active: filterStatus.value
  })
}

function onFilter() {
  loadCategories({
    search: searchQuery.value,
    is_active: filterStatus.value
  })
}

function openCreateDialog() {
  resetForm()
  showFormDialog.value = true
}

function viewCategory(category) {
  selectedCategory.value = category
  showViewDialog.value = true
}

function editCategory(category) {
  isEditing.value = true
  selectedCategory.value = category
  formData.value = { ...category }
  showFormDialog.value = true
}

function resetForm() {
  isEditing.value = false
  selectedCategory.value = null
  formData.value = {
    code: '',
    nom: '',
    description: '',
    is_active: true
  }
}

async function saveCategory() {
  try {
    if (isEditing.value) {
      await deploymentStore.boqCategories.update(selectedCategory.value.id, formData.value)
    } else {
      await deploymentStore.boqCategories.create(formData.value)
    }

    showFormDialog.value = false
    resetForm()
    await loadCategories()
  } catch (error) {
    console.error('Erreur sauvegarde catégorie BOQ:', error)
  }
}

function confirmDelete(category) {
  selectedCategory.value = category
  showDeleteDialog.value = true
}

async function deleteCategory() {
  try {
    await deploymentStore.boqCategories.remove(selectedCategory.value.id)
    showDeleteDialog.value = false
    selectedCategory.value = null
    await loadCategories()
  } catch (error) {
    console.error('Erreur suppression catégorie BOQ:', error)
  }
}

// ============================================
// LIFECYCLE
// ============================================

onMounted(() => {
  loadCategories()
})
</script>
