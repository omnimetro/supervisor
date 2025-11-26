<template>
  <q-page class="q-pa-md">
    <!-- En-tête de page -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h4 text-weight-bold text-primary">Définitions de Tâches</div>
        <div class="text-subtitle2 text-grey-7">Tâches AIV avec KPI de productivité</div>
      </div>
      <q-btn
        color="primary"
        icon="add"
        label="Nouvelle Tâche"
        @click="openCreateDialog"
        unelevated
      />
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
              placeholder="Rechercher une tâche..."
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
              v-model="filterUnite"
              outlined
              dense
              :options="uniteFilterOptions"
              emit-value
              map-options
              label="Unité"
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
              @click="loadTaskDefinitions"
              outline
              class="full-width"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Tableau des tâches -->
    <q-card>
      <q-card-section>
        <q-table
          :rows="taskDefinitions"
          :columns="columns"
          :loading="loading"
          row-key="id"
          flat
          :pagination="pagination"
          @request="onTableRequest"
          binary-state-sort
        >
          <!-- Slot personnalisé pour le code -->
          <template v-slot:body-cell-code="props">
            <q-td :props="props">
              <div class="text-weight-medium text-primary">{{ props.row.code }}</div>
            </q-td>
          </template>

          <!-- Slot personnalisé pour KPI -->
          <template v-slot:body-cell-kpi="props">
            <q-td :props="props">
              <div class="text-weight-bold text-positive">
                {{ props.row.kpi }} {{ getUniteName(props.row.unite) }}/jour
              </div>
            </q-td>
          </template>

          <!-- Slot personnalisé pour le nombre d'articles BOQ -->
          <template v-slot:body-cell-boq_items_count="props">
            <q-td :props="props">
              <q-badge color="info" :label="props.row.boq_items_count || 0" />
            </q-td>
          </template>

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
                @click="viewTaskDefinition(props.row)"
              >
                <q-tooltip>Voir</q-tooltip>
              </q-btn>
              <q-btn
                flat
                dense
                round
                color="primary"
                icon="edit"
                @click="editTaskDefinition(props.row)"
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
      <q-card style="min-width: 650px">
        <q-card-section class="row items-center">
          <div class="text-h6">{{ isEditing ? 'Modifier' : 'Créer' }} une tâche</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 70vh" class="scroll">
          <q-form class="q-gutter-md">
            <div class="row q-col-gutter-md">
              <div class="col-4">
                <q-input
                  v-model="formData.code"
                  label="Code *"
                  outlined
                  maxlength="50"
                  hint="Ex: INST_PCO"
                  :rules="[val => !!val || 'Le code est requis']"
                />
              </div>
              <div class="col-8">
                <q-input
                  v-model="formData.libelle"
                  label="Libellé *"
                  outlined
                  hint="Ex: Installation de PCO"
                  :rules="[val => !!val || 'Le libellé est requis']"
                />
              </div>
            </div>

            <div class="row q-col-gutter-md">
              <div class="col-6">
                <q-select
                  v-model="formData.unite"
                  outlined
                  :options="uniteOptions"
                  emit-value
                  map-options
                  label="Unité *"
                  :rules="[val => !!val || 'L\'unité est requise']"
                />
              </div>
              <div class="col-6">
                <q-input
                  v-model.number="formData.kpi"
                  label="KPI (quantité/jour) *"
                  type="number"
                  outlined
                  min="0.01"
                  step="0.01"
                  suffix="/jour"
                  hint="Productivité attendue"
                  :rules="[val => val > 0 || 'Le KPI doit être positif']"
                />
              </div>
            </div>

            <q-select
              v-model="formData.boq_items"
              outlined
              :options="boqItems"
              option-value="id"
              option-label="libelle"
              emit-value
              map-options
              multiple
              use-chips
              label="Articles BOQ associés"
              hint="Sélectionnez 0 ou plusieurs articles BOQ"
            >
              <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps">
                  <q-item-section>
                    <q-item-label>{{ scope.opt.code }} - {{ scope.opt.libelle }}</q-item-label>
                    <q-item-label caption>{{ getOperatorName(scope.opt.operator) }}</q-item-label>
                  </q-item-section>
                </q-item>
              </template>
            </q-select>

            <q-input
              v-model="formData.description"
              label="Description"
              type="textarea"
              outlined
              rows="3"
            />

            <q-toggle
              v-model="formData.is_active"
              label="Tâche active"
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
            @click="saveTaskDefinition"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog de visualisation -->
    <q-dialog v-model="showViewDialog">
      <q-card style="min-width: 550px">
        <q-card-section class="row items-center">
          <div class="text-h6">Détails de la tâche</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section v-if="selectedTaskDefinition" class="q-gutter-md">
          <div>
            <div class="text-caption text-grey-7">Code</div>
            <div class="text-h6 text-primary">{{ selectedTaskDefinition.code }}</div>
          </div>
          <div>
            <div class="text-caption text-grey-7">Libellé</div>
            <div class="text-body1">{{ selectedTaskDefinition.libelle }}</div>
          </div>
          <div class="row q-col-gutter-md">
            <div class="col-6">
              <div class="text-caption text-grey-7">Unité</div>
              <div class="text-body1">{{ getUniteName(selectedTaskDefinition.unite) }}</div>
            </div>
            <div class="col-6">
              <div class="text-caption text-grey-7">KPI</div>
              <div class="text-body1 text-weight-bold text-positive">
                {{ selectedTaskDefinition.kpi }} {{ getUniteName(selectedTaskDefinition.unite) }}/jour
              </div>
            </div>
          </div>
          <div v-if="selectedTaskDefinition.description">
            <div class="text-caption text-grey-7">Description</div>
            <div class="text-body1">{{ selectedTaskDefinition.description }}</div>
          </div>
          <div>
            <div class="text-caption text-grey-7">Articles BOQ associés</div>
            <div class="text-body1">
              <q-badge color="info" :label="selectedTaskDefinition.boq_items_count || 0" />
              <span class="q-ml-sm">article(s)</span>
            </div>
          </div>
          <div>
            <div class="text-caption text-grey-7">Statut</div>
            <q-badge
              :color="selectedTaskDefinition.is_active ? 'positive' : 'negative'"
              :label="selectedTaskDefinition.is_active ? 'Active' : 'Inactive'"
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
          <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer cette tâche ?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            label="Supprimer"
            color="negative"
            @click="deleteTaskDefinition"
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
const selectedTaskDefinition = ref(null)

