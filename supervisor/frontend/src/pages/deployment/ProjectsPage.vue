<template>
  <q-page class="q-pa-md">
    <!-- En-tête de page -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h4 text-weight-bold text-primary">Projets / Chantiers</div>
        <div class="text-subtitle2 text-grey-7">Gestion des projets de déploiement</div>
      </div>
      <div class="row q-gutter-sm">
        <q-btn
          color="accent"
          icon="warning"
          label="Projets en retard"
          @click="loadDelayedProjects"
          outline
        />
        <q-btn
          color="primary"
          icon="add"
          label="Nouveau Projet"
          @click="openCreateDialog"
          unelevated
        />
      </div>
    </div>

    <!-- Statistiques -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-md-3">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-primary">{{ stats.total }}</div>
            <div class="text-caption text-grey-7">Total Projets</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-positive">{{ stats.enCours }}</div>
            <div class="text-caption text-grey-7">En Cours</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-warning">{{ stats.planifies }}</div>
            <div class="text-caption text-grey-7">Planifiés</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card flat bordered>
          <q-card-section class="text-center">
            <div class="text-h4 text-info">{{ stats.termines }}</div>
            <div class="text-caption text-grey-7">Terminés</div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Filtres et recherche -->
    <q-card class="q-mb-md">
      <q-card-section>
        <div class="row q-col-gutter-md items-center">
          <div class="col-12 col-md-3">
            <q-input
              v-model="searchQuery"
              outlined
              dense
              placeholder="Rechercher..."
              clearable
              @update:model-value="onSearch"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
          <div class="col-12 col-md-2">
            <q-select
              v-model="filterOperator"
              outlined
              dense
              :options="operators"
              option-value="id"
              option-label="nom"
              emit-value
              map-options
              label="Opérateur"
              clearable
              @update:model-value="onFilter"
            >
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    {{ operators.length === 0 ? 'Aucun opérateur chargé' : 'Aucune option' }}
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
            <!-- DEBUG: Afficher le nombre d'opérateurs -->
            <div class="text-caption text-grey-7 q-mt-xs">
              Opérateurs chargés: {{ operators.length }}
            </div>
          </div>
          <div class="col-12 col-md-2">
            <q-select
              v-model="filterType"
              outlined
              dense
              :options="typeOptions"
              emit-value
              map-options
              label="Type"
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
            <q-btn-group outline class="full-width">
              <q-btn
                :outline="viewMode !== 'grid'"
                :unelevated="viewMode === 'grid'"
                icon="grid_view"
                @click="viewMode = 'grid'"
                class="col"
              >
                <q-tooltip>Vue grille</q-tooltip>
              </q-btn>
              <q-btn
                :outline="viewMode !== 'table'"
                :unelevated="viewMode === 'table'"
                icon="table_rows"
                @click="viewMode = 'table'"
                class="col"
              >
                <q-tooltip>Vue tableau</q-tooltip>
              </q-btn>
              <q-btn
                color="secondary"
                icon="refresh"
                @click="loadProjects"
                class="col"
              >
                <q-tooltip>Actualiser</q-tooltip>
              </q-btn>
            </q-btn-group>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Loading indicator -->
    <div v-if="loading" class="row justify-center q-py-xl">
      <q-spinner color="primary" size="50px" />
      <div class="col-12 text-center q-mt-md text-grey-7">Chargement...</div>
    </div>

    <!-- Vue Grille (Cartes) -->
    <div v-else-if="!loading && viewMode === 'grid'" class="row q-col-gutter-md">
      <div
        v-for="project in projects"
        :key="project.id"
        class="col-12 col-md-6 col-lg-4"
      >
        <q-card bordered class="project-card cursor-pointer" @click="viewProjectDetail(project.id)">
          <q-card-section>
            <div class="row items-center q-mb-sm">
              <div class="text-h6 text-primary">{{ project.code }}</div>
              <q-space />
              <q-badge :color="getStatusColor(project.statut)">
                {{ getStatusLabel(project.statut) }}
              </q-badge>
            </div>
            <div class="text-subtitle2 text-weight-medium q-mb-xs">{{ project.nom }}</div>
            <div class="text-caption text-grey-7">{{ project.zone_deploiement }}</div>
          </q-card-section>

          <q-separator />

          <q-card-section>
            <div class="row q-col-gutter-xs text-caption">
              <div class="col-6">
                <q-icon name="business" size="xs" class="q-mr-xs" />
                {{ project.operator_nom || '-' }}
              </div>
              <div class="col-6">
                <q-icon name="category" size="xs" class="q-mr-xs" />
                {{ getTypeLabel(project.type_projet) }}
              </div>
              <div class="col-6">
                <q-icon name="event" size="xs" class="q-mr-xs" />
                {{ formatDate(project.date_debut_prevue) }}
              </div>
              <div class="col-6">
                <q-icon name="person" size="xs" class="q-mr-xs" />
                {{ project.superviseur_aiv_nom || '-' }}
              </div>
            </div>
          </q-card-section>

          <q-card-section v-if="project.progression_percentage !== undefined">
            <q-linear-progress
              :value="project.progression_percentage / 100"
              :color="project.progression_percentage < 50 ? 'warning' : 'positive'"
              size="8px"
              rounded
            />
            <div class="text-caption text-center q-mt-xs">
              Progression: {{ project.progression_percentage }}%
            </div>
          </q-card-section>

          <q-separator />

          <q-card-actions>
            <q-btn
              flat
              dense
              icon="visibility"
              label="Voir"
              color="primary"
              @click.stop="viewProjectDetail(project.id)"
            />
            <q-space />
            <q-btn
              flat
              dense
              icon="edit"
              color="primary"
              @click.stop="editProject(project)"
            />
            <q-btn
              flat
              dense
              icon="delete"
              color="negative"
              @click.stop="confirmDelete(project)"
            />
          </q-card-actions>
        </q-card>
      </div>

      <!-- Message si aucun projet -->
      <div v-if="!loading && projects.length === 0" class="col-12 text-center q-py-xl">
        <q-icon name="folder_open" size="64px" color="grey-5" />
        <div class="text-h6 text-grey-6 q-mt-md">Aucun projet trouvé</div>
      </div>
    </div>

    <!-- Vue Tableau -->
    <q-card v-else-if="!loading && viewMode === 'table'">
      <q-card-section>
        <q-table
          v-if="projects && columns"
          :rows="projects"
          :columns="columns"
          :loading="loading"
          row-key="id"
          flat
          :pagination="pagination"
          @request="onTableRequest"
          binary-state-sort
          @row-click="(evt, row) => viewProjectDetail(row.id)"
          class="cursor-pointer"
        >
          <!-- Slot pour le code -->
          <template v-slot:body-cell-code="props">
            <q-td :props="props">
              <div class="text-weight-medium text-primary">{{ props.row.code }}</div>
            </q-td>
          </template>

          <!-- Slot pour le statut -->
          <template v-slot:body-cell-statut="props">
            <q-td :props="props">
              <q-badge :color="getStatusColor(props.row.statut)">
                {{ getStatusLabel(props.row.statut) }}
              </q-badge>
            </q-td>
          </template>

          <!-- Slot pour le type -->
          <template v-slot:body-cell-type_projet="props">
            <q-td :props="props">
              {{ getTypeLabel(props.row.type_projet) }}
            </q-td>
          </template>

          <!-- Slot pour la progression -->
          <template v-slot:body-cell-progression="props">
            <q-td :props="props">
              <div v-if="props.row.progression_percentage !== undefined">
                <q-linear-progress
                  :value="props.row.progression_percentage / 100"
                  :color="props.row.progression_percentage < 50 ? 'warning' : 'positive'"
                  size="8px"
                  rounded
                />
                <div class="text-caption text-center">{{ props.row.progression_percentage }}%</div>
              </div>
            </q-td>
          </template>

          <!-- Slot pour les actions -->
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn
                flat
                dense
                round
                color="primary"
                icon="edit"
                @click.stop="editProject(props.row)"
              >
                <q-tooltip>Modifier</q-tooltip>
              </q-btn>
              <q-btn
                flat
                dense
                round
                color="negative"
                icon="delete"
                @click.stop="confirmDelete(props.row)"
              >
                <q-tooltip>Supprimer</q-tooltip>
              </q-btn>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Dialog de formulaire -->
    <q-dialog v-model="showFormDialog" persistent maximized>
      <q-card>
        <q-card-section class="row items-center bg-primary text-white">
          <div class="text-h6">{{ isEditing ? 'Modifier' : 'Créer' }} un projet</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section class="scroll" style="max-height: calc(100vh - 150px)">
          <q-form @submit="saveProject" class="q-gutter-md">
            <div class="row q-col-gutter-md">
              <!-- Colonne gauche -->
              <div class="col-12 col-md-6">
                <div class="text-h6 q-mb-md">Informations générales</div>

                <q-input
                  v-model="formData.code"
                  label="Code du projet *"
                  outlined
                  :rules="[val => !!val || 'Le code est requis']"
                />

                <q-input
                  v-model="formData.nom"
                  label="Nom du projet *"
                  outlined
                  :rules="[val => !!val || 'Le nom est requis']"
                />

                <q-select
                  v-model="formData.operator"
                  outlined
                  :options="operators"
                  option-value="id"
                  option-label="nom"
                  emit-value
                  map-options
                  label="Opérateur *"
                  :rules="[val => !!val || 'L\'opérateur est requis']"
                />

                <q-select
                  v-model="formData.type_projet"
                  outlined
                  :options="typeOptions"
                  emit-value
                  map-options
                  label="Type de projet *"
                  :rules="[val => !!val || 'Le type est requis']"
                />

                <q-input
                  v-model="formData.zone_deploiement"
                  label="Zone de déploiement *"
                  outlined
                  :rules="[val => !!val || 'La zone est requise']"
                />

                <q-input
                  v-model="formData.budget"
                  label="Budget (FCFA)"
                  type="number"
                  outlined
                  prefix="F"
                />

                <q-input
                  v-model="formData.description"
                  label="Description"
                  type="textarea"
                  outlined
                  rows="3"
                />
              </div>

              <!-- Colonne droite -->
              <div class="col-12 col-md-6">
                <div class="text-h6 q-mb-md">Planning et responsables</div>

                <q-select
                  v-model="formData.superviseur_aiv"
                  outlined
                  :options="supervisors"
                  option-value="id"
                  option-label="full_name"
                  emit-value
                  map-options
                  label="Superviseur AIV *"
                  :rules="[val => !!val || 'Le superviseur est requis']"
                />

                <q-select
                  v-model="formData.coordonnateur"
                  outlined
                  :options="coordinators"
                  option-value="id"
                  option-label="full_name"
                  emit-value
                  map-options
                  label="Coordonnateur"
                  clearable
                />

                <div class="row q-col-gutter-md">
                  <div class="col-6">
                    <q-input
                      v-model="formData.date_debut_prevue"
                      label="Date début prévue *"
                      type="date"
                      outlined
                      :rules="[val => !!val || 'La date est requise']"
                    />
                  </div>
                  <div class="col-6">
                    <q-input
                      v-model="formData.date_fin_prevue"
                      label="Date fin prévue *"
                      type="date"
                      outlined
                      :rules="[val => !!val || 'La date est requise']"
                    />
                  </div>
                </div>

                <div class="row q-col-gutter-md">
                  <div class="col-6">
                    <q-input
                      v-model="formData.date_debut_reelle"
                      label="Date début réelle"
                      type="date"
                      outlined
                    />
                  </div>
                  <div class="col-6">
                    <q-input
                      v-model="formData.date_fin_reelle"
                      label="Date fin réelle"
                      type="date"
                      outlined
                    />
                  </div>
                </div>

                <q-select
                  v-model="formData.statut"
                  outlined
                  :options="statusOptions"
                  emit-value
                  map-options
                  label="Statut *"
                  :rules="[val => !!val || 'Le statut est requis']"
                />
              </div>
            </div>
          </q-form>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right" class="q-pa-md">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            :label="isEditing ? 'Modifier' : 'Créer'"
            color="primary"
            @click="saveProject"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog de confirmation de suppression -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="warning" color="negative" text-color="white" />
          <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer ce projet ?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            label="Supprimer"
            color="negative"
            @click="deleteProject"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDeploymentStore } from 'src/stores/deployment'

