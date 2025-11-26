<template>
  <q-page class="q-pa-md">
    <!-- En-tête de page -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h4 text-weight-bold text-primary">Opérateurs Télécoms</div>
        <div class="text-subtitle2 text-grey-7">Gestion des opérateurs (Orange, Moov, etc.)</div>
      </div>
      <q-btn
        color="primary"
        icon="add"
        label="Nouvel Opérateur"
        @click="showFormDialog = true"
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
              placeholder="Rechercher un opérateur..."
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
              @click="loadOperators"
              outline
              class="full-width"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- Tableau des opérateurs -->
    <q-card>
      <q-card-section>
        <q-table
          :rows="operators"
          :columns="columns"
          :loading="loading"
          row-key="id"
          flat
          :pagination="pagination"
          @request="onTableRequest"
          binary-state-sort
        >
          <!-- Slot personnalisé pour le logo -->
          <template v-slot:body-cell-logo="props">
            <q-td :props="props">
              <q-avatar v-if="props.row.logo" size="40px">
                <img :src="props.row.logo" :alt="props.row.nom">
              </q-avatar>
              <q-avatar v-else size="40px" color="grey-4" text-color="grey-7" icon="business" />
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

          <!-- Slot personnalisé pour les couleurs -->
          <template v-slot:body-cell-couleur_primaire="props">
            <q-td :props="props">
              <div class="row items-center q-gutter-xs">
                <div
                  v-if="props.row.couleur_primaire"
                  class="color-preview"
                  :style="{ backgroundColor: props.row.couleur_primaire }"
                />
                <span>{{ props.row.couleur_primaire || '-' }}</span>
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
                color="info"
                icon="list_alt"
                @click="openBoqItemsDialog(props.row)"
              >
                <q-tooltip>Gérer les articles BOQ</q-tooltip>
              </q-btn>
              <q-btn
                flat
                dense
                round
                color="primary"
                icon="edit"
                @click="editOperator(props.row)"
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

    <!-- Dialog de formulaire opérateur -->
    <q-dialog v-model="showFormDialog" persistent>
      <q-card style="min-width: 600px">
        <q-card-section class="row items-center">
          <div class="text-h6">{{ isEditing ? 'Modifier' : 'Créer' }} un opérateur</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 60vh" class="scroll">
          <q-form @submit="saveOperator" class="q-gutter-md">
            <q-input
              v-model="formData.nom"
              label="Nom de l'opérateur *"
              outlined
              :rules="[val => !!val || 'Le nom est requis']"
            />

            <q-input
              v-model="formData.code"
              label="Code (ex: ORG, MOV) *"
              outlined
              maxlength="10"
              :rules="[val => !!val || 'Le code est requis']"
            />

            <div class="row q-col-gutter-md">
              <div class="col-6">
                <q-input
                  v-model="formData.couleur_primaire"
                  label="Couleur primaire"
                  outlined
                >
                  <template v-slot:append>
                    <q-icon name="colorize" class="cursor-pointer">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-color v-model="formData.couleur_primaire" />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
              <div class="col-6">
                <q-input
                  v-model="formData.couleur_secondaire"
                  label="Couleur secondaire"
                  outlined
                >
                  <template v-slot:append>
                    <q-icon name="colorize" class="cursor-pointer">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-color v-model="formData.couleur_secondaire" />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
            </div>

            <q-input
              v-model="formData.email_contact"
              label="Email de contact"
              type="email"
              outlined
            />

            <q-input
              v-model="formData.telephone_contact"
              label="Téléphone de contact"
              outlined
            />

            <q-toggle
              v-model="formData.actif"
              label="Opérateur actif"
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
            @click="saveOperator"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog de confirmation de suppression opérateur -->
    <q-dialog v-model="showDeleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="warning" color="negative" text-color="white" />
          <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer cet opérateur ?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            label="Supprimer"
            color="negative"
            @click="deleteOperator"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- ============================================ -->
    <!-- Dialog de gestion des BOQ Items -->
    <!-- ============================================ -->
    <q-dialog v-model="showBoqItemsDialog" maximized>
      <q-card>
        <q-card-section class="row items-center bg-primary text-white">
          <q-icon name="list_alt" size="md" class="q-mr-sm" />
          <div class="text-h6">Articles BOQ - {{ selectedOperatorForBoq?.nom }}</div>
          <q-space />
          <q-btn icon="close" flat round dense color="white" v-close-popup />
        </q-card-section>

        <q-card-section>
          <!-- Barre d'outils BOQ -->
          <div class="row q-col-gutter-md q-mb-md">
            <div class="col-12 col-md-4">
              <q-input
                v-model="boqSearchQuery"
                outlined
                dense
                placeholder="Rechercher un article..."
                clearable
                @update:model-value="loadBoqItems"
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-3">
              <q-select
                v-model="boqFilterCategory"
                outlined
                dense
                :options="categoryOptions"
                emit-value
                map-options
                label="Catégorie"
                clearable
                @update:model-value="loadBoqItems"
              />
            </div>
            <div class="col-12 col-md-2">
              <q-btn
                color="secondary"
                icon="refresh"
                label="Actualiser"
                @click="loadBoqItems"
                outline
                class="full-width"
              />
            </div>
            <div class="col-12 col-md-3">
              <q-btn
                color="primary"
                icon="add"
                label="Nouvel Article"
                @click="openBoqItemForm"
                unelevated
                class="full-width"
              />
            </div>
          </div>

          <!-- Tableau des BOQ Items -->
          <q-table
            :rows="boqItems"
            :columns="boqColumns"
            :loading="boqLoading"
            row-key="id"
            flat
            bordered
            :pagination="boqPagination"
            @request="onBoqTableRequest"
            binary-state-sort
          >
            <!-- Catégorie -->
            <template v-slot:body-cell-category="props">
              <q-td :props="props">
                <q-badge color="primary" outline>
                  {{ getCategoryName(props.row.category) }}
                </q-badge>
              </q-td>
            </template>

            <!-- Prix unitaire -->
            <template v-slot:body-cell-prix_unitaire="props">
              <q-td :props="props">
                <span class="text-weight-medium">
                  {{ formatPrice(props.row.prix_unitaire) }} FCFA
                </span>
              </q-td>
            </template>

            <!-- Statut -->
            <template v-slot:body-cell-is_active="props">
              <q-td :props="props">
                <q-badge
                  :color="props.row.is_active ? 'positive' : 'negative'"
                  :label="props.row.is_active ? 'Actif' : 'Inactif'"
                />
              </q-td>
            </template>

            <!-- Actions -->
            <template v-slot:body-cell-actions="props">
              <q-td :props="props">
                <q-btn
                  flat
                  dense
                  round
                  color="primary"
                  icon="visibility"
                  @click="viewBoqItem(props.row)"
                >
                  <q-tooltip>Voir</q-tooltip>
                </q-btn>
                <q-btn
                  flat
                  dense
                  round
                  color="primary"
                  icon="edit"
                  @click="editBoqItem(props.row)"
                >
                  <q-tooltip>Modifier</q-tooltip>
                </q-btn>
                <q-btn
                  flat
                  dense
                  round
                  color="negative"
                  icon="delete"
                  @click="confirmDeleteBoqItem(props.row)"
                >
                  <q-tooltip>Supprimer</q-tooltip>
                </q-btn>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog formulaire BOQ Item -->
    <q-dialog v-model="showBoqItemFormDialog" persistent>
      <q-card style="min-width: 600px">
        <q-card-section class="row items-center">
          <div class="text-h6">{{ isEditingBoqItem ? 'Modifier' : 'Créer' }} un article BOQ</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section style="max-height: 70vh" class="scroll">
          <q-form class="q-gutter-md">
            <q-select
              v-model="boqItemFormData.category"
              outlined
              :options="categories"
              option-value="id"
              option-label="nom"
              emit-value
              map-options
              label="Catégorie *"
              :rules="[val => !!val || 'La catégorie est requise']"
            />

            <div class="row q-col-gutter-md">
              <div class="col-4">
                <q-input
                  v-model="boqItemFormData.code"
                  label="Code *"
                  outlined
                  maxlength="50"
                  :rules="[val => !!val || 'Le code est requis']"
                />
              </div>
              <div class="col-8">
                <q-input
                  v-model="boqItemFormData.libelle"
                  label="Libellé *"
                  outlined
                  :rules="[val => !!val || 'Le libellé est requis']"
                />
              </div>
            </div>

            <div class="row q-col-gutter-md">
              <div class="col-6">
                <q-select
                  v-model="boqItemFormData.unite"
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
                  v-model.number="boqItemFormData.prix_unitaire"
                  label="Prix unitaire (FCFA) *"
                  type="number"
                  outlined
                  min="0"
                  step="0.01"
                  :rules="[val => val >= 0 || 'Le prix doit être positif']"
                />
              </div>
            </div>

            <q-input
              v-model="boqItemFormData.description"
              label="Description"
              type="textarea"
              outlined
              rows="3"
            />

            <q-toggle
              v-model="boqItemFormData.is_active"
              label="Article actif"
              color="positive"
            />
          </q-form>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            :label="isEditingBoqItem ? 'Modifier' : 'Créer'"
            color="primary"
            @click="saveBoqItem"
            :loading="boqLoading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog visualisation BOQ Item -->
    <q-dialog v-model="showBoqItemViewDialog">
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center">
          <div class="text-h6">Détails de l'article BOQ</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section v-if="selectedBoqItem" class="q-gutter-md">
          <div class="row q-col-gutter-md">
            <div class="col-4">
              <div class="text-caption text-grey-7">Code</div>
              <div class="text-body1 text-weight-medium">{{ selectedBoqItem.code }}</div>
            </div>
            <div class="col-8">
              <div class="text-caption text-grey-7">Catégorie</div>
              <div class="text-body1">{{ getCategoryName(selectedBoqItem.category) }}</div>
            </div>
          </div>
          <div>
            <div class="text-caption text-grey-7">Libellé</div>
            <div class="text-body1">{{ selectedBoqItem.libelle }}</div>
          </div>
          <div class="row q-col-gutter-md">
            <div class="col-6">
              <div class="text-caption text-grey-7">Unité</div>
              <div class="text-body1">{{ getUniteName(selectedBoqItem.unite) }}</div>
            </div>
            <div class="col-6">
              <div class="text-caption text-grey-7">Prix unitaire</div>
              <div class="text-body1 text-weight-bold text-primary">
                {{ formatPrice(selectedBoqItem.prix_unitaire) }} FCFA
              </div>
            </div>
          </div>
          <div v-if="selectedBoqItem.description">
            <div class="text-caption text-grey-7">Description</div>
            <div class="text-body1">{{ selectedBoqItem.description }}</div>
          </div>
          <div>
            <div class="text-caption text-grey-7">Statut</div>
            <q-badge
              :color="selectedBoqItem.is_active ? 'positive' : 'negative'"
              :label="selectedBoqItem.is_active ? 'Actif' : 'Inactif'"
            />
          </div>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat label="Fermer" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog confirmation suppression BOQ Item -->
    <q-dialog v-model="showBoqItemDeleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="warning" color="negative" text-color="white" />
          <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer cet article BOQ ?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Annuler" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            label="Supprimer"
            color="negative"
            @click="deleteBoqItem"
            :loading="boqLoading"
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
// STATE - Opérateurs
// ============================================

