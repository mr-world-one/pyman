<template>
  <div class="tender-list-page">
    <div class="tender-list-container">
      <div class="page-header">
        <h1>Мої тендери</h1>
        <div class="header-actions">
          <AppButton variant="ghost" @click="showImportModal = true">Імпорт з Prozorro</AppButton>
          <AppButton @click="$router.push('/tenders/create')">Створити тендер</AppButton>
        </div>
      </div>

      <TenderFilters v-model="store.filters.value" @update:modelValue="onFilterChange" />

      <AppLoader v-if="store.loading.value" />

      <div v-else-if="store.error.value" class="error-message">
        <p>{{ store.error.value }}</p>
      </div>

      <div v-else-if="store.tenders.value.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>Тендерів поки немає</h3>
        <p>Створіть новий тендер або імпортуйте з Prozorro</p>
      </div>

      <div v-else class="tenders-grid">
        <TenderCard
          v-for="tender in store.tenders.value"
          :key="tender.id"
          :tender="tender"
          @click="$router.push(`/tenders/${tender.id}`)"
        />
      </div>

      <div v-if="store.tenders.value.length > 0" class="pagination">
        <AppButton variant="ghost" size="sm" :disabled="store.filters.value.page <= 1" @click="store.prevPage(); store.fetchTenders()">
          &larr; Назад
        </AppButton>
        <span class="page-num">Сторінка {{ store.filters.value.page }}</span>
        <AppButton variant="ghost" size="sm" :disabled="store.tenders.value.length < store.filters.value.limit" @click="store.nextPage(); store.fetchTenders()">
          Вперед &rarr;
        </AppButton>
      </div>

      <TenderImportModal
        v-if="showImportModal"
        @close="showImportModal = false"
        @imported="onImported"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTendersStore } from '@/stores/tenders'
import AppButton from '@/components/AppButton.vue'
import AppLoader from '@/components/AppLoader.vue'
import TenderCard from '@/components/tenders/TenderCard.vue'
import TenderFilters from '@/components/tenders/TenderFilters.vue'
import TenderImportModal from '@/components/tenders/TenderImportModal.vue'

export default {
  name: 'TenderListView',
  components: { AppButton, AppLoader, TenderCard, TenderFilters, TenderImportModal },
  setup() {
    const store = useTendersStore()
    const router = useRouter()
    const showImportModal = ref(false)

    onMounted(() => {
      store.fetchTenders()
    })

    const onFilterChange = (newFilters) => {
      store.filters.value = newFilters
      store.fetchTenders()
    }

    const onImported = (tender) => {
      router.push(`/tenders/${tender.id}`)
    }

    return { store, showImportModal, onFilterChange, onImported }
  },
}
</script>

<style scoped>
.tender-list-page {
  display: flex;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  padding-top: 100px;
}

.tender-list-container {
  max-width: 1100px;
  width: 100%;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.page-header h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: var(--space-2);
}

.tenders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-4);
  margin-top: var(--space-6);
}

.empty-state {
  text-align: center;
  padding: var(--space-16) var(--space-4);
  color: var(--color-text-secondary);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: var(--space-3);
}

.empty-state h3 {
  font-size: var(--text-xl);
  color: var(--color-heading);
  margin-bottom: var(--space-2);
}

.error-message {
  text-align: center;
  color: var(--color-danger);
  padding: var(--space-8);
  font-size: var(--text-lg);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  margin-top: var(--space-8);
}

.page-num {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-medium);
}
</style>
