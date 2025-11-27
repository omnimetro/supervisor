<template>
  <q-page class="q-pa-md">
    <!-- En-tête de page -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h4 text-weight-bold text-primary">Sous-traitants</div>
        <div class="text-subtitle2 text-grey-7">Gestion des partenaires sous-traitants</div>
      </div>
      <q-btn
        color="primary"
        icon="add"
        label="Nouveau Sous-traitant"
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
              placeholder="Rechercher un sous-traitant..."
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
              @click="loadSubcontractors"
              outline
              class="full-width"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Tableau des sous-traitants -->
    <q-card>
      <q-card-section>
        <q-table
          :rows="subcontractors"
          :columns="columns"
          :loading="loading"
          row-key="id"
          flat
          :pagination="pagination"
          @request="onTableRequest"
          binary-state-sort
        >
          <!-- Slot personnalisé pour le nom avec sigle -->
          <template v-slot:body-cell-nom="props">
            <q-td :props="props">
              <div>
                <div class="text-weight-medium">{{ props.row.nom }}</div>
                <div class="text-caption text-grey-7">{{ props.row.sigle }}</div>
              </div>
            </q-td>
          </template>

          <!-- Slot personnalisé pour le statut -->
          <template v-slot:body-cell-actif="props">
            <q-td :props="props">
              <q-badge
                :color="props.row.actif ? 'positive' : 'negative'"
                :label="props.row.actif ? 'Actif' : 'Inactif'"
              />
            </q-td>
          </template>

          <!-- Slot personnalisé pour les domaines de compétence -->
          <template v-slot:body-cell-domaines_competence="props">
            <q-td :props="props">
              <div class="text-caption" style="max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                {{ props.row.domaines_competence || '-' }}
              </div>
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
                @click="viewSubcontractor(props.row)"
              >
                <q-tooltip>Voir</q-tooltip>
              </q-btn>
              <q-btn
                flat
                dense
                round
                color="primary"
                icon="edit"
                @click="editSubcontractor(props.row)"
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
      <q-card style="min-width: 700px">
        <q-card-section class="row items-center">
          <div class="text-h6">{{ isEditing ? 'Modifier' : 'Créer' }} un sous-traitant</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 70vh" class="scroll">
          <q-form @submit="saveSubcontractor" class="q-gutter-md">
            <div class="row q-col-gutter-md">
              <div class="col-4">
                <q-input
                  v-model="formData.code"
                  label="Code *"
                  outlined
                  maxlength="20"
                  :rules="[val => !!val || 'Le code est requis']"
                  hint="Ex: ST001"
                />
              </div>
              <div class="col-8">
                <q-input
                  v-model="formData.nom"
                  label="Nom de l'entreprise *"
                  outlined
                  :rules="[val => !!val || 'Le nom est requis']"
                />
              </div>
            </div>

            <div class="row q-col-gutter-md">
              <div class="col-6">
                <q-input
                  v-model="formData.telephone"
                  label="Téléphone"
                  outlined
                />
              </div>
              <div class="col-6">
                <q-input
                  v-model="formData.email"
                  label="Email"
                  type="email"
                  outlined
                />
              </div>
            </div>

            <q-input
              v-model="formData.adresse"
              label="Adresse"
              type="textarea"
              outlined
              rows="2"
            />

            <div class="row q-col-gutter-md">
              <div class="col-6">
                <q-input
                  v-model="formData.contact_principal_nom"
                  label="Nom du contact principal"
                  outlined
                />
              </div>
              <div class="col-6">
                <q-input
                  v-model="formData.contact_principal_telephone"
                  label="Téléphone du contact"
                  outlined
                />
              </div>
            </div>

            <q-input
              v-model="formData.specialites"
              label="Spécialités"
              type="textarea"
              outlined
              rows="3"
              hint="Ex: Génie civil, Tirage de câbles, Soudure, etc."
            />

            <div class="row q-col-gutter-md">
              <div class="col-6">
                <q-input
                  v-model="formData.numero_registre_commerce"
                  label="Numéro de Registre de Commerce"
                  outlined
                />
              </div>
              <div class="col-6">
                <q-input
                  v-model="formData.date_debut_collaboration"
                  label="Date de début de collaboration"
                  type="date"
                  outlined
                />
              </div>
            </div>

            <q-input
              v-model="formData.notes"
              label="Notes"
              type="textarea"
              outlined
              rows="2"
            />

            <q-toggle
              v-model="formData.is_active"
              label="Sous-traitant actif"
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
            @click="saveSubcontractor"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog de visualisation -->
    <q-dialog v-model="showViewDialog">
      <q-card style="min-width: 600px">
        <q-card-section class="row items-center">
          <div class="text-h6">Détails du sous-traitant</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section v-if="selectedSubcontractor">
          <div class="q-gutter-md">
            <div>
              <div class="text-caption text-grey-7">Nom</div>
              <div class="text-body1">{{ selectedSubcontractor.nom }}</div>
            </div>
            <div>
              <div class="text-caption text-grey-7">Sigle</div>
              <div class="text-body1">{{ selectedSubcontractor.sigle }}</div>
            </div>
            <div class="row q-col-gutter-md">
              <div class="col-6">
                <div class="text-caption text-grey-7">Téléphone</div>
                <div class="text-body1">{{ selectedSubcontractor.telephone }}</div>
              </div>
              <div class="col-6">
                <div class="text-caption text-grey-7">Email</div>
                <div class="text-body1">{{ selectedSubcontractor.email }}</div>
              </div>
            </div>
            <div v-if="selectedSubcontractor.numero_cc">
              <div class="text-caption text-grey-7">Numéro CC</div>
              <div class="text-body1">{{ selectedSubcontractor.numero_cc }}</div>
            </div>
            <div v-if="selectedSubcontractor.adresse">
              <div class="text-caption text-grey-7">Adresse</div>
              <div class="text-body1">{{ selectedSubcontractor.adresse }}</div>
            </div>
            <div v-if="selectedSubcontractor.domaines_competence">
              <div class="text-caption text-grey-7">Domaines de compétence</div>
              <div class="text-body1">{{ selectedSubcontractor.domaines_competence }}</div>
            </div>
            <div>
              <div class="text-caption text-grey-7">Statut</div>
              <q-badge
                :color="selectedSubcontractor.actif ? 'positive' : 'negative'"
                :label="selectedSubcontractor.actif ? 'Actif' : 'Inactif'"
              />
            </div>
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
          <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer ce sous-traitant ?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            label="Supprimer"
            color="negative"
            @click="deleteSubcontractor"
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
const selectedSubcontractor = ref(null)

