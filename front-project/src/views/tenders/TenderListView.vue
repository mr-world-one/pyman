<template>
  <div class="tender-list">
    <div class="tender-list__inner">
      <!-- Page header -->
      <div class="page-header">
        <div>
          <h1 class="page-header__title">Мої тендери</h1>
          <p class="page-header__subtitle num">
            {{ store.tenders.length }} закупівель
            <span v-if="store.tenders.length" class="page-header__sep">·</span>
            <span v-if="store.tenders.length">оновлено {{ updatedLabel }}</span>
          </p>
        </div>
        <div class="page-header__actions">
          <AppButton variant="secondary">
            <template #icon-left><AppIcon name="download" :size="14" /></template>
            Експорт
          </AppButton>
          <AppButton @click="showImportModal = true">
            <template #icon-left><AppIcon name="plus" :size="14" /></template>
            Імпорт з Prozorro
          </AppButton>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-row">
        <TenderFilters v-model="store.filters" @update:modelValue="onFilterChange" />
        <div class="view-toggle">
          <button
            :class="['view-toggle__btn', { 'is-active': view === 'grid' }]"
            aria-label="Сітка"
            @click="view = 'grid'"
          >
            <AppIcon name="grid" :size="14" />
          </button>
          <button
            :class="['view-toggle__btn', { 'is-active': view === 'list' }]"
            aria-label="Список"
            @click="view = 'list'"
          >
            <AppIcon name="list" :size="14" />
          </button>
        </div>
      </div>

      <AppLoader v-if="store.loading" :overlay="false" />

      <div v-else-if="store.error" class="alert alert-error">{{ store.error }}</div>

      <EmptyState
        v-else-if="store.tenders.length === 0"
        icon-name="package"
        title="Тендерів поки немає"
        description="Імпортуйте першу закупівлю з Prozorro або завантажте Excel-файл."
      >
        <AppButton @click="showImportModal = true">
          <template #icon-left><AppIcon name="plus" :size="14" /></template>
          Імпорт з Prozorro
        </AppButton>
        <router-link to="/excel-page" class="empty-link">
          Завантажити Excel
        </router-link>
      </EmptyState>

      <div v-else :class="['tenders-grid', `tenders-grid--${view}`]">
        <TenderCard
          v-for="tender in store.tenders"
          :key="tender.id"
          :tender="tender"
          @click="$router.push(`/tenders/${tender.id}`)"
        />
      </div>

      <!-- Pagination -->
      <div v-if="store.tenders.length > 0" class="pagination">
        <div class="pagination__info">
          Сторінка <span class="num">{{ store.filters.page }}</span>
        </div>
        <div class="pagination__controls">
          <AppButton
            variant="secondary"
            size="sm"
            :disabled="store.filters.page <= 1"
            @click="prevPage"
          >
            <template #icon-left><AppIcon name="chevron-left" :size="14" /></template>
            Попередня
          </AppButton>
          <AppButton
            variant="secondary"
            size="sm"
            :disabled="store.tenders.length < store.filters.limit"
            @click="nextPage"
          >
            Наступна
            <template #icon-right><AppIcon name="chevron-right" :size="14" /></template>
          </AppButton>
        </div>
      </div>

      <TenderImportModal
        v-if="showImportModal"
        v-model="showImportModal"
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
import AppIcon from '@/components/AppIcon.vue'
import EmptyState from '@/components/EmptyState.vue'
import TenderCard from '@/components/tenders/TenderCard.vue'
import TenderFilters from '@/components/tenders/TenderFilters.vue'
import TenderImportModal from '@/components/tenders/TenderImportModal.vue'

export default {
  name: 'TenderListView',
  components: { AppButton, AppLoader, AppIcon, EmptyState, TenderCard, TenderFilters, TenderImportModal },
  setup() {
    const store = useTendersStore()
    const router = useRouter()
    const showImportModal = ref(false)
    const view = ref('grid')
    const updatedLabel = ref('щойно')

    onMounted(() => {
      store.fetchTenders()
    })

    const onFilterChange = (newFilters) => {
      store.filters = newFilters
      store.fetchTenders()
    }

    const onImported = (tender) => {
      router.push(`/tenders/${tender.id}`)
    }

    const nextPage = () => { store.nextPage(); store.fetchTenders() }
    const prevPage = () => { store.prevPage(); store.fetchTenders() }

    return { store, showImportModal, view, updatedLabel, onFilterChange, onImported, nextPage, prevPage }
  },
}
</script>

<style scoped>
.tender-list {
  padding: calc(var(--header-height) + var(--space-8)) var(--space-6) var(--space-12);
}

.tender-list__inner {
  max-width: var(--container-max-width);
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
  margin-bottom: var(--space-6);
}

.page-header__title {
  font-size: clamp(1.75rem, 3vw, 2rem);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
}

.page-header__subtitle {
  margin-top: 4px;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.page-header__sep {
  margin: 0 4px;
  opacity: 0.6;
}

.page-header__actions {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.filters-row {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
}

.view-toggle {
  margin-left: auto;
  display: inline-flex;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: 2px;
}

.view-toggle__btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.view-toggle__btn:hover { color: var(--color-text); }

.view-toggle__btn.is-active {
  background: var(--color-bg-subtle);
  color: var(--color-heading);
}

.tenders-grid--grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-4);
}

.tenders-grid--list {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-2);
}

.empty-link {
  display: inline-flex;
  align-items: center;
  height: 36px;
  padding: 0 var(--space-4);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  color: var(--color-text);
  text-decoration: none;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
}

.empty-link:hover {
  background: var(--color-bg-subtle);
  color: var(--color-heading);
}

.pagination {
  margin-top: var(--space-8);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  font-size: var(--text-sm);
  flex-wrap: wrap;
}

.pagination__info { color: var(--color-text-secondary); }

.pagination__controls {
  display: flex;
  gap: var(--space-2);
}

@media (max-width: 640px) {
  .tender-list { padding: calc(var(--header-height) + var(--space-6)) var(--space-4) var(--space-10); }
}
</style>
