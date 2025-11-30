<template>
  <q-page padding>
    <!-- En-tête de la page -->
    <div class="row items-center justify-between mb-md">
      <div>
        <h1 class="text-h4 text-brand q-mb-xs">Types de Documents</h1>
        <p class="text-body text-secondary">
          Gérez les types de documents utilisés dans les projets (BOM, MAP, SYNOPTIQUE, AUTRES)
        </p>
      </div>
      <q-btn
        color="primary"
        icon="add"
        label="Nouveau Type"
        @click="openCreateDialog"
        unelevated
      />
    </div>

    <!-- Tableau des types de documents -->
    <q-card flat bordered class="rounded-lg">
      <q-card-section class="q-pa-none">
        <q-table
          :rows="typeDocuments"
          :columns="columns"
          :loading="loading"
          :pagination="pagination"
          @request="onTableRequest"
          row-key="id"
          flat
          class="sticky-header-table"
        >
          <!-- En-tête personnalisé -->
          <template v-slot:top>
            <div class="row items-center q-gutter-sm full-width">
              <q-icon name="description" size="md" color="primary" />
              <span class="text-h6">Liste des Types de Documents</span>
              <q-space />
              <q-input
                v-model="searchQuery"
                placeholder="Rechercher..."
                dense
                outlined
                clearable
                @update:model-value="onSearch"
                style="min-width: 300px"
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
          </template>

          <!-- Colonne Statut -->
          <template v-slot:body-cell-is_active="props">
            <q-td :props="props">
              <q-badge
                :color="props.row.is_active ? 'positive' : 'negative'"
                :label="props.row.is_active ? 'Actif' : 'Inactif'"
              />
            </q-td>
          </template>

          <!-- Colonne Documents Count -->
          <template v-slot:body-cell-documents_count="props">
            <q-td :props="props">
              <q-badge
                color="info"
                :label="props.row.documents_count || 0"
              />
            </q-td>
          </template>

          <!-- Colonne Actions -->
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <div class="row q-gutter-xs">
                <q-btn
                  icon="edit"
                  size="sm"
                  flat
                  round
                  color="primary"
                  @click="openEditDialog(props.row)"
                >
                  <q-tooltip>Modifier</q-tooltip>
                </q-btn>
                <q-btn
                  icon="delete"
                  size="sm"
                  flat
                  round
                  color="negative"
                  @click="confirmDelete(props.row)"
                >
                  <q-tooltip>Supprimer</q-tooltip>
                </q-btn>
              </div>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Dialog Création/Modification -->
    <q-dialog v-model="showDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">
            {{ isEditing ? 'Modifier le Type de Document' : 'Nouveau Type de Document' }}
          </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveTypeDocument" class="q-gutter-md">
            <q-input
              v-model="formData.code"
              label="Code *"
              hint="Code unique (ex: BOM, MAP, SYNOPTIQUE, AUTRES)"
              outlined
              :rules="[
                val => !!val || 'Le code est requis',
                val => val.length >= 2 || 'Minimum 2 caractères',
                val => val.length <= 20 || 'Maximum 20 caractères'
              ]"
              lazy-rules
              maxlength="20"
            />

            <q-input
              v-model="formData.nom"
              label="Nom *"
              hint="Nom complet du type de document"
              outlined
              :rules="[
                val => !!val || 'Le nom est requis',
                val => val.length >= 3 || 'Minimum 3 caractères',
                val => val.length <= 100 || 'Maximum 100 caractères'
              ]"
              lazy-rules
              maxlength="100"
            />

            <q-input
              v-model="formData.description"
              label="Description"
              type="textarea"
              outlined
              rows="3"
              hint="Description optionnelle"
            />

            <q-toggle
              v-model="formData.is_active"
              label="Type actif"
              color="positive"
            />

            <div class="row justify-end q-gutter-sm q-mt-md">
              <q-btn
                label="Annuler"
                color="grey"
                flat
                v-close-popup
              />
              <q-btn
                label="Enregistrer"
                type="submit"
                color="primary"
                unelevated
                :loading="saving"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog de Confirmation de Suppression -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-icon name="warning" color="warning" size="md" class="q-mr-sm" />
          <span class="text-h6">Confirmer la suppression</span>
        </q-card-section>

        <q-card-section>
          Êtes-vous sûr de vouloir supprimer le type de document
          <strong>{{ typeToDelete?.nom }}</strong> ?
          <br><br>
          <span v-if="typeToDelete?.documents_count > 0" class="text-negative">
            Attention : Ce type est utilisé par {{ typeToDelete.documents_count }} document(s).
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn label="Annuler" color="grey" flat v-close-popup />
          <q-btn
            label="Supprimer"
            color="negative"
            unelevated
            @click="deleteTypeDocument"
            :loading="deleting"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { apiService } from 'src/services/api'