const searchQuery = ref('')
const filterStatus = ref(null)

const formData = ref({
  code: '',
  nom: '',
  adresse: '',
  telephone: '',
  email: '',
  contact_principal_nom: '',
  contact_principal_telephone: '',
  specialites: '',
  numero_registre_commerce: '',
  is_active: true,
  date_debut_collaboration: '',
  notes: ''
})

const pagination = ref({
  sortBy: 'nom',
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

// État local pour les données (TOUJOURS initialisés)
const subcontractors = ref([])
const loading = ref(false)

// ============================================
// COMPUTED
// ============================================

const statusOptions = [
  { label: 'Tous', value: null },
  { label: 'Actif', value: true },
  { label: 'Inactif', value: false }
]

const columns = [
  {
    name: 'nom',
    label: 'Nom / Sigle',
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
    name: 'email',
    label: 'Email',
    field: 'email',
    align: 'left'
  },
  {
    name: 'domaines_competence',
    label: 'Domaines',
    field: 'domaines_competence',
    align: 'left'
  },
  {
    name: 'actif',
    label: 'Statut',
    field: 'actif',
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

async function loadSubcontractors(params = {}) {
  loading.value = true
  try {
    const result = await deploymentStore.subcontractors.list(params)

    // Mettre à jour le ref local
    subcontractors.value = Array.isArray(result) ? result : []

    // Mettre à jour la pagination
    if (deploymentStore.subcontractors?.pagination?.value?.rowsNumber !== undefined) {
      pagination.value.rowsNumber = deploymentStore.subcontractors.pagination.value.rowsNumber
    }
  } catch (error) {
    console.error('Erreur chargement sous-traitants:', error)
    subcontractors.value = [] // Toujours un tableau vide en cas d'erreur
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
    params.actif = filterStatus.value
  }

  await loadSubcontractors(params)
  pagination.value = props.pagination
}

function onSearch() {
  loadSubcontractors({
    search: searchQuery.value,
    actif: filterStatus.value
  })
}

function onFilter() {
  loadSubcontractors({
    search: searchQuery.value,
    actif: filterStatus.value
  })
}

function openCreateDialog() {
  resetForm()
  showFormDialog.value = true
}

function viewSubcontractor(subcontractor) {
  selectedSubcontractor.value = subcontractor
  showViewDialog.value = true
}

function editSubcontractor(subcontractor) {
  isEditing.value = true
  selectedSubcontractor.value = subcontractor
  formData.value = { ...subcontractor }
  showFormDialog.value = true
}

function resetForm() {
  isEditing.value = false
  selectedSubcontractor.value = null
  formData.value = {
    code: '',
    nom: '',
    adresse: '',
    telephone: '',
    email: '',
    contact_principal_nom: '',
    contact_principal_telephone: '',
    specialites: '',
    numero_registre_commerce: '',
    is_active: true,
    date_debut_collaboration: '',
    notes: ''
  }
}

async function saveSubcontractor() {
  try {
    if (isEditing.value) {
      await deploymentStore.subcontractors.update(selectedSubcontractor.value.id, formData.value)
    } else {
      await deploymentStore.subcontractors.create(formData.value)
    }

    showFormDialog.value = false
    resetForm()
    await loadSubcontractors()
  } catch (error) {
    console.error('Erreur sauvegarde sous-traitant:', error)
  }
}

function confirmDelete(subcontractor) {
  selectedSubcontractor.value = subcontractor
  showDeleteDialog.value = true
}

async function deleteSubcontractor() {
  try {
    await deploymentStore.subcontractors.remove(selectedSubcontractor.value.id)
    showDeleteDialog.value = false
    selectedSubcontractor.value = null
    await loadSubcontractors()
  } catch (error) {
    console.error('Erreur suppression sous-traitant:', error)
  }
}

// ============================================
// LIFECYCLE
// ============================================

onMounted(() => {
  loadSubcontractors()
})
</script>
