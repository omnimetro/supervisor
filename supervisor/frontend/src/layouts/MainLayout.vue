<template>
  <q-layout view="hHh LpR fFf">
    <!-- Header -->
    <q-header elevated class="bg-white text-dark">
      <q-toolbar>
        <!-- Menu Toggle Button -->
        <q-btn
          flat
          dense
          round
          icon="menu"
          @click="toggleLeftDrawer"
          class="q-mr-sm"
        />

        <!-- Logo/Title -->
        <q-toolbar-title class="text-primary text-weight-bold">
          SUPERVISOR V2.0
        </q-toolbar-title>

        <!-- Spacer -->
        <q-space />

        <!-- Sync Icon with Badge -->
        <q-btn
          flat
          dense
          round
          icon="sync"
          class="q-mr-sm"
          @click="handleSync"
        >
          <q-badge
            v-if="pendingSyncCount > 0"
            color="warning"
            floating
          >
            {{ pendingSyncCount }}
          </q-badge>
          <q-tooltip>
            {{ pendingSyncCount > 0 ? `${pendingSyncCount} données en attente de synchronisation` : 'Synchronisation' }}
          </q-tooltip>
        </q-btn>

        <!-- Notifications Icon with Badge -->
        <q-btn
          flat
          dense
          round
          icon="notifications"
          class="q-mr-sm"
          @click="showNotifications = true"
        >
          <q-badge
            v-if="unreadNotificationsCount > 0"
            color="negative"
            floating
          >
            {{ unreadNotificationsCount }}
          </q-badge>
          <q-tooltip>
            {{ unreadNotificationsCount > 0 ? `${unreadNotificationsCount} notifications non lues` : 'Notifications' }}
          </q-tooltip>
        </q-btn>

        <!-- User Menu -->
        <q-btn-dropdown
          flat
          dense
          no-caps
          class="user-menu-btn"
        >
          <template v-slot:label>
            <div class="row items-center no-wrap">
              <q-avatar size="32px" color="primary" text-color="white" class="q-mr-sm">
                <span class="text-caption">{{ getUserInitials() }}</span>
              </q-avatar>
              <div class="text-left gt-xs">
                <div class="text-body2 text-weight-medium">{{ authStore.userFullName }}</div>
                <div class="text-caption text-grey-6">{{ authStore.userRole }}</div>
              </div>
            </div>
          </template>

          <q-list style="min-width: 220px">
            <!-- User Info Header -->
            <q-item class="bg-grey-2">
              <q-item-section>
                <q-item-label class="text-weight-medium">{{ authStore.userFullName }}</q-item-label>
                <q-item-label caption>{{ authStore.user?.email }}</q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <!-- Mon Profil -->
            <q-item clickable v-close-popup @click="goToProfile">
              <q-item-section avatar>
                <q-icon name="person" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Mon Profil</q-item-label>
              </q-item-section>
            </q-item>

            <!-- Paramètres (Admin only) -->
            <q-item
              v-if="authStore.hasAdminRights"
              clickable
              v-close-popup
              @click="goToSettings"
            >
              <q-item-section avatar>
                <q-icon name="settings" color="secondary" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Paramètres</q-item-label>
              </q-item-section>
            </q-item>

            <!-- Aide -->
            <q-item clickable v-close-popup @click="showHelp">
              <q-item-section avatar>
                <q-icon name="help" color="info" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Aide</q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <!-- Déconnexion -->
            <q-item clickable v-close-popup @click="handleLogout">
              <q-item-section avatar>
                <q-icon name="logout" color="negative" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Se déconnecter</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <!-- Left Drawer (Navigation) -->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :width="260"
      class="main-drawer"
    >
      <!-- Drawer Header -->
      <div class="drawer-header q-pa-md bg-primary text-white">
        <div class="text-h6 text-weight-bold">AI Venture</div>
        <div class="text-caption">Gestion des chantiers</div>
      </div>

      <!-- Navigation Menu -->
      <q-list padding class="menu-list">
        <!-- Dashboard -->
        <q-item
          clickable
          v-ripple
          :active="$route.name === 'dashboard'"
          @click="navigateTo('/dashboard')"
          active-class="active-menu-item"
        >
          <q-item-section avatar>
            <q-icon name="dashboard" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Tableau de Bord</q-item-label>
          </q-item-section>
        </q-item>

        <!-- Chantiers -->
        <q-expansion-item
          icon="construction"
          label="Chantiers"
          header-class="menu-expansion-header"
          default-opened
        >
          <!-- Projets -->
          <q-item
            clickable
            v-ripple
            :inset-level="1"
            :active="$route.name === 'projects'"
            @click="navigateTo('/deployment/projects')"
            active-class="active-menu-item"
          >
            <q-item-section avatar>
              <q-icon name="construction" size="xs" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Projets</q-item-label>
            </q-item-section>
          </q-item>

          <q-separator inset />

          <!-- Opérateurs -->
          <q-item
            clickable
            v-ripple
            :inset-level="1"
            :active="$route.name === 'operators'"
            @click="navigateTo('/deployment/operators')"
            active-class="active-menu-item"
          >
            <q-item-section avatar>
              <q-icon name="business" size="xs" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Opérateurs</q-item-label>
            </q-item-section>
          </q-item>

          <!-- Catégories BOQ -->
          <q-item
            clickable
            v-ripple
            :inset-level="1"
            :active="$route.name === 'boq-categories'"
            @click="navigateTo('/deployment/boq-categories')"
            active-class="active-menu-item"
          >
            <q-item-section avatar>
              <q-icon name="category" size="xs" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Catégories BOQ</q-item-label>
            </q-item-section>
          </q-item>

          <!-- Définitions de tâches -->
          <q-item
            clickable
            v-ripple
            :inset-level="1"
            :active="$route.name === 'task-definitions'"
            @click="navigateTo('/deployment/task-definitions')"
            active-class="active-menu-item"
          >
            <q-item-section avatar>
              <q-icon name="assignment" size="xs" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Définitions de tâches</q-item-label>
            </q-item-section>
          </q-item>

          <!-- Sous-traitants -->
          <q-item
            clickable
            v-ripple
            :inset-level="1"
            :active="$route.name === 'subcontractors'"
            @click="navigateTo('/deployment/subcontractors')"
            active-class="active-menu-item"
          >
            <q-item-section avatar>
              <q-icon name="engineering" size="xs" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Sous-traitants</q-item-label>
            </q-item-section>
          </q-item>

          <!-- Techniciens -->
          <q-item
            clickable
            v-ripple
            :inset-level="1"
            :active="$route.name === 'technicians'"
            @click="navigateTo('/deployment/technicians')"
            active-class="active-menu-item"
          >
            <q-item-section avatar>
              <q-icon name="people" size="xs" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Techniciens</q-item-label>
            </q-item-section>
          </q-item>
        </q-expansion-item>

        <!-- B2B (Future) -->
        <q-expansion-item
          icon="business_center"
          label="B2B"
          header-class="menu-expansion-header"
          disable
        >
          <q-item clickable v-ripple :inset-level="1">
            <q-item-section>Interventions</q-item-section>
          </q-item>
          <q-item clickable v-ripple :inset-level="1">
            <q-item-section>Maintenances</q-item-section>
          </q-item>
        </q-expansion-item>

        <!-- Stocks (Future) -->
        <q-item
          clickable
          v-ripple
          disable
        >
          <q-item-section avatar>
            <q-icon name="inventory" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Stocks</q-item-label>
          </q-item-section>
        </q-item>

        <!-- Dépenses (Future) -->
        <q-item
          clickable
          v-ripple
          disable
        >
          <q-item-section avatar>
            <q-icon name="payments" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Dépenses</q-item-label>
          </q-item-section>
        </q-item>

        <!-- Cartographie (Future) -->
        <q-item
          clickable
          v-ripple
          disable
        >
          <q-item-section avatar>
            <q-icon name="map" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Cartographie</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-my-md" />

        <!-- Administration (Only for SUPERADMIN/ADMIN) -->
        <q-expansion-item
          v-if="authStore.hasAdminRights"
          icon="settings"
          label="Administration"
          header-class="menu-expansion-header"
          disable
        >
          <q-item clickable v-ripple :inset-level="1">
            <q-item-section>Utilisateurs</q-item-section>
          </q-item>
          <q-item clickable v-ripple :inset-level="1">
            <q-item-section>Rôles & Permissions</q-item-section>
          </q-item>
        </q-expansion-item>
      </q-list>

      <!-- Drawer Footer -->
      <div class="drawer-footer absolute-bottom q-pa-md text-center text-caption text-grey-6">
        <div>SUPERVISOR V2.0</div>
        <div>&copy; {{ currentYear }} AI Venture</div>
      </div>
    </q-drawer>

    <!-- Page Container -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Notifications Dialog -->
    <q-dialog v-model="showNotifications" position="right">
      <q-card style="width: 400px; max-width: 90vw">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Notifications</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-list v-if="notifications.length > 0" separator>
            <q-item
              v-for="notification in notifications"
              :key="notification.id"
              :class="{ 'bg-grey-2': !notification.read }"
              clickable
              @click="markAsRead(notification.id)"
            >
              <q-item-section avatar>
                <q-avatar :color="getNotificationColor(notification.type)" text-color="white">
                  <q-icon :name="getNotificationIcon(notification.type)" />
                </q-avatar>
              </q-item-section>
              <q-item-section>
                <q-item-label>{{ notification.title }}</q-item-label>
                <q-item-label caption>{{ notification.message }}</q-item-label>
                <q-item-label caption class="text-grey-6">{{ notification.time }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>

          <div v-else class="text-center text-grey-6 q-py-lg">
            <q-icon name="notifications_none" size="48px" class="q-mb-sm" />
            <div>Aucune notification</div>
          </div>
        </q-card-section>

        <q-card-actions v-if="notifications.length > 0" align="right">
          <q-btn
            flat
            label="Tout marquer comme lu"
            color="primary"
            @click="markAllAsRead"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

// ============================================
// Composables
// ============================================

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

// ============================================
// State
// ============================================

const leftDrawerOpen = ref(false)
const currentYear = new Date().getFullYear()
const showNotifications = ref(false)
const pendingSyncCount = ref(0)  // Nombre de données en attente de synchronisation

// Notifications (simulées, à remplacer par appel API)
const notifications = ref([
  {
    id: 1,
    type: 'info',
    title: 'Nouveau chantier assigné',
    message: 'Déploiement FTTH Zone Nord - Orange',
    time: 'Il y a 5 minutes',
    read: false
  },
  {
    id: 2,
    type: 'success',
    title: 'Tâche terminée',
    message: 'Installation PCO - Rue des Jardins',
    time: 'Il y a 2 heures',
    read: false
  },
  {
    id: 3,
    type: 'warning',
    title: 'Stock faible',
    message: 'Le stock de câbles optiques est faible',
    time: 'Il y a 1 jour',
    read: true
  }
])

// Computed pour compter les notifications non lues
const unreadNotificationsCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

// ============================================
// Methods
// ============================================

/**
 * Toggle left drawer
 */
function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

/**
 * Navigate to route
 */
function navigateTo(path) {
  router.push(path)
}

/**
 * Go to profile page
 */
function goToProfile() {
  router.push('/profile')
}

/**
 * Handle logout
 */
async function handleLogout() {
  $q.dialog({
    title: 'Déconnexion',
    message: 'Êtes-vous sûr de vouloir vous déconnecter ?',
    cancel: {
      label: 'Annuler',
      flat: true
    },
    ok: {
      label: 'Déconnexion',
      color: 'negative'
    },
    persistent: true
  }).onOk(async () => {
    try {
      await authStore.logout()

      $q.notify({
        type: 'info',
        message: 'Déconnexion réussie',
        position: 'top',
        timeout: 2000
      })

      router.push('/auth/login')
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error)
    }
  })
}

