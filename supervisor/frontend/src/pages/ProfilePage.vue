<template>
  <q-page class="profile-page q-pa-md">
    <div class="profile-container">
      <!-- Header -->
      <div class="page-header q-mb-lg">
        <h4 class="page-title q-my-none">Mon Profil</h4>
        <p class="page-subtitle q-my-none text-grey-6">
          Gérez vos informations personnelles et paramètres
        </p>
      </div>

      <div class="row q-col-gutter-lg">
        <!-- Left Column - Profile Info -->
        <div class="col-12 col-md-4">
          <q-card>
            <q-card-section class="text-center">
              <!-- Photo Profile -->
              <q-avatar size="120px" color="primary" text-color="white" class="q-mb-md">
                <img v-if="authStore.user?.profile?.photo" :src="authStore.user.profile.photo" />
                <span v-else class="text-h4">
                  {{ getInitials(authStore.userFullName) }}
                </span>
              </q-avatar>

              <!-- Nom -->
              <div class="text-h5 q-mb-xs">{{ authStore.userFullName }}</div>
              <div class="text-subtitle2 text-grey-6 q-mb-sm">{{ authStore.user?.email }}</div>

              <!-- Badge Rôle -->
              <q-badge :color="getRoleColor(authStore.userRole)" class="q-px-md q-py-xs">
                {{ authStore.userRole }}
              </q-badge>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <q-list>
                <q-item>
                  <q-item-section avatar>
                    <q-icon name="badge" color="primary" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label caption>Code</q-item-label>
                    <q-item-label>{{ authStore.user?.profile?.code }}</q-item-label>
                  </q-item-section>
                </q-item>

                <q-item>
                  <q-item-section avatar>
                    <q-icon name="business" color="secondary" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label caption>Fonction</q-item-label>
                    <q-item-label>{{ authStore.user?.profile?.fonction || 'N/A' }}</q-item-label>
                  </q-item-section>
                </q-item>

                <q-item>
                  <q-item-section avatar>
                    <q-icon name="phone" color="accent" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label caption>Téléphone</q-item-label>
                    <q-item-label>{{ authStore.user?.profile?.telephone || 'N/A' }}</q-item-label>
                  </q-item-section>
                </q-item>

                <q-item v-if="authStore.user?.profile?.superieur_hierarchique">
                  <q-item-section avatar>
                    <q-icon name="supervisor_account" color="positive" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label caption>Supérieur hiérarchique</q-item-label>
                    <q-item-label>
                      {{ authStore.user.profile.superieur_hierarchique }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card-section>
          </q-card>
        </div>

        <!-- Right Column - Forms -->
        <div class="col-12 col-md-8">
          <!-- Update Profile Form -->
          <q-card class="q-mb-md">
            <q-card-section>
              <div class="text-h6 q-mb-md">Informations personnelles</div>

              <q-form @submit="handleUpdateProfile" class="q-gutter-md">
                <div class="row q-col-gutter-md">
                  <div class="col-12 col-sm-6">
                    <q-input
                      v-model="profileForm.nom"
                      label="Nom"
                      outlined
                      :disable="loading"
                      readonly
                    />
                  </div>

                  <div class="col-12 col-sm-6">
                    <q-input
                      v-model="profileForm.prenoms"
                      label="Prénoms"
                      outlined
                      :disable="loading"
                      readonly
                    />
                  </div>

                  <div class="col-12">
                    <q-input
                      v-model="profileForm.email"
                      type="email"
                      label="Email"
                      outlined
                      :disable="loading"
                      :rules="[
                        val => !!val || 'Email requis',
                        val => /.+@.+\..+/.test(val) || 'Email invalide'
                      ]"
                    />
                  </div>

                  <div class="col-12">
                    <q-input
                      v-model="profileForm.telephone"
                      label="Téléphone"
                      outlined
                      :disable="loading"
                      mask="## ## ## ## ##"
                      hint="Format: 07 07 07 07 07"
                    />
                  </div>
                </div>

                <div class="row justify-end">
                  <q-btn
                    type="submit"
                    label="Mettre à jour"
                    color="primary"
                    :loading="loading"
                    :disable="loading"
                    unelevated
                  />
                </div>
              </q-form>
            </q-card-section>
          </q-card>

          <!-- Change Password Form -->
          <q-card>
            <q-card-section>
              <div class="text-h6 q-mb-md">Changer le mot de passe</div>

              <q-form @submit="handleChangePassword" class="q-gutter-md">
                <q-input
                  v-model="passwordForm.old_password"
                  :type="showOldPassword ? 'text' : 'password'"
                  label="Ancien mot de passe"
                  outlined
                  :disable="loading"
                  :rules="[val => !!val || 'Requis']"
                >
                  <template v-slot:append>
                    <q-icon
                      :name="showOldPassword ? 'visibility_off' : 'visibility'"
                      class="cursor-pointer"
                      @click="showOldPassword = !showOldPassword"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="passwordForm.new_password"
                  :type="showNewPassword ? 'text' : 'password'"
                  label="Nouveau mot de passe"
                  outlined
                  :disable="loading"
                  :rules="[
                    val => !!val || 'Requis',
                    val => val.length >= 8 || 'Minimum 8 caractères'
                  ]"
                >
                  <template v-slot:append>
                    <q-icon
                      :name="showNewPassword ? 'visibility_off' : 'visibility'"
                      class="cursor-pointer"
                      @click="showNewPassword = !showNewPassword"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="passwordForm.confirm_password"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  label="Confirmer le mot de passe"
                  outlined
                  :disable="loading"
                  :rules="[
                    val => !!val || 'Requis',
                    val => val === passwordForm.new_password || 'Les mots de passe ne correspondent pas'
                  ]"
                >
                  <template v-slot:append>
                    <q-icon
                      :name="showConfirmPassword ? 'visibility_off' : 'visibility'"
                      class="cursor-pointer"
                      @click="showConfirmPassword = !showConfirmPassword"
                    />
                  </template>
                </q-input>

                <div class="row justify-end">
                  <q-btn
                    type="submit"
                    label="Changer le mot de passe"
                    color="primary"
                    :loading="loading"
                    :disable="loading"
                    unelevated
                  />
                </div>
              </q-form>
            </q-card-section>
          </q-card>
        </div>
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
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const profileForm = ref({
  nom: '',
  prenoms: '',
  email: '',
  telephone: ''
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// ============================================
// Methods
// ============================================

/**
 * Obtenir les initiales du nom complet
 */
function getInitials(fullName) {
  if (!fullName) return 'U'
  const names = fullName.split(' ')
  if (names.length >= 2) {
    return (names[0][0] + names[1][0]).toUpperCase()
  }
  return fullName.substring(0, 2).toUpperCase()
}

/**
 * Obtenir la couleur du badge selon le rôle
 */
function getRoleColor(role) {
  const colors = {
    SUPERADMIN: 'negative',
    ADMIN: 'warning',
    COORDONNATEUR: 'info',
    STOCKMAN: 'purple',
    SUPERVISEUR: 'positive'
  }
  return colors[role] || 'grey'
}

/**
 * Mettre à jour le profil
 */
async function handleUpdateProfile() {
  loading.value = true

  try {
    await authStore.updateUserProfile({
      email: profileForm.value.email,
      profile: {
        telephone: profileForm.value.telephone
      }
    })

    $q.notify({
      type: 'positive',
      message: 'Profil mis à jour avec succès',
      position: 'top',
      timeout: 2000
    })
  } catch (error) {
    console.error('Erreur mise à jour profil:', error)
    $q.notify({
      type: 'negative',
      message: error.response?.data?.detail || 'Erreur lors de la mise à jour',
      position: 'top'
    })
  } finally {
    loading.value = false
  }
}

/**
 * Changer le mot de passe
 */
async function handleChangePassword() {
  loading.value = true

  try {
    await authStore.changePassword({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    })

    $q.notify({
      type: 'positive',
      message: 'Mot de passe changé avec succès',
      position: 'top',
      timeout: 2000
    })

    // Réinitialiser le formulaire
    passwordForm.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    console.error('Erreur changement mot de passe:', error)
    $q.notify({
      type: 'negative',
      message: error.response?.data?.old_password?.[0] || 'Erreur lors du changement',
      position: 'top'
    })
  } finally {
    loading.value = false
  }
}

/**
 * Charger les données du profil
 */
function loadProfileData() {
  if (authStore.user) {
    profileForm.value = {
      nom: authStore.user.profile?.nom || '',
      prenoms: authStore.user.profile?.prenoms || '',
      email: authStore.user.email || '',
      telephone: authStore.user.profile?.telephone || ''
    }
  }
}

// ============================================
// Lifecycle
// ============================================

onMounted(() => {
  loadProfileData()
})
</script>

<style lang="scss" scoped>
.profile-page {
  max-width: 1200px;
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
</style>