// ============================================
// ROUTER & STORE
// ============================================

const router = useRouter()
const deploymentStore = useDeploymentStore()

// ============================================
// STATE
// ============================================

const viewMode = ref('grid') // 'grid' or 'table'
const showFormDialog = ref(false)
const showDeleteDialog = ref(false)
const isEditing = ref(false)
const selectedProject = ref(null)

const searchQuery = ref('')
const filterOperator = ref(null)
const filterType = ref(null)
const filterStatus = ref(null)

// État local pour les données (TOUJOURS initialisés à des tableaux vides)
const projects = ref([])
const operators = ref([])
const supervisors = ref([])
const coordinators = ref([])
const loading = ref(false)

const formData = ref({
  code: '',
  nom: '',
  operator: null,
  type_projet: '',
  zone_deploiement: '',
  coordonnateur: null,
  superviseur_aiv: null,
  date_debut_prevue: '',
  date_fin_prevue: '',
  date_debut_reelle: '',
  date_fin_reelle: '',
  statut: 'planifie',
  budget: null,
  description: ''
})

const pagination = ref({
  sortBy: 'code',
  descending: false,
  page: 1,
  rowsPerPage: 20,
  rowsNumber: 0
})

// ============================================
// COMPUTED
// ============================================

const stats = computed(() => {
  const total = projects.value.length
  const enCours = projects.value.filter(p => p.statut === 'en_cours').length
  const planifies = projects.value.filter(p => p.statut === 'planifie').length
  const termines = projects.value.filter(p => p.statut === 'termine').length

  return { total, enCours, planifies, termines }
})