/**
 * Get user initials for avatar
 */
function getUserInitials() {
  const fullName = authStore.userFullName
  if (!fullName) return 'U'

  const names = fullName.split(' ')
  if (names.length >= 2) {
    return (names[0][0] + names[1][0]).toUpperCase()
  }
  return fullName.substring(0, 2).toUpperCase()
}

/**
 * Handle sync button click
 */
function handleSync() {
  $q.notify({
    type: 'info',
    message: 'Synchronisation en cours...',
    position: 'top',
    timeout: 2000
  })

  // TODO: Implémenter la logique de synchronisation
  // - Envoyer les données en attente vers le serveur
  // - Récupérer les nouvelles données du serveur
  // - Mettre à jour pendingSyncCount
}

/**
 * Go to settings page (Admin only)
 */
function goToSettings() {
  router.push('/settings')
}

/**
 * Show help dialog
 */
function showHelp() {
  $q.dialog({
    title: 'Aide',
    message: 'Documentation et support technique à venir. Pour toute question, contactez l\'administrateur.',
    ok: {
      label: 'Fermer',
      color: 'primary'
    }
  })

  // TODO: Créer une page d'aide complète ou ouvrir un lien vers la documentation
}

/**
 * Mark a notification as read
 */
function markAsRead(notificationId) {
  const notification = notifications.value.find(n => n.id === notificationId)
  if (notification) {
    notification.read = true

    // TODO: Appeler l'API pour marquer la notification comme lue
    // await apiService.notifications.markAsRead(notificationId)
  }
}

