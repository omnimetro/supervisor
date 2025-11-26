<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md">Test Page Opérateurs</div>

    <div class="q-mb-md">
      <div>Store chargé : {{ storeLoaded }}</div>
      <div>Loading : {{ loading }}</div>
      <div>Erreur : {{ error }}</div>
      <div>Nombre d'opérateurs : {{ operators.length }}</div>
    </div>

    <q-btn
      color="primary"
      label="Charger les opérateurs"
      @click="loadOperators"
      :loading="loading"
    />

    <q-card class="q-mt-md" v-if="operators.length > 0">
      <q-card-section>
        <div class="text-h6">Liste des opérateurs</div>
      </q-card-section>
      <q-card-section>
        <div v-for="op in operators" :key="op.id" class="q-mb-sm">
          {{ op.nom }} ({{ op.code }})
        </div>
      </q-card-section>
    </q-card>

    <q-card class="q-mt-md" v-else-if="!loading">
      <q-card-section>
        <div class="text-grey-7">Aucun opérateur trouvé. Cliquez sur "Charger les opérateurs" pour tester l'API.</div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDeploymentStore } from 'src/stores/deployment'

const deploymentStore = useDeploymentStore()
const storeLoaded = ref(false)

// État local (refs au lieu de computed)
const operators = ref([])
const loading = ref(false)
const error = ref(null)

async function loadOperators() {
  loading.value = true
  error.value = null
  try {
    console.log('Chargement des opérateurs...')
    const result = await deploymentStore.operators.list()
    console.log('API result:', result)

    // Mettre à jour le ref local avec les données retournées
    operators.value = Array.isArray(result) ? result : []
    console.log('Opérateurs chargés (local ref):', operators.value)
  } catch (err) {
    console.error('Erreur lors du chargement:', err)
    error.value = err.message || 'Erreur de chargement'
    operators.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  console.log('deploymentStore:', deploymentStore)
  console.log('deploymentStore.operators:', deploymentStore.operators)
  storeLoaded.value = !!deploymentStore
})
</script>
