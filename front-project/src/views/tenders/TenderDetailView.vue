<template>
  <div class="tender-detail-page">
    <div class="tender-detail-container" v-if="tender">
      <div class="detail-header">
        <div class="header-left">
          <AppButton variant="ghost" size="sm" @click="$router.push('/tenders')">&larr; До списку</AppButton>
          <TenderTypeBadge :type="tender.tender_type" />
          <span class="detail-status" :class="'status-' + tender.status">{{ tender.status }}</span>
        </div>
        <div class="header-right">
          <AppButton v-if="tender.tender_type !== 'service'" variant="ghost" @click="showAnalysis = true" :disabled="analyzing">
            {{ analyzing ? 'Аналізуємо...' : 'Аналіз цін' }}
          </AppButton>
          <AppButton variant="danger" size="sm" @click="handleDelete">Видалити</AppButton>
        </div>
      </div>

      <h1>{{ tender.title }}</h1>

      <div class="meta-row">
        <span class="meta-id">{{ tender.prozorro_id }}</span>
        <span v-if="tender.customer_name" class="meta-customer">{{ tender.customer_name }}</span>
        <span v-if="tender.region" class="meta-region">{{ tender.region }}</span>
        <span class="meta-date">{{ formatDate(tender.created_at) }}</span>
      </div>

      <p v-if="tender.description" class="tender-description">{{ tender.description }}</p>

      <div class="summary-cards">
        <div class="summary-card">
          <div class="summary-label">Загальна сума</div>
          <div class="summary-value">{{ formatPrice(tender.total_amount) }} {{ tender.currency }}</div>
        </div>
        <div class="summary-card" v-if="tender.expected_cost">
          <div class="summary-label">Очікувана вартість</div>
          <div class="summary-value">{{ formatPrice(tender.expected_cost) }} {{ tender.currency }}</div>
        </div>
        <div class="summary-card">
          <div class="summary-label">Позицій</div>
          <div class="summary-value">{{ tender.items.length }}</div>
        </div>
      </div>

      <div class="items-section">
        <ProductTenderDetail v-if="tender.tender_type === 'product'" :items="tender.items" />
        <ServiceTenderDetail v-if="tender.tender_type === 'service'" :items="tender.items" />
        <WorkTenderDetail v-if="tender.tender_type === 'work'" :items="tender.items" />
      </div>

      <!-- Analysis results -->
      <div v-if="analysisResults" class="analysis-section">
        <h2>Результати аналізу цін</h2>
        <div v-for="group in processedAnalysis" :key="group.name" class="product-group">
          <div class="product-header">
            <div class="product-name">{{ group.name }}</div>
            <div class="product-meta">
              <span class="meta-badge tender-badge" v-if="group.tender_price > 0">
                Тендер: <strong>{{ formatPrice(group.tender_price) }} грн</strong>
              </span>
              <span class="meta-badge qty-badge" v-if="group.quantity">{{ group.quantity }} {{ group.unit_name || 'шт' }}</span>
            </div>
          </div>
          <table class="modern-table" v-if="group.matches.length">
            <thead>
              <tr>
                <th>Магазин</th>
                <th>Назва</th>
                <th>Ціна</th>
                <th>Різниця</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(match, idx) in group.matches" :key="idx" :class="{ 'best-match': idx === 0 }">
                <td><span class="store-badge" :class="'store-' + match.store">{{ match.store_name }}</span></td>
                <td class="name-cell">
                  <a :href="match.url" target="_blank" rel="noopener" v-if="match.url">{{ match.title }}</a>
                  <span v-else>{{ match.title }}</span>
                </td>
                <td class="price-cell">{{ formatPrice(match.effective_price) }} грн</td>
                <td :class="match.diff > 0 ? 'price-higher' : match.diff < 0 ? 'price-lower' : ''">
                  {{ match.diff != null ? ((match.diff >= 0 ? '+' : '') + formatPrice(match.diff) + ' грн') : '—' }}
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="no-matches">Не знайдено в магазинах</div>
        </div>
      </div>

      <!-- Store selector modal for analysis -->
      <div v-if="showAnalysis" class="analysis-modal-overlay" @click.self="showAnalysis = false">
        <div class="analysis-modal">
          <h3>Вибір магазинів для аналізу</h3>
          <StoreSelector v-model="selectedStores" :stores="availableStores" />
          <div class="modal-actions">
            <AppButton variant="ghost" @click="showAnalysis = false">Скасувати</AppButton>
            <AppButton :disabled="selectedStores.length === 0 || analyzing" @click="runAnalysis">
              {{ analyzing ? 'Аналізуємо...' : 'Запустити аналіз' }}
            </AppButton>
          </div>
        </div>
      </div>
    </div>

    <AppLoader v-if="store.loading.value && !tender" :overlay="true" />

    <div v-if="store.error.value && !tender" class="error-page">
      <p>{{ store.error.value }}</p>
      <AppButton @click="$router.push('/tenders')">До списку тендерів</AppButton>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTendersStore } from '@/stores/tenders'
