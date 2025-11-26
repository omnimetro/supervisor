<template>
  <q-page class="q-pa-md">
    <div v-if="loading" class="flex flex-center" style="min-height: 400px">
      <q-spinner-dots color="primary" size="50px" />
    </div>

    <div v-else-if="project">
      <!-- En-tête -->
      <div class="row items-center q-mb-md">
        <q-btn
          flat
          round
          icon="arrow_back"
          @click="goBack"
        />
        <div class="q-ml-md">
          <div class="text-h4 text-weight-bold text-primary">{{ project.code }}</div>
          <div class="text-subtitle2 text-grey-7">{{ project.nom }}</div>
        </div>
        <q-space />
        <q-badge :color="getStatusColor(project.statut)" class="q-px-md q-py-sm text-subtitle2">
          {{ getStatusLabel(project.statut) }}
        </q-badge>
      </div>

      <!-- Onglets -->
      <q-card>
        <q-tabs
          v-model="activeTab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="left"
        >
          <q-tab name="overview" label="Vue d'ensemble" icon="dashboard" />
          <q-tab name="planning" label="Planning des travaux" icon="list_alt" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="activeTab" animated>
          <!-- ============================================ -->
          <!-- ONGLET 1 : VUE D'ENSEMBLE -->
          <!-- ============================================ -->
          <q-tab-panel name="overview">
            <div class="row q-col-gutter-md">
              <!-- Informations principales -->
              <div class="col-12 col-md-8">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-h6 q-mb-md">Informations du projet</div>
                    <div class="row q-col-gutter-md">
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Opérateur</div>
                        <div class="text-body1">{{ project.operator_nom || '-' }}</div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Type</div>
                        <div class="text-body1">{{ getTypeLabel(project.type_projet) }}</div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Zone</div>
                        <div class="text-body1">{{ project.zone_deploiement }}</div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Budget</div>
                        <div class="text-body1 text-weight-bold text-primary">{{ formatCurrency(project.budget) }}</div>
                      </div>
                      <div class="col-12">
                        <div class="text-caption text-grey-7">Description</div>
                        <div class="text-body1">{{ project.description || '-' }}</div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>

                <!-- Planning -->
                <q-card flat bordered class="q-mt-md">
                  <q-card-section>
                    <div class="text-h6 q-mb-md">Calendrier</div>
                    <div class="row q-col-gutter-md">
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Date début prévue</div>
                        <div class="text-body1">{{ formatDate(project.date_debut_prevue) }}</div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Date fin prévue</div>
                        <div class="text-body1">{{ formatDate(project.date_fin_prevue) }}</div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Date début réelle</div>
                        <div class="text-body1">{{ formatDate(project.date_debut_reelle) || '-' }}</div>
                      </div>
                      <div class="col-6">
                        <div class="text-caption text-grey-7">Date fin réelle</div>
                        <div class="text-body1">{{ formatDate(project.date_fin_reelle) || '-' }}</div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>

              <!-- Progression -->
              <div class="col-12 col-md-4">
                <q-card flat bordered>
                  <q-card-section class="text-center">
                    <div class="text-h6 q-mb-md">Progression</div>
                    <q-circular-progress
                      :value="project.progression_percentage || 0"
                      size="150px"
                      :thickness="0.15"
                      color="primary"
                      track-color="grey-3"
                      show-value
                      class="q-my-md"
                    >
                      <div class="text-h4 text-weight-bold">{{ project.progression_percentage || 0 }}%</div>
                    </q-circular-progress>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>

          <!-- ============================================ -->
          <!-- ONGLET 2 : PLANNING DES TRAVAUX -->
          <!-- ============================================ -->
          <q-tab-panel name="planning">
            <div class="row items-center justify-between q-mb-md">
              <div class="text-h6">Travaux planifiés</div>
              <q-btn
                color="primary"
                icon="add"
                label="Ajouter un travail"
                @click="openPlanningDialog"
                unelevated
              />
            </div>

            <!-- Tableau des travaux planifiés -->
            <q-table
              :rows="plannings"
              :columns="planningColumns"
              :loading="planningLoading"
              row-key="id"
              flat
              bordered
            >
              <!-- Code BOQ -->
              <template v-slot:body-cell-boq_item_code="props">
                <q-td :props="props">
                  <div class="text-weight-medium text-primary">{{ props.row.boq_item_code }}</div>
                </q-td>
              </template>

              <!-- Quantité -->
              <template v-slot:body-cell-quantite_prevue="props">
                <q-td :props="props">
                  <div class="text-weight-medium">
                    {{ props.row.quantite_prevue }} {{ props.row.boq_item_unite }}
                  </div>
                </q-td>
              </template>

              <!-- Montant total -->
              <template v-slot:body-cell-montant_total="props">
                <q-td :props="props">
                  <div class="text-weight-bold text-positive">
                    {{ formatCurrency(props.row.montant_total) }}
                  </div>
                </q-td>
              </template>

              <!-- Progression -->
              <template v-slot:body-cell-progression_percentage="props">
                <q-td :props="props">
                  <q-linear-progress
                    :value="props.row.progression_percentage / 100"
                    color="primary"
                    size="20px"
                    class="q-my-xs"
                  >
                    <div class="absolute-full flex flex-center">
                      <div class="text-white text-weight-bold">{{ props.row.progression_percentage }}%</div>
                    </div>
                  </q-linear-progress>
                </q-td>
              </template>

              <!-- Actions -->
              <template v-slot:body-cell-actions="props">
                <q-td :props="props">
                  <q-btn
                    flat
                    dense
                    round
                    color="info"
                    icon="assignment"
                    @click="openTaskPlanningsDialog(props.row)"
                  >
                    <q-tooltip>Gérer les tâches</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    dense
                    round
                    color="primary"
                    icon="visibility"
                    @click="viewPlanning(props.row)"
                  >
                    <q-tooltip>Voir</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    dense
                    round
                    color="primary"
                    icon="edit"
                    @click="editPlanning(props.row)"
                  >
                    <q-tooltip>Modifier</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    dense
                    round
                    color="negative"
                    icon="delete"
                    @click="confirmDeletePlanning(props.row)"
                  >
                    <q-tooltip>Supprimer</q-tooltip>
                  </q-btn>
                </q-td>
              </template>
            </q-table>

            <!-- Résumé financier -->
            <q-card flat bordered class="q-mt-md">
              <q-card-section>
                <div class="row q-col-gutter-md">
                  <div class="col-4">
                    <div class="text-caption text-grey-7">Montant total planifié</div>
                    <div class="text-h5 text-weight-bold text-primary">{{ formatCurrency(totalMontantPlanifie) }}</div>
                  </div>
                  <div class="col-4">
                    <div class="text-caption text-grey-7">Nombre de travaux</div>
                    <div class="text-h5 text-weight-bold">{{ plannings.length }}</div>
                  </div>
                  <div class="col-4">
                    <div class="text-caption text-grey-7">Délai total estimé</div>
                    <div class="text-h5 text-weight-bold">{{ totalDelai }} jours</div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>

      <!-- Dialog formulaire Planning -->
      <q-dialog v-model="showPlanningDialog" persistent>
        <q-card style="min-width: 600px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ isEditingPlanning ? 'Modifier' : 'Ajouter' }} un travail au planning</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-separator />

          <q-card-section>
            <q-form class="q-gutter-md">
              <q-select
                v-model="planningFormData.boq_item"
                outlined
                :options="filteredBoqItems"
                option-value="id"
                option-label="libelle"
                emit-value
                map-options
                label="Travail BOQ *"
                :rules="[val => !!val || 'Le travail est requis']"
                :disable="isEditingPlanning"
              >
                <template v-slot:option="scope">
                  <q-item v-bind="scope.itemProps">
                    <q-item-section>
                      <q-item-label>{{ scope.opt.code }} - {{ scope.opt.libelle }}</q-item-label>
                      <q-item-label caption>
                        {{ scope.opt.unite }} - {{ formatCurrency(scope.opt.prix_unitaire) }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>

              <div class="row q-col-gutter-md">
                <div class="col-4">
                  <q-input
                    v-model.number="planningFormData.valeur_unite"
                    outlined
                    type="number"
                    min="1"
                    label="Valeur de l'unité *"
                    hint="Valeur numérique de l'unité"
                    :rules="[val => val >= 1 || 'La valeur doit être >= 1']"
                  />
                </div>
                <div class="col-4">
                  <q-input
                    v-model.number="planningFormData.quantite_prevue"
                    label="Quantité prévue *"
                    type="number"
                    outlined
                    min="0.01"
                    step="0.01"
                    :rules="[val => val > 0 || 'La quantité doit être positive']"
                  />
                </div>
                <div class="col-4">
                  <q-input
                    v-model.number="planningFormData.delai_jours"
                    label="Délai (jours) *"
                    type="number"
                    outlined
                    min="1"
                    :rules="[val => val >= 1 || 'Le délai doit être au moins 1 jour']"
                  />
                </div>
              </div>

              <q-input
                v-model.number="planningFormData.ordre"
                label="Ordre d'exécution"
                type="number"
                outlined
                min="0"
                hint="Ordre dans lequel ce travail sera exécuté"
              />

              <!-- Montant estimé -->
              <div v-if="planningFormData.boq_item && planningFormData.quantite_prevue > 0">
                <q-separator class="q-my-md" />
                <div class="row items-center">
                  <div class="col">
                    <div class="text-caption text-grey-7">Montant total estimé</div>
                  </div>
                  <div class="col-auto">
                    <div class="text-h6 text-weight-bold text-positive">
                      {{ formatCurrency(calculateMontantEstime()) }}
                    </div>
                  </div>
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-separator />

          <q-card-actions align="right">
            <q-btn flat label="Annuler" color="grey-7" v-close-popup />
            <q-btn
              unelevated
              :label="isEditingPlanning ? 'Modifier' : 'Ajouter'"
              color="primary"
              @click="savePlanning"
              :loading="planningLoading"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Dialog visualisation Planning -->
      <q-dialog v-model="showPlanningViewDialog">
        <q-card style="min-width: 500px">
          <q-card-section class="row items-center">
            <div class="text-h6">Détails du travail</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-separator />

          <q-card-section v-if="selectedPlanning" class="q-gutter-md">
            <div>
              <div class="text-caption text-grey-7">Travail BOQ</div>
              <div class="text-h6">{{ selectedPlanning.boq_item_code }} - {{ selectedPlanning.boq_item_libelle }}</div>
            </div>
            <div class="row q-col-gutter-md">
              <div class="col-6">
                <div class="text-caption text-grey-7">Quantité prévue</div>
                <div class="text-body1 text-weight-medium">
                  {{ selectedPlanning.quantite_prevue }} {{ selectedPlanning.boq_item_unite }}
                </div>
              </div>
              <div class="col-6">
                <div class="text-caption text-grey-7">Quantité réalisée</div>
                <div class="text-body1 text-weight-medium">
                  {{ selectedPlanning.quantite_realisee || 0 }} {{ selectedPlanning.boq_item_unite }}
                </div>
              </div>
            </div>
            <div class="row q-col-gutter-md">
              <div class="col-6">
                <div class="text-caption text-grey-7">Délai</div>
                <div class="text-body1">{{ selectedPlanning.delai_jours }} jours</div>
              </div>
              <div class="col-6">
                <div class="text-caption text-grey-7">Ordre</div>
                <div class="text-body1">{{ selectedPlanning.ordre }}</div>
              </div>
            </div>
            <div>
              <div class="text-caption text-grey-7">Montant total</div>
              <div class="text-h6 text-weight-bold text-positive">
                {{ formatCurrency(selectedPlanning.montant_total) }}
              </div>
            </div>
            <div>
              <div class="text-caption text-grey-7">Progression</div>
              <q-linear-progress
                :value="selectedPlanning.progression_percentage / 100"
                color="primary"
                size="25px"
                class="q-my-sm"
              >
                <div class="absolute-full flex flex-center">
                  <div class="text-white text-weight-bold">{{ selectedPlanning.progression_percentage }}%</div>
                </div>
              </q-linear-progress>
            </div>
          </q-card-section>

          <q-separator />

          <q-card-actions align="right">
            <q-btn flat label="Fermer" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Dialog confirmation suppression Planning -->
      <q-dialog v-model="showPlanningDeleteDialog" persistent>
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="warning" color="negative" text-color="white" />
            <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer ce travail du planning ?</span>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Annuler" color="grey-7" v-close-popup />
            <q-btn
              unelevated
              label="Supprimer"
              color="negative"
              @click="deletePlanning"
              :loading="planningLoading"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- ============================================ -->
      <!-- DIALOG : GESTION DES TASK PLANNINGS -->
      <!-- ============================================ -->
      <q-dialog v-model="showTaskPlanningsDialog" maximized>
        <q-card>
          <q-card-section class="row items-center q-pb-none bg-primary text-white">
            <div class="text-h6">
              Tâches planifiées - {{ selectedProjectPlanning?.boq_item_libelle }}
            </div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <!-- Toolbar -->
            <div class="row q-col-gutter-md q-mb-md">
              <div class="col-12 col-md-4">
                <q-input
                  v-model="taskPlanningSearchQuery"
                  outlined
                  dense
                  placeholder="Rechercher une tâche..."
                  clearable
                >
                  <template v-slot:prepend>
                    <q-icon name="search" />
                  </template>
                </q-input>
              </div>
              <div class="col-12 col-md-3">
                <q-select
                  v-model="taskPlanningStatusFilter"
                  outlined
                  dense
                  :options="taskStatusOptions"
                  option-value="value"
                  option-label="label"
                  emit-value
                  map-options
                  clearable
                  label="Statut"
                />
              </div>
              <div class="col-12 col-md-5 text-right">
                <q-btn
                  unelevated
                  color="primary"
                  icon="add"
                  label="Ajouter une tâche"
                  @click="openTaskPlanningForm()"
                />
              </div>
            </div>

            <!-- Tableau -->
            <q-table
              :rows="filteredTaskPlannings"
              :columns="taskPlanningColumns"
              row-key="id"
              :loading="loadingTaskPlannings"
              :pagination="{ rowsPerPage: 20 }"
              no-data-label="Aucune tâche planifiée"
            >
              <!-- Statut avec badge -->
              <template v-slot:body-cell-statut="props">
                <q-td :props="props">
                  <q-badge :color="getTaskStatusColor(props.row.statut)">
                    {{ getTaskStatusLabel(props.row.statut) }}
                  </q-badge>
                </q-td>
              </template>

              <!-- Progression -->
              <template v-slot:body-cell-progression_percentage="props">
                <q-td :props="props">
                  <q-linear-progress
                    :value="props.row.progression_percentage / 100"
                    :color="props.row.progression_percentage === 100 ? 'positive' : 'primary'"
                    size="20px"
                    class="q-my-xs"
                  >
                    <div class="absolute-full flex flex-center">
                      <div class="text-white text-weight-bold">{{ props.row.progression_percentage }}%</div>
                    </div>
                  </q-linear-progress>
                </q-td>
              </template>

              <!-- En retard -->
              <template v-slot:body-cell-is_delayed="props">
                <q-td :props="props">
                  <q-icon
                    v-if="props.row.is_delayed && props.row.statut !== 'termine'"
                    name="warning"
                    color="negative"
                    size="sm"
                  >
                    <q-tooltip>En retard</q-tooltip>
                  </q-icon>
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
                    @click="viewTaskPlanning(props.row)"
                  >
                    <q-tooltip>Voir</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    dense
                    round
                    color="primary"
                    icon="edit"
                    @click="editTaskPlanning(props.row)"
                  >
                    <q-tooltip>Modifier</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    dense
                    round
                    color="negative"
                    icon="delete"
                    @click="confirmDeleteTaskPlanning(props.row)"
                  >
                    <q-tooltip>Supprimer</q-tooltip>
                  </q-btn>
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- ============================================ -->
      <!-- DIALOG : FORMULAIRE TASK PLANNING -->
      <!-- ============================================ -->
      <q-dialog v-model="showTaskPlanningFormDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">
              {{ isEditingTaskPlanning ? 'Modifier' : 'Ajouter' }} une tâche planifiée
            </div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="saveTaskPlanning">
              <div class="row q-col-gutter-md">
                <!-- TaskDefinition -->
                <div class="col-12">
                  <q-select
                    v-model="taskPlanningFormData.task_definition"
                    outlined
                    :options="taskDefinitions"
                    option-value="id"
                    option-label="libelle"
                    emit-value
                    map-options
                    label="Tâche *"
                    :rules="[val => !!val || 'La tâche est obligatoire']"
                    :disable="isEditingTaskPlanning"
                  >
                    <template v-slot:option="scope">
                      <q-item v-bind="scope.itemProps">
                        <q-item-section>
                          <q-item-label>{{ scope.opt.libelle }}</q-item-label>
                          <q-item-label caption>{{ scope.opt.code }} - {{ scope.opt.unite }} - KPI: {{ scope.opt.kpi }}</q-item-label>
                        </q-item-section>
                      </q-item>
                    </template>
                  </q-select>
                </div>

                <!-- Valeur unité -->
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="taskPlanningFormData.valeur_unite"
                    outlined
                    type="number"
                    min="1"
                    label="Valeur de l'unité *"
                    hint="Valeur numérique de l'unité"
                    :rules="[val => val >= 1 || 'La valeur doit être >= 1']"
                  />
                </div>

                <!-- Quantité prévue -->
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="taskPlanningFormData.quantite_prevue"
                    outlined
                    type="number"
                    step="0.01"
                    min="0.01"
                    label="Quantité prévue *"
                    :rules="[val => val > 0 || 'La quantité doit être supérieure à 0']"
                  />
                </div>

                <!-- Délai jours -->
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="taskPlanningFormData.delai_jours"
                    outlined
                    type="number"
                    min="1"
                    label="Délai (jours) *"
                    :rules="[val => val >= 1 || 'Le délai doit être d\'au moins 1 jour']"
                  />
                </div>

                <!-- Date début prévue -->
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="taskPlanningFormData.date_debut_prevue"
                    outlined
                    type="date"
                    label="Date début prévue *"
                    :rules="[val => !!val || 'La date de début est obligatoire']"
                  />
                </div>

                <!-- Date fin prévue -->
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="taskPlanningFormData.date_fin_prevue"
                    outlined
                    type="date"
                    label="Date fin prévue *"
                    :rules="[val => !!val || 'La date de fin est obligatoire']"
                  />
                </div>

                <!-- Date début réelle -->
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="taskPlanningFormData.date_debut_reelle"
                    outlined
                    type="date"
                    label="Date début réelle"
                    clearable
                  />
                </div>

                <!-- Date fin réelle -->
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="taskPlanningFormData.date_fin_reelle"
                    outlined
                    type="date"
                    label="Date fin réelle"
                    clearable
                  />
                </div>

                <!-- Statut -->
                <div class="col-12 col-md-6">
                  <q-select
                    v-model="taskPlanningFormData.statut"
                    outlined
                    :options="taskStatusOptions"
                    option-value="value"
                    option-label="label"
                    emit-value
                    map-options
                    label="Statut *"
                    :rules="[val => !!val || 'Le statut est obligatoire']"
                  />
                </div>

                <!-- Ordre -->
                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="taskPlanningFormData.ordre"
                    outlined
                    type="number"
                    min="0"
                    label="Ordre d'exécution"
                  />
                </div>
              </div>

              <div class="row q-col-gutter-md q-mt-md">
                <div class="col-12 text-right">
                  <q-btn flat label="Annuler" color="grey-7" v-close-popup class="q-mr-sm" />
                  <q-btn
                    unelevated
                    type="submit"
                    :label="isEditingTaskPlanning ? 'Modifier' : 'Ajouter'"
                    color="primary"
                    :loading="taskPlanningLoading"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- ============================================ -->
      <!-- DIALOG : VISUALISATION TASK PLANNING -->
      <!-- ============================================ -->
      <q-dialog v-model="showTaskPlanningViewDialog">
        <q-card style="min-width: 500px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Détails de la tâche planifiée</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="selectedTaskPlanning">
            <div class="row q-col-gutter-md">
              <div class="col-12">
                <div class="text-caption text-grey-7">Tâche</div>
                <div class="text-body1 text-weight-bold">{{ selectedTaskPlanning.task_libelle }}</div>
                <div class="text-caption">{{ selectedTaskPlanning.task_code }}</div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Quantité prévue</div>
                <div class="text-body1">{{ selectedTaskPlanning.quantite_prevue }} {{ selectedTaskPlanning.task_unite }}</div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Quantité réalisée</div>
                <div class="text-body1 text-weight-bold" :class="selectedTaskPlanning.quantite_realisee >= selectedTaskPlanning.quantite_prevue ? 'text-positive' : 'text-primary'">
                  {{ selectedTaskPlanning.quantite_realisee }} {{ selectedTaskPlanning.task_unite }}
                </div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Délai prévu</div>
                <div class="text-body1">{{ selectedTaskPlanning.delai_jours }} jours</div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Ordre</div>
                <div class="text-body1">{{ selectedTaskPlanning.ordre }}</div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Date début prévue</div>
                <div class="text-body1">{{ formatDate(selectedTaskPlanning.date_debut_prevue) }}</div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Date fin prévue</div>
                <div class="text-body1">{{ formatDate(selectedTaskPlanning.date_fin_prevue) }}</div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Date début réelle</div>
                <div class="text-body1">{{ formatDate(selectedTaskPlanning.date_debut_reelle) || '-' }}</div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Date fin réelle</div>
                <div class="text-body1">{{ formatDate(selectedTaskPlanning.date_fin_reelle) || '-' }}</div>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">Statut</div>
                <q-badge :color="getTaskStatusColor(selectedTaskPlanning.statut)">
                  {{ getTaskStatusLabel(selectedTaskPlanning.statut) }}
                </q-badge>
              </div>

              <div class="col-6">
                <div class="text-caption text-grey-7">En retard</div>
                <div class="text-body1">
                  <q-icon
                    v-if="selectedTaskPlanning.is_delayed && selectedTaskPlanning.statut !== 'termine'"
                    name="warning"
                    color="negative"
                    size="sm"
                  />
                  <span v-else class="text-grey-7">-</span>
                </div>
              </div>

              <div class="col-12">
                <div class="text-caption text-grey-7">Progression</div>
                <q-linear-progress
                  :value="selectedTaskPlanning.progression_percentage / 100"
                  :color="selectedTaskPlanning.progression_percentage === 100 ? 'positive' : 'primary'"
                  size="25px"
                  class="q-my-xs"
                >
                  <div class="absolute-full flex flex-center">
                    <div class="text-white text-weight-bold">{{ selectedTaskPlanning.progression_percentage }}%</div>
                  </div>
                </q-linear-progress>
              </div>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Fermer" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- ============================================ -->
      <!-- DIALOG : CONFIRMATION SUPPRESSION TASK PLANNING -->
      <!-- ============================================ -->
      <q-dialog v-model="showTaskPlanningDeleteDialog" persistent>
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="warning" color="negative" text-color="white" />
            <span class="q-ml-sm">Êtes-vous sûr de vouloir supprimer cette tâche planifiée ?</span>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Annuler" color="grey-7" v-close-popup />
            <q-btn
              unelevated
              label="Supprimer"
              color="negative"
              @click="deleteTaskPlanning"
              :loading="taskPlanningLoading"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDeploymentStore } from 'src/stores/deployment'