/**
 * Mark all notifications as read
 */
function markAllAsRead() {
  notifications.value.forEach(n => {
    n.read = true
  })

  $q.notify({
    type: 'positive',
    message: 'Toutes les notifications ont été marquées comme lues',
    position: 'top',
    timeout: 2000
  })

  // TODO: Appeler l'API pour marquer toutes les notifications comme lues
  // await apiService.notifications.markAllAsRead()
}

/**
 * Get notification color based on type
 */
function getNotificationColor(type) {
  const colors = {
    info: 'info',
    success: 'positive',
    warning: 'warning',
    error: 'negative'
  }
  return colors[type] || 'grey'
}

/**
 * Get notification icon based on type
 */
function getNotificationIcon(type) {
  const icons = {
    info: 'info',
    success: 'check_circle',
    warning: 'warning',
    error: 'error'
  }
  return icons[type] || 'notifications'
}
</script>

<style lang="scss" scoped>
@use 'sass:color';

// ============================================
// Variables
// ============================================

$primary-color: #ea1d31;
$drawer-width: 260px;

// ============================================
// Header
// ============================================

.q-header {
  border-bottom: 1px solid #E0E0E0;
}

.user-menu-btn {
  :deep(.q-btn__content) {
    padding: 4px 8px;
  }
}