import AppButton from '@/components/AppButton.vue'
import AppLoader from '@/components/AppLoader.vue'
import StoreSelector from '@/components/StoreSelector.vue'
import TenderTypeBadge from '@/components/tenders/TenderTypeBadge.vue'
import ProductTenderDetail from '@/components/tenders/details/ProductTenderDetail.vue'
import ServiceTenderDetail from '@/components/tenders/details/ServiceTenderDetail.vue'
import WorkTenderDetail from '@/components/tenders/details/WorkTenderDetail.vue'

export default {
  name: 'TenderDetailView',
  components: {
    AppButton, AppLoader, StoreSelector, TenderTypeBadge,
    ProductTenderDetail, ServiceTenderDetail, WorkTenderDetail,
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const store = useTendersStore()

    const tender = computed(() => store.currentTender.value)
    const showAnalysis = ref(false)
    const analyzing = ref(false)
    const analysisResults = ref(null)
    const selectedStores = ref(['rozetka', 'silpo', 'epicentr'])
    const availableStores = [
      { key: 'rozetka', name: 'Rozetka' },
      { key: 'silpo', name: 'Сільпо' },
      { key: 'epicentr', name: 'Епіцентр' },
      { key: 'citadel', name: 'Citadel' },
    ]

    onMounted(() => {
      store.fetchTender(Number(route.params.id))
    })

    const processedAnalysis = computed(() => {
      if (!analysisResults.value?.matched_items) return []
      return analysisResults.value.matched_items.map((group) => {
        const t = group.tender_item || {}
        const tenderPrice = parseFloat(t.unit_price) || 0
        const matches = (group.matches || []).map((item) => {
          const ep = item.price_on_sale ? parseFloat(item.price_on_sale) : parseFloat(item.price) || null
          return {
            title: item.title || '—',
            store: item.store || '',
            store_name: item.store_name || '—',
            url: item.url || null,
            effective_price: ep,
            diff: (ep !== null && tenderPrice > 0) ? tenderPrice - ep : null,
          }
        }).sort((a, b) => (a.effective_price ?? Infinity) - (b.effective_price ?? Infinity))

        return { name: t.name || '', tender_price: tenderPrice, quantity: t.quantity, unit_name: t.unit_name, matches }
      }).filter((g) => g.name)
    })

    const runAnalysis = async () => {
      analyzing.value = true
      showAnalysis.value = false
      try {
        const result = await store.analyzeTender(Number(route.params.id), selectedStores.value)
        analysisResults.value = result
      } catch {
        // error is handled by store
      } finally {
        analyzing.value = false
      }
    }

    const handleDelete = async () => {
      if (!confirm('Видалити цей тендер?')) return
      try {
        await store.deleteTender(Number(route.params.id))
        router.push('/tenders')
      } catch {
        // error is handled by store
      }
    }

    const formatPrice = (val) => {
      if (val == null) return '—'
      return Number(val).toLocaleString('uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('uk-UA')
    }

    return {
      store, tender, showAnalysis, analyzing, analysisResults, selectedStores,
      availableStores, processedAnalysis,
      runAnalysis, handleDelete, formatPrice, formatDate,
    }
  },
}
</script>

<style scoped>
.tender-detail-page {
  display: flex;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  padding-top: 100px;
}

.tender-detail-container {
  max-width: 1100px;
  width: 100%;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.header-left, .header-right {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.detail-status {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-full);
}

.status-active { background: var(--color-green-100); color: var(--color-green-700); }
.status-closed { background: var(--color-gray-100); color: var(--color-gray-600); }
.status-cancelled { background: var(--color-danger-light); color: var(--color-danger); }

.tender-detail-container h1 {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-3);
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.meta-id { font-family: monospace; color: var(--color-info); }

.tender-description {
  color: var(--color-text-secondary);
  font-size: var(--text-base);
  margin-bottom: var(--space-6);
  line-height: 1.6;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.summary-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  text-align: center;
}

.summary-label { font-size: var(--text-sm); color: var(--color-text-secondary); margin-bottom: 0.3rem; }
.summary-value { font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--color-heading); }

.items-section {
  margin-bottom: var(--space-8);
}

/* Analysis */
.analysis-section {
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 2px solid var(--color-green-200);
}

.analysis-section h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-4);
}