// ============================================
// ROUTER & STORE
// ============================================

const route = useRoute()
const router = useRouter()
const deploymentStore = useDeploymentStore()

// ============================================
// STATE
// ============================================

const activeTab = ref('overview')
const project = ref(null)
const loading = ref(false)

// Planning
const plannings = ref([])
const boqItems = ref([])
const planningLoading = ref(false)
const showPlanningDialog = ref(false)
const showPlanningViewDialog = ref(false)
const showPlanningDeleteDialog = ref(false)
const isEditingPlanning = ref(false)
const selectedPlanning = ref(null)

const planningFormData = ref({
  boq_item: null,
  valeur_unite: 1,
  quantite_prevue: 1,
  delai_jours: 1,
  ordre: 0
})

// Task Planning
const taskPlannings = ref([])
const taskDefinitions = ref([])
const loadingTaskPlannings = ref(false)
const taskPlanningLoading = ref(false)
const showTaskPlanningsDialog = ref(false)
const showTaskPlanningFormDialog = ref(false)
const showTaskPlanningViewDialog = ref(false)
const showTaskPlanningDeleteDialog = ref(false)
const isEditingTaskPlanning = ref(false)
const selectedProjectPlanning = ref(null)
const selectedTaskPlanning = ref(null)
const taskPlanningSearchQuery = ref('')
const taskPlanningStatusFilter = ref(null)