// ============================================
// Drawer
// ============================================

.main-drawer {
  .drawer-header {
    background: linear-gradient(135deg, $primary-color 0%, color.adjust($primary-color, $lightness: -10%) 100%);
  }

  .drawer-footer {
    border-top: 1px solid #E0E0E0;
  }
}

// ============================================
// Navigation Menu
// ============================================

.menu-list {
  .q-item {
    border-radius: 8px;
    margin: 4px 8px;
    transition: all 200ms ease-out;

    &:hover:not(.q-item--disabled) {
      background-color: rgba($primary-color, 0.05);
    }

    &.active-menu-item {
      background-color: rgba($primary-color, 0.1);
      color: $primary-color;
      font-weight: 600;

      :deep(.q-icon) {
        color: $primary-color;
      }
    }

    &.q-item--disabled {
      opacity: 0.5;
    }
  }

  .q-expansion-item {
    :deep(.q-item) {
      border-radius: 8px;
      margin: 4px 8px;
    }

    &.q-expansion-item--disabled {
      opacity: 0.5;
    }
  }

  .menu-expansion-header {
    border-radius: 8px;
    margin: 4px 8px;
    transition: all 200ms ease-out;

    &:hover {
      background-color: rgba($primary-color, 0.05);
    }
  }
}

// ============================================
// Responsive
// ============================================

@media (max-width: 1023px) {
  .main-drawer {
    .drawer-footer {
      display: none;
    }
  }
}
</style>