.product-group { margin-bottom: var(--space-6); }

.product-header {
  background: var(--color-green-50);
  border: 1px solid var(--color-green-200);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  margin-bottom: var(--space-2);
}

.product-name { font-weight: var(--font-bold); color: var(--color-heading); margin-bottom: var(--space-1); }
.product-meta { display: flex; flex-wrap: wrap; gap: var(--space-2); }
.meta-badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: var(--radius-full); font-size: var(--text-xs); font-weight: var(--font-semibold); }
.tender-badge { background: var(--color-info-bg); color: var(--color-info); }
.qty-badge { background: var(--color-primary-light); color: var(--color-primary); }

.modern-table { width: 100%; border-collapse: collapse; box-shadow: var(--shadow-sm); border-radius: var(--radius-md); overflow: hidden; }
.modern-table th { background: var(--color-gray-100); color: var(--color-text-secondary); padding: 10px 14px; font-size: var(--text-xs); font-weight: var(--font-bold); text-align: center; text-transform: uppercase; border-bottom: 2px solid var(--color-border); }
.modern-table td { padding: 10px 14px; text-align: center; color: var(--color-text); font-size: var(--text-sm); border-bottom: 1px solid var(--color-border); background: var(--color-surface); }
.modern-table td a { color: var(--color-info); text-decoration: none; }
.modern-table td a:hover { text-decoration: underline; }
.best-match td { background: var(--color-green-50); }
.name-cell { text-align: left !important; }
.price-cell { font-weight: var(--font-bold); white-space: nowrap; }
.price-higher { color: var(--color-danger); font-weight: var(--font-bold); }
.price-lower { color: var(--color-success); font-weight: var(--font-bold); }
.store-badge { display: inline-block; padding: 3px 8px; border-radius: var(--radius-sm); font-size: var(--text-xs); font-weight: var(--font-bold); }
.store-rozetka { background: var(--color-green-100); color: var(--color-green-700); }
.store-silpo { background: var(--color-warning-bg); color: var(--color-warning); }
.store-epicentr { background: var(--color-info-bg); color: var(--color-info); }
.store-citadel { background: var(--color-danger-light); color: var(--color-danger); }
.no-matches { padding: var(--space-3); color: var(--color-text-secondary); font-style: italic; }

/* Analysis modal */
.analysis-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 900;
}

.analysis-modal {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: var(--space-5);
  max-width: 450px;
  width: 100%;
  margin: var(--space-4);
}

.analysis-modal h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-4);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
  margin-top: var(--space-4);
}

.error-page {
  text-align: center;
  padding: var(--space-16);
  color: var(--color-danger);
}
</style>