const taskPlanningFormData = ref({
  project_planning: null,
  task_definition: null,
  valeur_unite: 1,
  quantite_prevue: 1,
  delai_jours: 1,
  date_debut_prevue: '',
  date_fin_prevue: '',
  date_debut_reelle: null,
  date_fin_reelle: null,
  statut: 'non_commence',
  ordre: 0
})

// ============================================
// COLUMNS
// ============================================

const planningColumns = [
  { name: 'ordre', label: 'Ordre', field: 'ordre', align: 'center', sortable: true },
  { name: 'boq_item_code', label: 'Code', field: 'boq_item_code', align: 'left', sortable: true },
  { name: 'boq_item_libelle', label: 'Travail', field: 'boq_item_libelle', align: 'left', sortable: true },
  { name: 'quantite_prevue', label: 'Quantité', field: 'quantite_prevue', align: 'right' },
  { name: 'delai_jours', label: 'Délai (j)', field: 'delai_jours', align: 'center', sortable: true },
  { name: 'montant_total', label: 'Montant', field: 'montant_total', align: 'right', sortable: true },
  { name: 'progression_percentage', label: 'Progression', field: 'progression_percentage', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const taskPlanningColumns = [
  { name: 'ordre', label: 'Ordre', field: 'ordre', align: 'center', sortable: true },
  { name: 'task_code', label: 'Code', field: 'task_code', align: 'left', sortable: true },
  { name: 'task_libelle', label: 'Tâche', field: 'task_libelle', align: 'left', sortable: true },
  { name: 'quantite_prevue', label: 'Qté prévue', field: 'quantite_prevue', align: 'right' },
  { name: 'quantite_realisee', label: 'Qté réalisée', field: 'quantite_realisee', align: 'right' },
  { name: 'delai_jours', label: 'Délai (j)', field: 'delai_jours', align: 'center', sortable: true },
  { name: 'date_debut_prevue', label: 'Début prévu', field: 'date_debut_prevue', align: 'center', sortable: true },
  { name: 'date_fin_prevue', label: 'Fin prévue', field: 'date_fin_prevue', align: 'center', sortable: true },
  { name: 'statut', label: 'Statut', field: 'statut', align: 'center' },
  { name: 'progression_percentage', label: 'Progression', field: 'progression_percentage', align: 'center' },
  { name: 'is_delayed', label: 'Retard', field: 'is_delayed', align: 'center' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

// ============================================
// OPTIONS
// ============================================

const taskStatusOptions = [
  { value: 'non_commence', label: 'Non commencé' },
  { value: 'en_cours', label: 'En cours' },
  { value: 'termine', label: 'Terminé' },
  { value: 'suspendu', label: 'Suspendu' }
]

// ============================================
// COMPUTED
// ============================================

const filteredBoqItems = computed(() => {
  if (!project.value || !boqItems.value.length) return []

  // Filtrer par opérateur du projet
  return boqItems.value.filter(item => item.operator === project.value.operator)
})

const totalMontantPlanifie = computed(() => {
  return plannings.value.reduce((sum, p) => sum + (p.montant_total || 0), 0)
})

const totalDelai = computed(() => {
  return plannings.value.reduce((sum, p) => sum + (p.delai_jours || 0), 0)
})

const filteredTaskPlannings = computed(() => {
  let filtered = [...taskPlannings.value]

  // Filtrer par recherche
  if (taskPlanningSearchQuery.value) {
    const query = taskPlanningSearchQuery.value.toLowerCase()
    filtered = filtered.filter(tp =>
      tp.task_code?.toLowerCase().includes(query) ||
      tp.task_libelle?.toLowerCase().includes(query)
    )
  }

  // Filtrer par statut
  if (taskPlanningStatusFilter.value) {
    filtered = filtered.filter(tp => tp.statut === taskPlanningStatusFilter.value)
  }

  return filtered
})

// ============================================
// METHODS - Project
// ============================================

async function loadProject() {
  loading.value = true
  try {
    const projectId = route.params.id
    const result = await deploymentStore.projects.get(projectId)
    project.value = result
  } catch (error) {
    console.error('Erreur chargement projet:', error)
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.push('/deployment/projects')
}

function getStatusLabel(status) {
  const labels = {
    'planifie': 'Planifié',
    'en_cours': 'En cours',
    'en_livraison': 'En livraison',
    'termine': 'Terminé',
    'annule': 'Annulé'
  }
  return labels[status] || status
}

function getStatusColor(status) {
  const colors = {
    'planifie': 'info',
    'en_cours': 'primary',
    'en_livraison': 'warning',
    'termine': 'positive',
    'annule': 'negative'
  }
  return colors[status] || 'grey'
}

function getTypeLabel(type) {
  const labels = {
    'backbone': 'Backbone',
    'transport': 'Réseau de transport',
    'distribution': 'Réseau de distribution'
  }
  return labels[type] || type
}

// ============================================
// METHODS - Planning
// ============================================

async function loadPlannings() {
  planningLoading.value = true
  try {
    const projectId = route.params.id
    const result = await deploymentStore.projectPlannings.list({ project: projectId })
    plannings.value = Array.isArray(result) ? result : []
  } catch (error) {
    console.error('Erreur chargement plannings:', error)
    plannings.value = []
  } finally {
    planningLoading.value = false
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

function openPlanningDialog() {
  resetPlanningForm()
  showPlanningDialog.value = true
}

function viewPlanning(planning) {
  selectedPlanning.value = planning
  showPlanningViewDialog.value = true
}

function editPlanning(planning) {
  isEditingPlanning.value = true
  selectedPlanning.value = planning
  planningFormData.value = {
    boq_item: planning.boq_item,
    valeur_unite: planning.valeur_unite || 1,
    quantite_prevue: planning.quantite_prevue,
    delai_jours: planning.delai_jours,
    ordre: planning.ordre
  }
  showPlanningDialog.value = true
}

function resetPlanningForm() {
  isEditingPlanning.value = false
  selectedPlanning.value = null
  planningFormData.value = {
    boq_item: null,
    valeur_unite: 1,
    quantite_prevue: 1,
    delai_jours: 1,
    ordre: 0
  }
}

function calculateMontantEstime() {
  if (!planningFormData.value.boq_item || !planningFormData.value.quantite_prevue) return 0

  const boqItem = boqItems.value.find(item => item.id === planningFormData.value.boq_item)
  if (!boqItem) return 0

  return boqItem.prix_unitaire * planningFormData.value.quantite_prevue
}

async function savePlanning() {
  planningLoading.value = true
  try {
    const data = {
      ...planningFormData.value,
      project: project.value.id
    }

    if (isEditingPlanning.value) {
      await deploymentStore.projectPlannings.update(selectedPlanning.value.id, data)
    } else {
      await deploymentStore.projectPlannings.create(data)
    }

    showPlanningDialog.value = false
    resetPlanningForm()
    await loadPlannings()
  } catch (error) {
    console.error('Erreur sauvegarde planning:', error)
  } finally {
    planningLoading.value = false
  }
}

function confirmDeletePlanning(planning) {
  selectedPlanning.value = planning
  showPlanningDeleteDialog.value = true
}

async function deletePlanning() {
  planningLoading.value = true
  try {
    await deploymentStore.projectPlannings.remove(selectedPlanning.value.id)
    showPlanningDeleteDialog.value = false
    selectedPlanning.value = null
    await loadPlannings()
  } catch (error) {
    console.error('Erreur suppression planning:', error)
  } finally {
    planningLoading.value = false
  }
}

// ============================================
// METHODS - Task Planning
// ============================================

async function loadTaskPlannings() {
  if (!selectedProjectPlanning.value) return

  loadingTaskPlannings.value = true
  try {
    const result = await deploymentStore.taskPlannings.list({
      project_planning: selectedProjectPlanning.value.id
    })
    taskPlannings.value = result
  } catch (error) {
    console.error('Erreur chargement task plannings:', error)
  } finally {
    loadingTaskPlannings.value = false
  }
}

async function loadTaskDefinitions() {
  try {
    const result = await deploymentStore.taskDefinitions.list()
    taskDefinitions.value = result
  } catch (error) {
    console.error('Erreur chargement task definitions:', error)
  }
}

async function openTaskPlanningsDialog(planning) {
  selectedProjectPlanning.value = planning
  showTaskPlanningsDialog.value = true
  await loadTaskPlannings()
  await loadTaskDefinitions()
}

function openTaskPlanningForm() {
  isEditingTaskPlanning.value = false
  taskPlanningFormData.value = {
    project_planning: selectedProjectPlanning.value.id,
    task_definition: null,
    valeur_unite: 1,
    quantite_prevue: 1,
    delai_jours: 1,
    date_debut_prevue: '',
    date_fin_prevue: '',
    date_debut_reelle: null,
    date_fin_reelle: null,
    statut: 'non_commence',
    ordre: 0
  }
  showTaskPlanningFormDialog.value = true
}

function viewTaskPlanning(taskPlanning) {
  selectedTaskPlanning.value = taskPlanning
  showTaskPlanningViewDialog.value = true
}

function editTaskPlanning(taskPlanning) {
  isEditingTaskPlanning.value = true
  selectedTaskPlanning.value = taskPlanning
  taskPlanningFormData.value = {
    project_planning: taskPlanning.project_planning,
    task_definition: taskPlanning.task_definition,
    valeur_unite: taskPlanning.valeur_unite || 1,
    quantite_prevue: taskPlanning.quantite_prevue,
    delai_jours: taskPlanning.delai_jours,
    date_debut_prevue: taskPlanning.date_debut_prevue,
    date_fin_prevue: taskPlanning.date_fin_prevue,
    date_debut_reelle: taskPlanning.date_debut_reelle || null,
    date_fin_reelle: taskPlanning.date_fin_reelle || null,
    statut: taskPlanning.statut,
    ordre: taskPlanning.ordre
  }
  showTaskPlanningFormDialog.value = true
}

function confirmDeleteTaskPlanning(taskPlanning) {
  selectedTaskPlanning.value = taskPlanning
  showTaskPlanningDeleteDialog.value = true
}

async function saveTaskPlanning() {
  taskPlanningLoading.value = true
  try {
    // Nettoyer les dates vides
    const data = { ...taskPlanningFormData.value }
    if (!data.date_debut_reelle) delete data.date_debut_reelle
    if (!data.date_fin_reelle) delete data.date_fin_reelle

    if (isEditingTaskPlanning.value) {
      await deploymentStore.taskPlannings.update(selectedTaskPlanning.value.id, data)
    } else {
      await deploymentStore.taskPlannings.create(data)
    }

    showTaskPlanningFormDialog.value = false
    await loadTaskPlannings()
  } catch (error) {
    console.error('Erreur sauvegarde task planning:', error)
  } finally {
    taskPlanningLoading.value = false
  }
}

async function deleteTaskPlanning() {
  taskPlanningLoading.value = true
  try {
    await deploymentStore.taskPlannings.remove(selectedTaskPlanning.value.id)
    showTaskPlanningDeleteDialog.value = false
    selectedTaskPlanning.value = null
    await loadTaskPlannings()
  } catch (error) {
    console.error('Erreur suppression task planning:', error)
  } finally {
    taskPlanningLoading.value = false
  }
}

function getTaskStatusLabel(status) {
  const option = taskStatusOptions.find(opt => opt.value === status)
  return option ? option.label : status
}

function getTaskStatusColor(status) {
  const colors = {
    'non_commence': 'grey',
    'en_cours': 'primary',
    'termine': 'positive',
    'suspendu': 'warning'
  }
  return colors[status] || 'grey'
}

// ============================================
// HELPERS
// ============================================

function formatDate(dateString) {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR')
}

function formatCurrency(value) {
  if (!value) return '0 FCFA'
  return new Intl.NumberFormat('fr-FR').format(value) + ' FCFA'
}

// ============================================
// LIFECYCLE
// ============================================

onMounted(() => {
  loadProject()
  loadPlannings()
  loadBoqItems()
})
</script>