// ============================================
// État Réactif
// ============================================

const $q = useQuasar()
const typeDocuments = ref([])
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const searchQuery = ref('')

const showDialog = ref(false)
const showDeleteDialog = ref(false)
const isEditing = ref(false)
const typeToDelete = ref(null)

const formData = ref({
  code: '',
  nom: '',
  description: '',
  is_active: true
})

const pagination = ref({
  page: 1,
  rowsPerPage: 20,
  rowsNumber: 0
})

// ============================================
// Configuration du Tableau
// ============================================

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
    align: 'left'
  },
  {
    name: 'is_active',
    label: 'Statut',
    field: 'is_active',
    align: 'center',
    sortable: true
  },
  {
    name: 'documents_count',
    label: 'Nb Documents',
    field: 'documents_count',
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
// Fonctions
// ============================================

/**
 * Récupérer les types de documents depuis l'API
 */
async function fetchTypeDocuments() {
  loading.value = true
  try {
    const response = await apiService.deployment.typeDocuments.list({
      page: pagination.value.page,
      page_size: pagination.value.rowsPerPage,
      search: searchQuery.value
    })

    // Gérer la pagination de l'API
    if (response.data.results) {
      typeDocuments.value = response.data.results
      pagination.value.rowsNumber = response.data.count
    } else if (Array.isArray(response.data)) {
      typeDocuments.value = response.data
      pagination.value.rowsNumber = response.data.length
    } else {
      typeDocuments.value = []
      pagination.value.rowsNumber = 0
    }
  } catch (error) {
    console.error('Erreur chargement types de documents:', error)
    typeDocuments.value = []
    $q.notify({
      type: 'negative',
      message: 'Erreur lors du chargement des types de documents',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    loading.value = false
  }
}

/**
 * Gestion de la requête du tableau (pagination, tri, etc.)
 */
function onTableRequest(props) {
  pagination.value.page = props.pagination.page
  pagination.value.rowsPerPage = props.pagination.rowsPerPage
  fetchTypeDocuments()
}

/**
 * Recherche
 */
function onSearch() {
  pagination.value.page = 1
  fetchTypeDocuments()
}

/**
 * Ouvrir le dialog de création
 */
function openCreateDialog() {
  isEditing.value = false
  formData.value = {
    code: '',
    nom: '',
    description: '',
    is_active: true
  }
  showDialog.value = true
}

/**
 * Ouvrir le dialog de modification
 */
function openEditDialog(type) {
  isEditing.value = true
  formData.value = {
    id: type.id,
    code: type.code,
    nom: type.nom,
    description: type.description || '',
    is_active: type.is_active
  }
  showDialog.value = true
}

/**
 * Enregistrer un type de document (création ou modification)
 */
async function saveTypeDocument() {
  saving.value = true
  try {
    if (isEditing.value) {
      await apiService.deployment.typeDocuments.update(formData.value.id, formData.value)
      $q.notify({
        type: 'positive',
        message: 'Type de document modifié avec succès'
      })
    } else {
      await apiService.deployment.typeDocuments.create(formData.value)
      $q.notify({
        type: 'positive',
        message: 'Type de document créé avec succès'
      })
    }

    showDialog.value = false
    await fetchTypeDocuments()
  } catch (error) {
    console.error('Erreur sauvegarde type de document:', error)
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de la sauvegarde',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    saving.value = false
  }
}

/**
 * Confirmer la suppression
 */
function confirmDelete(type) {
  typeToDelete.value = type
  showDeleteDialog.value = true
}

/**
 * Supprimer un type de document
 */
async function deleteTypeDocument() {
  deleting.value = true
  try {
    await apiService.deployment.typeDocuments.delete(typeToDelete.value.id)
    $q.notify({
      type: 'positive',
      message: 'Type de document supprimé avec succès'
    })
    showDeleteDialog.value = false
    typeToDelete.value = null
    await fetchTypeDocuments()
  } catch (error) {
    console.error('Erreur suppression type de document:', error)
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de la suppression',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    deleting.value = false
  }
}

// ============================================
// Cycle de Vie
// ============================================

onMounted(() => {
  fetchTypeDocuments()
})
</script>

<style scoped lang="scss">
.sticky-header-table {
  max-height: calc(100vh - 250px);

  :deep(thead tr th) {
    position: sticky;
    z-index: 1;
    background-color: #f5f5f5;
  }

  :deep(thead tr:first-child th) {
    top: 0;
  }
}
</style>
