<template>
  <q-page class="dashboard-page q-pa-md">
    <!-- Header Section -->
    <div class="page-header q-mb-lg">
      <div class="row items-center justify-between">
        <div class="col-auto">
          <h4 class="page-title q-my-none">Tableau de Bord</h4>
          <p class="page-subtitle q-my-none text-grey-6">
            Bienvenue, {{ authStore.userFullName || authStore.user?.username }}
          </p>
        </div>
        <div class="col-auto">
          <q-btn
            flat
            dense
            round
            icon="refresh"
            color="primary"
            @click="refreshDashboard"
            :loading="loading"
          >
            <q-tooltip>Actualiser</q-tooltip>
          </q-btn>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row q-col-gutter-md q-mb-lg">
      <!-- Card Chantiers -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="stats-card">
          <q-card-section>
            <div class="row items-center">
              <div class="col">
                <div class="stats-value text-primary">{{ stats.projets }}</div>
                <div class="stats-label">Chantiers en cours</div>
              </div>
              <div class="col-auto">
                <q-icon name="construction" size="48px" color="primary" class="stats-icon" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Card Tâches -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="stats-card">
          <q-card-section>
            <div class="row items-center">
              <div class="col">
                <div class="stats-value text-secondary">{{ stats.taches }}</div>
                <div class="stats-label">Tâches du jour</div>
              </div>
              <div class="col-auto">
                <q-icon name="assignment" size="48px" color="secondary" class="stats-icon" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Card B2B -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="stats-card">
          <q-card-section>
            <div class="row items-center">
              <div class="col">
                <div class="stats-value text-accent">{{ stats.b2b }}</div>
                <div class="stats-label">Interventions B2B</div>
              </div>
              <div class="col-auto">
                <q-icon name="business_center" size="48px" color="accent" class="stats-icon" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Card Alertes Stock -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card class="stats-card">
          <q-card-section>
            <div class="row items-center">
              <div class="col">
                <div class="stats-value text-warning">{{ stats.alertesStock }}</div>
                <div class="stats-label">Alertes de stock</div>
              </div>
              <div class="col-auto">
                <q-icon name="warning" size="48px" color="warning" class="stats-icon" />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Actions rapides</div>
            <div class="row q-col-gutter-sm">
              <div class="col-12 col-sm-6 col-md-3">
                <q-btn
                  unelevated
                  class="full-width"
                  color="primary"
                  icon="add"
                  label="Nouveau chantier"
                  @click="$q.notify('Fonctionnalité à venir')"
                />
              </div>
              <div class="col-12 col-sm-6 col-md-3">
                <q-btn
                  unelevated
                  class="full-width"
                  color="secondary"
                  icon="assignment_add"
                  label="Nouvelle tâche"
                  @click="$q.notify('Fonctionnalité à venir')"
                />
              </div>
              <div class="col-12 col-sm-6 col-md-3">
                <q-btn
                  unelevated
                  class="full-width"
                  color="accent"
                  icon="build"
                  label="Intervention B2B"
                  @click="$q.notify('Fonctionnalité à venir')"
                />
              </div>
              <div class="col-12 col-sm-6 col-md-3">
                <q-btn
                  unelevated
                  class="full-width"
                  color="positive"
                  icon="inventory"
                  label="Gérer stock"
                  @click="$q.notify('Fonctionnalité à venir')"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-8">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Activités récentes</div>
            <q-list separator>
              <q-item v-for="activity in recentActivities" :key="activity.id">
                <q-item-section avatar>
                  <q-avatar :color="activity.color" text-color="white" :icon="activity.icon" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ activity.title }}</q-item-label>
                  <q-item-label caption>{{ activity.description }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label caption>{{ activity.time }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card>
          <q-card-section>
            <div class="text-h6 q-mb-md">Informations</div>
            <q-list>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="person" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Rôle</q-item-label>
                  <q-item-label caption>{{ authStore.userRole }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="business" color="secondary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Fonction</q-item-label>
                  <q-item-label caption>{{ authStore.user?.profile?.fonction || 'N/A' }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="email" color="accent" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Email</q-item-label>
                  <q-item-label caption>{{ authStore.user?.email }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

// ============================================
// Composables
// ============================================

const $q = useQuasar()
const authStore = useAuthStore()

// ============================================
// State
// ============================================

const loading = ref(false)

const stats = ref({
  projets: 12,
  taches: 38,
  b2b: 24,
  alertesStock: 5
})

const recentActivities = ref([
  {
    id: 1,
    title: 'Nouveau chantier créé',
    description: 'Déploiement FTTH Zone Nord - Orange',
    time: 'Il y a 2h',
    icon: 'construction',
    color: 'primary'
  },
  {
    id: 2,
    title: 'Tâche terminée',
    description: 'Installation PCO - Rue des Jardins',
    time: 'Il y a 4h',
    icon: 'check_circle',
    color: 'positive'
  },
  {
    id: 3,
    title: 'Intervention B2B',
    description: 'Raccordement client entreprise',
    time: 'Il y a 6h',
    icon: 'build',
    color: 'accent'
  },
  {
    id: 4,
    title: 'Rapport généré',
    description: 'RFC Chantier Cocody - Moov',
    time: 'Hier',
    icon: 'description',
    color: 'secondary'
  }
])

// ============================================
// Methods
// ============================================

/**
 * Actualise les données du dashboard
 */
async function refreshDashboard() {
  loading.value = true

  try {
    // Simuler un appel API
    await new Promise(resolve => setTimeout(resolve, 1000))

    $q.notify({
      type: 'positive',
      message: 'Dashboard actualisé',
      position: 'top',
      timeout: 1500
    })
  } catch (error) {
    console.error('Erreur refresh dashboard:', error)
    $q.notify({
      type: 'negative',
      message: 'Erreur lors de l\'actualisation',
      position: 'top'
    })
  } finally {
    loading.value = false
  }
}

// ============================================
// Lifecycle
// ============================================

onMounted(() => {
  // Charger les données du dashboard
  // Dans le futur, appeler l'API pour récupérer les vraies données
})
</script>

<style lang="scss" scoped>
.dashboard-page {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  .page-title {
    font-size: 28px;
    font-weight: 700;
    color: #263238;
    margin-bottom: 4px;
  }

  .page-subtitle {
    font-size: 15px;
    color: #546E7A;
  }
}

.stats-card {
  transition: all 200ms ease-out;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }

  .stats-value {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 4px;
  }

  .stats-label {
    font-size: 13px;
    color: #546E7A;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .stats-icon {
    opacity: 0.2;
  }
}
</style>
