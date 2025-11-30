<template>
  <q-page padding>
    <!-- En-tête de la page -->
    <div class="row items-center justify-between mb-md">
      <div>
        <h1 class="text-h4 text-brand q-mb-xs">Documents de Projet</h1>
        <p class="text-body text-secondary">
          Gérez tous les documents liés aux projets (BOM, MAP, SYNOPTIQUE, etc.)
        </p>
      </div>
      <q-btn
        color="primary"
        icon="add"
        label="Ajouter un Document"
        @click="openCreateDialog"
        unelevated
      />
    </div>

    <!-- Filtres -->
    <q-card flat bordered class="rounded-lg q-mb-md">
      <q-card-section>
        <div class="row q-gutter-md">
          <q-select
            v-model="filterProject"
            :options="projectOptions"
            label="Filtrer par Projet"
            outlined
            dense
            clearable
            emit-value
            map-options
            option-value="value"
            option-label="label"
            style="min-width: 250px"
            @update:model-value="onFilterChange"
          />
          <q-select
            v-model="filterType"
            :options="typeOptions"
            label="Filtrer par Type"
            outlined
            dense
            clearable
            emit-value
            map-options
            option-value="value"
            option-label="label"
            style="min-width: 200px"
            @update:model-value="onFilterChange"
          />
        </div>
      </q-card-section>
    </q-card>

    <!-- Tableau des documents -->
    <q-card flat bordered class="rounded-lg">
      <q-card-section class="q-pa-none">
        <q-table
          :rows="documents"
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
              <q-icon name="folder" size="md" color="primary" />
              <span class="text-h6">Liste des Documents</span>
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

          <!-- Colonne Fichier -->
          <template v-slot:body-cell-fichier="props">
            <q-td :props="props">
              <q-btn
                v-if="props.row.fichier"
                icon="download"
                size="sm"
                flat
                round
                color="primary"
                @click="downloadFile(props.row)"
              >
                <q-tooltip>Télécharger</q-tooltip>
              </q-btn>
              <span v-else class="text-grey">-</span>
            </q-td>
          </template>

          <!-- Colonne Taille -->
          <template v-slot:body-cell-taille_fichier_formatted="props">
            <q-td :props="props">
              <q-badge
                color="info"
                :label="props.row.taille_fichier_formatted || '-'"
              />
            </q-td>
          </template>

          <!-- Colonne Actions -->
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <div class="row q-gutter-xs">
                <q-btn
                  icon="visibility"
                  size="sm"
                  flat
                  round
                  color="info"
                  @click="viewDocument(props.row)"
                >
                  <q-tooltip>Voir détails</q-tooltip>
                </q-btn>
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
      <q-card style="min-width: 600px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">
            {{ isEditing ? 'Modifier le Document' : 'Nouveau Document' }}
          </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveDocument" class="q-gutter-md">
            <!-- Projet -->
            <q-select
              v-model="formData.project"
              :options="projectOptions"
              label="Projet *"
              outlined
              emit-value
              map-options
              option-value="value"
              option-label="label"
              :rules="[val => !!val || 'Le projet est requis']"
              lazy-rules
            />

            <!-- Type de Document avec bouton -->
            <div class="row q-gutter-sm items-end">
              <q-select
                v-model="formData.type_document"
                :options="typeOptions"
                label="Type de Document *"
                outlined
                emit-value
                map-options
                option-value="value"
                option-label="label"
                :rules="[val => !!val || 'Le type est requis']"
                lazy-rules
                class="col"
              />
              <q-btn
                icon="add_circle"
                color="secondary"
                outline
                label="Nouveau Type"
                @click="navigateToTypeDocuments"
                type="button"
              >
                <q-tooltip>Créer un nouveau type de document</q-tooltip>
              </q-btn>
            </div>

            <!-- Nom du Document -->
            <q-input
              v-model="formData.nom"
              label="Nom du Document *"
              outlined
              :rules="[
                val => !!val || 'Le nom est requis',
                val => val.length >= 3 || 'Minimum 3 caractères',
                val => val.length <= 200 || 'Maximum 200 caractères'
              ]"
              lazy-rules
              maxlength="200"
            />

            <!-- Upload de Fichier -->
            <q-file
              v-model="formData.fichier"
              label="Fichier *"
              outlined
              clearable
              accept=".pdf,.doc,.docx,.xls,.xlsx,.dwg,.kmz,.zip"
              max-file-size="104857600"
              :rules="[val => isEditing || !!val || 'Le fichier est requis']"
              lazy-rules
              @update:model-value="onFileChange"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
              <template v-slot:hint>
                Formats acceptés : PDF, DOC, DOCX, XLS, XLSX, DWG, KMZ, ZIP (max 100 MB)
              </template>
            </q-file>

            <!-- Version -->
            <q-input
              v-model="formData.version"
              label="Version"
              hint="Ex: 1.0, v2.1, etc."
              outlined
              maxlength="20"
            />

            <!-- Description -->
            <q-input
              v-model="formData.description"
              label="Description"
              type="textarea"
              outlined
              rows="3"
              hint="Description optionnelle"
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

    <!-- Dialog Détails -->
    <q-dialog v-model="showDetailsDialog">
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Détails du Document</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section v-if="selectedDocument">
          <q-list>
            <q-item>
              <q-item-section>
                <q-item-label caption>Nom</q-item-label>
                <q-item-label>{{ selectedDocument.nom }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label caption>Projet</q-item-label>
                <q-item-label>{{ selectedDocument.project_code }} - {{ selectedDocument.project_nom }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label caption>Type</q-item-label>
                <q-item-label>{{ selectedDocument.type_document_nom }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label caption>Version</q-item-label>
                <q-item-label>{{ selectedDocument.version || '-' }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label caption>Taille</q-item-label>
                <q-item-label>{{ selectedDocument.taille_fichier_formatted || '-' }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label caption>Uploadé par</q-item-label>
                <q-item-label>{{ selectedDocument.uploaded_by_profil_nom || '-' }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label caption>Date d'upload</q-item-label>
                <q-item-label>{{ formatDate(selectedDocument.date_upload) }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-item v-if="selectedDocument.description">
              <q-item-section>
                <q-item-label caption>Description</q-item-label>
                <q-item-label>{{ selectedDocument.description }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            v-if="selectedDocument && selectedDocument.fichier"
            label="Télécharger"
            color="primary"
            icon="download"
            @click="downloadFile(selectedDocument)"
            unelevated
          />
          <q-btn label="Fermer" color="grey" flat v-close-popup />
        </q-card-actions>
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
          Êtes-vous sûr de vouloir supprimer le document
          <strong>{{ documentToDelete?.nom }}</strong> ?
          <br><br>
          <span class="text-grey">Cette action est irréversible.</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn label="Annuler" color="grey" flat v-close-popup />
          <q-btn
            label="Supprimer"
            color="negative"
            unelevated
            @click="deleteDocument"
            :loading="deleting"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useQuasar, date } from 'quasar'
import { useRouter } from 'vue-router'
import { apiService } from 'src/services/api'

// ============================================
// Composables
// ============================================

const $q = useQuasar()
const router = useRouter()

// ============================================
// État Réactif
// ============================================

const documents = ref([])
const projects = ref([])
const typeDocuments = ref([])
const loading = ref(false)
const loadingProjects = ref(false)
const loadingTypes = ref(false)
const saving = ref(false)
const deleting = ref(false)
const searchQuery = ref('')
const filterProject = ref(null)
const filterType = ref(null)

const showDialog = ref(false)
const showDetailsDialog = ref(false)
const showDeleteDialog = ref(false)
const isEditing = ref(false)
const selectedDocument = ref(null)
const documentToDelete = ref(null)

const formData = ref({
  nom: '',
  project: null,
  type_document: null,
  fichier: null,
  version: '',
  description: ''
})

const pagination = ref({
  page: 1,
  rowsPerPage: 20,
  rowsNumber: 0
})

// ============================================
// Computed
// ============================================

const projectOptions = computed(() => {
  if (!Array.isArray(projects.value)) return []
  return projects.value.map(p => ({
    label: `${p.code} - ${p.nom}`,
    value: p.id
  }))
})

const typeOptions = computed(() => {
  if (!Array.isArray(typeDocuments.value)) return []
  return typeDocuments.value
    .filter(t => t.is_active)
    .map(t => ({
      label: t.nom,
      value: t.id
    }))
})

// ============================================
// Configuration du Tableau
// ============================================

const columns = [
  {
    name: 'nom',
    label: 'Nom',
    field: 'nom',
    align: 'left',
    sortable: true
  },
  {
    name: 'project_code',
    label: 'Projet',
    field: 'project_code',
    align: 'left',
    sortable: true
  },
  {
    name: 'type_document_nom',
    label: 'Type',
    field: 'type_document_nom',
    align: 'left',
    sortable: true
  },
  {
    name: 'version',
    label: 'Version',
    field: 'version',
    align: 'center'
  },
  {
    name: 'taille_fichier_formatted',
    label: 'Taille',
    field: 'taille_fichier_formatted',
    align: 'center'
  },
  {
    name: 'date_upload',
    label: 'Date Upload',
    field: 'date_upload',
    align: 'center',
    sortable: true,
    format: val => formatDate(val)
  },
  {
    name: 'fichier',
    label: 'Fichier',
    field: 'fichier',
    align: 'center'
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
 * Récupérer les documents depuis l'API
 */
async function fetchDocuments() {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.rowsPerPage,
      search: searchQuery.value
    }

    if (filterProject.value) {
      params.project = filterProject.value
    }
    if (filterType.value) {
      params.type_document = filterType.value
    }

    const response = await apiService.deployment.projectDocuments.list(params)

    // Gérer la pagination de l'API
    if (response.data.results) {
      documents.value = response.data.results
      pagination.value.rowsNumber = response.data.count
    } else if (Array.isArray(response.data)) {
      documents.value = response.data
      pagination.value.rowsNumber = response.data.length
    } else {
      documents.value = []
      pagination.value.rowsNumber = 0
    }
  } catch (error) {
    console.error('Erreur chargement documents:', error)
    documents.value = []
    $q.notify({
      type: 'negative',
      message: 'Erreur lors du chargement des documents',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    loading.value = false
  }
}

/**
 * Récupérer les projets
 */
async function fetchProjects() {
  loadingProjects.value = true
  try {
    const response = await apiService.deployment.projects.list()
    if (response.data.results) {
      projects.value = response.data.results
    } else if (Array.isArray(response.data)) {
      projects.value = response.data
    } else {
      projects.value = []
    }
  } catch (error) {
    console.error('Erreur chargement projets:', error)
    projects.value = []
  } finally {
    loadingProjects.value = false
  }
}

/**
 * Récupérer les types de documents
 */
async function fetchTypeDocuments() {
  loadingTypes.value = true
  try {
    const response = await apiService.deployment.typeDocuments.list()
    if (response.data.results) {
      typeDocuments.value = response.data.results
    } else if (Array.isArray(response.data)) {
      typeDocuments.value = response.data
    } else {
      typeDocuments.value = []
    }
  } catch (error) {
    console.error('Erreur chargement types de documents:', error)
    typeDocuments.value = []
  } finally {
    loadingTypes.value = false
  }
}

/**
 * Gestion de la requête du tableau (pagination, tri, etc.)
 */
function onTableRequest(props) {
  pagination.value.page = props.pagination.page
  pagination.value.rowsPerPage = props.pagination.rowsPerPage
  fetchDocuments()
}

/**
 * Recherche
 */
function onSearch() {
  pagination.value.page = 1
  fetchDocuments()
}

/**
 * Changement de filtre
 */
function onFilterChange() {
  pagination.value.page = 1
  fetchDocuments()
}

/**
 * Ouvrir le dialog de création
 */
function openCreateDialog() {
  isEditing.value = false
  formData.value = {
    nom: '',
    project: null,
    type_document: null,
    fichier: null,
    version: '',
    description: ''
  }
  showDialog.value = true
}

/**
 * Ouvrir le dialog de modification
 */
function openEditDialog(doc) {
  isEditing.value = true
  formData.value = {
    id: doc.id,
    nom: doc.nom,
    project: doc.project,
    type_document: doc.type_document,
    fichier: null, // On ne récupère pas le fichier pour l'édition
    version: doc.version || '',
    description: doc.description || ''
  }
  showDialog.value = true
}

/**
 * Gestion du changement de fichier
 */
function onFileChange(file) {
  if (file) {
    console.log('Fichier sélectionné:', file.name, file.size)
  }
}

/**
 * Enregistrer un document (création ou modification)
 */
async function saveDocument() {
  saving.value = true
  try {
    if (isEditing.value) {
      await apiService.deployment.projectDocuments.update(formData.value.id, formData.value)
      $q.notify({
        type: 'positive',
        message: 'Document modifié avec succès'
      })
    } else {
      await apiService.deployment.projectDocuments.create(formData.value)
      $q.notify({
        type: 'positive',
        message: 'Document créé avec succès'
      })
    }

    showDialog.value = false
    await fetchDocuments()
  } catch (error) {
    console.error('Erreur sauvegarde document:', error)
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
 * Voir les détails d'un document
 */
function viewDocument(doc) {
  selectedDocument.value = doc
  showDetailsDialog.value = true
}

/**
 * Confirmer la suppression
 */
function confirmDelete(doc) {
  documentToDelete.value = doc
  showDeleteDialog.value = true
}

/**
 * Supprimer un document
 */
async function deleteDocument() {
  deleting.value = true
  try {
    await apiService.deployment.projectDocuments.delete(documentToDelete.value.id)
    $q.notify({
      type: 'positive',
      message: 'Document supprimé avec succès'
    })
    showDeleteDialog.value = false
    documentToDelete.value = null
    await fetchDocuments()
  } catch (error) {
    console.error('Erreur suppression document:', error)
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de la suppression',
      caption: error.response?.data?.detail || error.message
    })
  } finally {
    deleting.value = false
  }
}

/**
 * Télécharger un fichier
 */
function downloadFile(doc) {
  if (doc.fichier) {
    window.open(doc.fichier, '_blank')
  }
}

/**
 * Naviguer vers la page des types de documents
 */
function navigateToTypeDocuments() {
  router.push({ name: 'type-documents' })
}

/**
 * Formater une date
 */
function formatDate(dateStr) {
  if (!dateStr) return '-'
  return date.formatDate(dateStr, 'DD/MM/YYYY HH:mm')
}

// ============================================
// Cycle de Vie
// ============================================

onMounted(() => {
  fetchDocuments()
  fetchProjects()
  fetchTypeDocuments()
})
</script>

<style scoped lang="scss">
.sticky-header-table {
  max-height: calc(100vh - 350px);

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