const typeOptions = [
  { label: 'Déploiement', value: 'deploiement' },
  { label: 'Backbone', value: 'backbone' },
  { label: 'Transport', value: 'transport' },
  { label: 'Réseau de distribution', value: 'reseau_distribution' }
]

const statusOptions = [
  { label: 'Planifié', value: 'planifie' },
  { label: 'En cours', value: 'en_cours' },
  { label: 'Suspendu', value: 'suspendu' },
  { label: 'Terminé', value: 'termine' },
  { label: 'Annulé', value: 'annule' }
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
    name: 'operator',
    label: 'Opérateur',
    field: 'operator_nom',
    align: 'left'
  },
  {
    name: 'type_projet',
    label: 'Type',
    field: 'type_projet',
    align: 'center'
  },
  {
    name: 'zone',
    label: 'Zone',
    field: 'zone_deploiement',
    align: 'left'
  },
  {
    name: 'date_debut',
    label: 'Début',
    field: 'date_debut_prevue',
    align: 'center',
    format: val => formatDate(val)
  },
  {
    name: 'progression',
    label: 'Progression',
    field: 'progression_percentage',
    align: 'center'
  },
  {
    name: 'statut',
    label: 'Statut',
    field: 'statut',
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

function formatDate(date) {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('fr-FR')
}

function getTypeLabel(value) {
  const option = typeOptions.find(opt => opt.value === value)
  return option ? option.label : value
}

function getStatusLabel(value) {
  const option = statusOptions.find(opt => opt.value === value)
  return option ? option.label : value
}

function getStatusColor(value) {
  const colors = {
    planifie: 'warning',
    en_cours: 'positive',
    suspendu: 'orange',
    termine: 'info',
    annule: 'negative'
  }
  return colors[value] || 'grey'
}

async function loadProjects(params = {}) {
  loading.value = true
  try {
    console.log('Loading projects with params:', params)
    const result = await deploymentStore.projects.list(params)
    console.log('Projects API result:', result)

    // Mettre à jour le ref local avec les données du store
    projects.value = Array.isArray(result) ? result : []
    console.log('Projects assigned to local ref:', projects.value)

    // Mettre à jour la pagination
    if (deploymentStore.projects?.pagination?.value?.rowsNumber !== undefined) {
      pagination.value.rowsNumber = deploymentStore.projects.pagination.value.rowsNumber
    }
  } catch (error) {
    console.error('Erreur chargement projets:', error)
    projects.value = [] // Toujours un tableau vide en cas d'erreur
  } finally {
    loading.value = false
  }
}

async function loadDelayedProjects() {
  try {
    await deploymentStore.fetchDelayedProjects()
  } catch (error) {
    console.error('Erreur chargement projets en retard:', error)
  }
}

async function loadOperators() {
  try {
    console.log('Loading operators...')
    const result = await deploymentStore.operators.list()
    console.log('Operators API result:', result)

    // Mettre à jour le ref local avec les données retournées
    operators.value = Array.isArray(result) ? result : []
    console.log('Operators assigned to local ref:', operators.value)
  } catch (error) {
    console.error('Erreur chargement opérateurs:', error)
    console.error('Error details:', error.response?.data)
    operators.value = [] // Toujours un tableau vide en cas d'erreur
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

  if (filterOperator.value) {
    params.operator = filterOperator.value
  }

  if (filterType.value) {
    params.type_projet = filterType.value
  }

  if (filterStatus.value) {
    params.statut = filterStatus.value
  }

  await loadProjects(params)
  pagination.value = props.pagination
}

function onSearch() {
  loadProjects({
    search: searchQuery.value,
    operator: filterOperator.value,
    type_projet: filterType.value,
    statut: filterStatus.value
  })
}

function onFilter() {
  onSearch()
}

function viewProjectDetail(projectId) {
  router.push({ name: 'project-detail', params: { id: projectId } })
}

function openCreateDialog() {
  resetForm()
  showFormDialog.value = true
}

function editProject(project) {
  isEditing.value = true
  selectedProject.value = project
  formData.value = { ...project }
  showFormDialog.value = true
}

function resetForm() {
  isEditing.value = false
  selectedProject.value = null
  formData.value = {
    code: '',
    nom: '',
    operator: null,
    type_projet: '',
    zone_deploiement: '',
    coordonnateur: null,
    superviseur_aiv: null,
    date_debut_prevue: '',
    date_fin_prevue: '',
    date_debut_reelle: '',
    date_fin_reelle: '',
    statut: 'planifie',
    budget: null,
    description: ''
  }
}

async function saveProject() {
  try {
    if (isEditing.value) {
      await deploymentStore.projects.update(selectedProject.value.id, formData.value)
    } else {
      await deploymentStore.projects.create(formData.value)
    }

    showFormDialog.value = false
    resetForm()
    await loadProjects()
  } catch (error) {
    console.error('Erreur sauvegarde projet:', error)
  }
}

function confirmDelete(project) {
  selectedProject.value = project
  showDeleteDialog.value = true
}

async function deleteProject() {
  try {
    await deploymentStore.projects.remove(selectedProject.value.id)
    showDeleteDialog.value = false
    selectedProject.value = null
    await loadProjects()
  } catch (error) {
    console.error('Erreur suppression projet:', error)
  }
}

// ============================================
// LIFECYCLE
// ============================================

onMounted(async () => {
  console.log('ProjectsPage mounted')
  console.log('deploymentStore:', deploymentStore)
  console.log('deploymentStore.operators:', deploymentStore.operators)
  console.log('deploymentStore.projects:', deploymentStore.projects)

  try {
    await loadOperators()
    console.log('Operators loaded:', operators.value)

    await loadProjects()
    console.log('Projects loaded:', projects.value)
  } catch (error) {
    console.error('Error in onMounted:', error)
  }

  // TODO: Charger les superviseurs et coordonnateurs depuis le store users
})
</script>

<style lang="scss" scoped>
.project-card {
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}
</style>