const searchQuery = ref('')
const filterUnite = ref(null)
const filterStatus = ref(null)

const formData = ref({
  code: '',
  libelle: '',
  unite: '',
  kpi: 1,
  description: '',
  boq_items: [],
  is_active: true
})

const pagination = ref({
  sortBy: 'code',
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

const taskDefinitions = ref([])
const boqItems = ref([])
const operators = ref([])
const loading = ref(false)

// ============================================
// OPTIONS
// ============================================

const statusOptions = [
  { label: 'Tous', value: null },
  { label: 'Active', value: true },
  { label: 'Inactive', value: false }
]

const uniteOptions = [
  { label: 'Mètre linéaire', value: 'ml' },
  { label: 'Unité', value: 'u' },
  { label: 'Mètre carré', value: 'm2' },
  { label: 'Mètre cube', value: 'm3' },
  { label: 'Kilogramme', value: 'kg' },
  { label: 'Litre', value: 'l' },
  { label: 'Jour', value: 'jour' },
  { label: 'Forfait', value: 'forfait' }
]

const uniteFilterOptions = [
  { label: 'Toutes', value: null },
  ...uniteOptions
]

const columns = [
  { name: 'code', label: 'Code', field: 'code', align: 'left', sortable: true },
  { name: 'libelle', label: 'Libellé', field: 'libelle', align: 'left', sortable: true },
  { name: 'unite', label: 'Unité', field: 'unite', align: 'center' },
  { name: 'kpi', label: 'KPI', field: 'kpi', align: 'center', sortable: true },
  { name: 'boq_items_count', label: 'Articles BOQ', field: 'boq_items_count', align: 'center' },
  { name: 'is_active', label: 'Statut', field: 'is_active', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

// ============================================
// METHODS
// ============================================

async function loadTaskDefinitions(params = {}) {
  loading.value = true
  try {
    const result = await deploymentStore.taskDefinitions.list(params)
    taskDefinitions.value = Array.isArray(result) ? result : []

    if (deploymentStore.taskDefinitions?.pagination?.value?.rowsNumber !== undefined) {
      pagination.value.rowsNumber = deploymentStore.taskDefinitions.pagination.value.rowsNumber
    }
  } catch (error) {
    console.error('Erreur chargement tâches:', error)
    taskDefinitions.value = []
  } finally {
    loading.value = false
  }
}

async function loadBoqItems() {
  try {
    const result = await deploymentStore.boqItems.list()
    boqItems.value = Array.isArray(result) ? result : []
  } catch (error) {
    console.error('Erreur chargement articles BOQ:', error)
    boqItems.value = []
  }
}

async function loadOperators() {
  try {
    const result = await deploymentStore.operators.list()
    operators.value = Array.isArray(result) ? result : []
  } catch (error) {
    console.error('Erreur chargement opérateurs:', error)
    operators.value = []
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

  if (filterUnite.value) {
    params.unite = filterUnite.value
  }

  if (filterStatus.value !== null) {
    params.is_active = filterStatus.value
  }

  await loadTaskDefinitions(params)
  pagination.value = props.pagination
}

function onSearch() {
  loadTaskDefinitions({
    search: searchQuery.value,
    unite: filterUnite.value,
    is_active: filterStatus.value
  })
}

function onFilter() {
  loadTaskDefinitions({
    search: searchQuery.value,
    unite: filterUnite.value,
    is_active: filterStatus.value
  })
}

function openCreateDialog() {
  resetForm()
  showFormDialog.value = true
}

function viewTaskDefinition(task) {
  selectedTaskDefinition.value = task
  showViewDialog.value = true
}

function editTaskDefinition(task) {
  isEditing.value = true
  selectedTaskDefinition.value = task
  formData.value = { ...task }
  showFormDialog.value = true
}

function resetForm() {
  isEditing.value = false
  selectedTaskDefinition.value = null
  formData.value = {
    code: '',
    libelle: '',
    unite: '',
    kpi: 1,
    description: '',
    boq_items: [],
    is_active: true
  }
}

async function saveTaskDefinition() {
  try {
    if (isEditing.value) {
      await deploymentStore.taskDefinitions.update(selectedTaskDefinition.value.id, formData.value)
    } else {
      await deploymentStore.taskDefinitions.create(formData.value)
    }

    showFormDialog.value = false
    resetForm()
    await loadTaskDefinitions()
  } catch (error) {
    console.error('Erreur sauvegarde tâche:', error)
  }
}

function confirmDelete(task) {
  selectedTaskDefinition.value = task
  showDeleteDialog.value = true
}

async function deleteTaskDefinition() {
  try {
    await deploymentStore.taskDefinitions.remove(selectedTaskDefinition.value.id)
    showDeleteDialog.value = false
    selectedTaskDefinition.value = null
    await loadTaskDefinitions()
  } catch (error) {
    console.error('Erreur suppression tâche:', error)
  }
}

// ============================================
// HELPERS
// ============================================

function getUniteName(value) {
  const option = uniteOptions.find(o => o.value === value)
  return option ? option.label : value
}

function getOperatorName(operatorId) {
  const operator = operators.value.find(op => op.id === operatorId)
  return operator ? operator.nom : '-'
}

// ============================================
// LIFECYCLE
// ============================================

onMounted(() => {
  loadTaskDefinitions()
  loadBoqItems()
  loadOperators()
})
</script>