const showFormDialog = ref(false)
const showDeleteDialog = ref(false)
const isEditing = ref(false)
const selectedOperator = ref(null)

const searchQuery = ref('')
const filterStatus = ref(null)

const formData = ref({
  nom: '',
  code: '',
  couleur_primaire: '#FF5722',
  couleur_secondaire: '#FFC107',
  email_contact: '',
  telephone_contact: '',
  actif: true
})

const pagination = ref({
  sortBy: 'nom',
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

const operators = ref([])
const loading = ref(false)

// ============================================
// STATE - BOQ Items
// ============================================

const showBoqItemsDialog = ref(false)
const showBoqItemFormDialog = ref(false)
const showBoqItemViewDialog = ref(false)
const showBoqItemDeleteDialog = ref(false)
const isEditingBoqItem = ref(false)
const selectedOperatorForBoq = ref(null)
const selectedBoqItem = ref(null)

const boqSearchQuery = ref('')
const boqFilterCategory = ref(null)

const boqItems = ref([])
const categories = ref([])
const boqLoading = ref(false)

const boqItemFormData = ref({
  category: null,
  code: '',
  libelle: '',
  unite: '',
  prix_unitaire: 0,
  description: '',
  is_active: true
})

const boqPagination = ref({
  sortBy: 'code',
  descending: false,
  page: 1,
  rowsPerPage: 15,
  rowsNumber: 0
})

// ============================================
// OPTIONS
// ============================================

const statusOptions = [
  { label: 'Tous', value: null },
  { label: 'Actif', value: true },
  { label: 'Inactif', value: false }
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

const categoryOptions = ref([{ label: 'Toutes', value: null }])

const columns = [
  { name: 'logo', label: 'Logo', field: 'logo', align: 'left' },
  { name: 'nom', label: 'Nom', field: 'nom', align: 'left', sortable: true },
  { name: 'code', label: 'Code', field: 'code', align: 'left', sortable: true },
  { name: 'couleur_primaire', label: 'Couleur', field: 'couleur_primaire', align: 'left' },
  { name: 'email_contact', label: 'Email', field: 'email_contact', align: 'left' },
  { name: 'telephone_contact', label: 'Téléphone', field: 'telephone_contact', align: 'left' },
  { name: 'actif', label: 'Statut', field: 'actif', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const boqColumns = [
  { name: 'code', label: 'Code', field: 'code', align: 'left', sortable: true },
  { name: 'libelle', label: 'Libellé', field: 'libelle', align: 'left', sortable: true },
  { name: 'category', label: 'Catégorie', field: 'category', align: 'left' },
  { name: 'unite', label: 'Unité', field: 'unite', align: 'center' },
  { name: 'prix_unitaire', label: 'Prix unitaire', field: 'prix_unitaire', align: 'right', sortable: true },
  { name: 'is_active', label: 'Statut', field: 'is_active', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

// ============================================
// METHODS - Opérateurs
// ============================================

async function loadOperators(params = {}) {
  loading.value = true
  try {
    const result = await deploymentStore.operators.list(params)
    operators.value = Array.isArray(result) ? result : []
    if (deploymentStore.operators?.pagination?.value?.rowsNumber !== undefined) {
      pagination.value.rowsNumber = deploymentStore.operators.pagination.value.rowsNumber
    }
  } catch (error) {
    console.error('Erreur chargement opérateurs:', error)
    operators.value = []
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
  if (searchQuery.value) params.search = searchQuery.value
  if (filterStatus.value !== null) params.actif = filterStatus.value
  await loadOperators(params)
  pagination.value = props.pagination
}

function onSearch() {
  loadOperators({ search: searchQuery.value, actif: filterStatus.value })
}

function onFilter() {
  loadOperators({ search: searchQuery.value, actif: filterStatus.value })
}

function editOperator(operator) {
  isEditing.value = true
  selectedOperator.value = operator
  formData.value = { ...operator }
  showFormDialog.value = true
}

function resetForm() {
  isEditing.value = false
  selectedOperator.value = null
  formData.value = {
    nom: '',
    code: '',
    couleur_primaire: '#FF5722',
    couleur_secondaire: '#FFC107',
    email_contact: '',
    telephone_contact: '',
    actif: true
  }
}

async function saveOperator() {
  try {
    if (isEditing.value) {
      await deploymentStore.operators.update(selectedOperator.value.id, formData.value)
    } else {
      await deploymentStore.operators.create(formData.value)
    }
    showFormDialog.value = false
    resetForm()
    await loadOperators()
  } catch (error) {
    console.error('Erreur sauvegarde opérateur:', error)
  }
}

function confirmDelete(operator) {
  selectedOperator.value = operator
  showDeleteDialog.value = true
}

async function deleteOperator() {
  try {
    await deploymentStore.operators.remove(selectedOperator.value.id)
    showDeleteDialog.value = false
    selectedOperator.value = null
    await loadOperators()
  } catch (error) {
    console.error('Erreur suppression opérateur:', error)
  }
}

// ============================================
// METHODS - BOQ Items
// ============================================

async function loadCategories() {
  try {
    const result = await deploymentStore.boqCategories.list()
    categories.value = Array.isArray(result) ? result : []
    categoryOptions.value = [
      { label: 'Toutes', value: null },
      ...categories.value.map(c => ({ label: c.nom, value: c.id }))
    ]
  } catch (error) {
    console.error('Erreur chargement catégories:', error)
    categories.value = []
  }
}

async function loadBoqItems() {
  if (!selectedOperatorForBoq.value) return

  boqLoading.value = true
  try {
    const params = { operator: selectedOperatorForBoq.value.id }
    if (boqSearchQuery.value) params.search = boqSearchQuery.value
    if (boqFilterCategory.value) params.category = boqFilterCategory.value

    const result = await deploymentStore.boqItems.list(params)
    boqItems.value = Array.isArray(result) ? result : []
  } catch (error) {
    console.error('Erreur chargement articles BOQ:', error)
    boqItems.value = []
  } finally {
    boqLoading.value = false
  }
}

async function onBoqTableRequest(props) {
  const { page, rowsPerPage, sortBy, descending } = props.pagination
  const params = {
    operator: selectedOperatorForBoq.value.id,
    page,
    page_size: rowsPerPage,
    ordering: (descending ? '-' : '') + sortBy
  }
  if (boqSearchQuery.value) params.search = boqSearchQuery.value
  if (boqFilterCategory.value) params.category = boqFilterCategory.value

  boqLoading.value = true
  try {
    const result = await deploymentStore.boqItems.list(params)
    boqItems.value = Array.isArray(result) ? result : []
  } catch (error) {
    console.error('Erreur chargement articles BOQ:', error)
    boqItems.value = []
  } finally {
    boqLoading.value = false
  }
  boqPagination.value = props.pagination
}

function openBoqItemsDialog(operator) {
  selectedOperatorForBoq.value = operator
  boqSearchQuery.value = ''
  boqFilterCategory.value = null
  showBoqItemsDialog.value = true
  loadCategories()
  loadBoqItems()
}

function openBoqItemForm() {
  resetBoqItemForm()
  showBoqItemFormDialog.value = true
}

function viewBoqItem(item) {
  selectedBoqItem.value = item
  showBoqItemViewDialog.value = true
}

function editBoqItem(item) {
  isEditingBoqItem.value = true
  selectedBoqItem.value = item
  boqItemFormData.value = { ...item }
  showBoqItemFormDialog.value = true
}

function resetBoqItemForm() {
  isEditingBoqItem.value = false
  selectedBoqItem.value = null
  boqItemFormData.value = {
    category: null,
    code: '',
    libelle: '',
    unite: '',
    prix_unitaire: 0,
    description: '',
    is_active: true
  }
}

async function saveBoqItem() {
  boqLoading.value = true
  try {
    const data = {
      ...boqItemFormData.value,
      operator: selectedOperatorForBoq.value.id
    }

    if (isEditingBoqItem.value) {
      await deploymentStore.boqItems.update(selectedBoqItem.value.id, data)
    } else {
      await deploymentStore.boqItems.create(data)
    }

    showBoqItemFormDialog.value = false
    resetBoqItemForm()
    await loadBoqItems()
  } catch (error) {
    console.error('Erreur sauvegarde article BOQ:', error)
  } finally {
    boqLoading.value = false
  }
}

function confirmDeleteBoqItem(item) {
  selectedBoqItem.value = item
  showBoqItemDeleteDialog.value = true
}

async function deleteBoqItem() {
  boqLoading.value = true
  try {
    await deploymentStore.boqItems.remove(selectedBoqItem.value.id)
    showBoqItemDeleteDialog.value = false
    selectedBoqItem.value = null
    await loadBoqItems()
  } catch (error) {
    console.error('Erreur suppression article BOQ:', error)
  } finally {
    boqLoading.value = false
  }
}

// ============================================
// HELPERS
// ============================================

function getCategoryName(categoryId) {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.nom : '-'
}

function getUniteName(value) {
  const option = uniteOptions.find(o => o.value === value)
  return option ? option.label : value
}

function formatPrice(value) {
  if (!value) return '0'
  return new Intl.NumberFormat('fr-FR').format(value)
}

// ============================================
// LIFECYCLE
// ============================================

onMounted(() => {
  loadOperators()
})
</script>

<style lang="scss" scoped>
.color-preview {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
