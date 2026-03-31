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
          <AppButton variant="ghost" @click="runRiskAnalysis" :disabled="analyzingRisks">
            {{ analyzingRisks ? 'Перевіряємо...' : 'Аналіз ризиків' }}
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
        <div class="summary-card" v-if="riskResult">
          <div class="summary-label">Рівень ризику</div>
          <div class="summary-value" :class="'risk-' + riskResult.risk_level">
            {{ riskResult.risk_score }}/100
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="tab-btn"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Tab: Items -->
      <div v-if="activeTab === 'items'" class="items-section">
        <ProductTenderDetail v-if="tender.tender_type === 'product'" :items="tender.items" />
        <ServiceTenderDetail v-if="tender.tender_type === 'service'" :items="tender.items" />
        <WorkTenderDetail v-if="tender.tender_type === 'work'" :items="tender.items" />
      </div>

      <!-- Tab: Price Analysis results -->
      <div v-if="activeTab === 'prices' && analysisResults" class="analysis-section">
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
      <div v-if="activeTab === 'prices' && !analysisResults" class="tab-empty">
        <p>Натисніть "Аналіз цін", щоб запустити порівняння з магазинами</p>
      </div>

      <!-- Tab: Price Analytics (Charts) -->
      <div v-if="activeTab === 'analytics'" class="analytics-section">
        <h2>Аналітика цін</h2>
        <div class="analytics-controls">
          <label>
            Період:
            <select v-model="historyDays" @change="loadPriceHistory">
              <option :value="7">7 днів</option>
              <option :value="30">30 днів</option>
              <option :value="90">90 днів</option>
            </select>
          </label>
        </div>
        <PriceTrendChart
          :tender-id="tender.id"
          :price-history="priceHistory"
          :loading="loadingHistory"
        />
      </div>

      <!-- Tab: Risk Analysis -->
      <div v-if="activeTab === 'risks'" class="risk-section">
        <h2>Аналіз корупційних ризиків</h2>
        <div v-if="riskResult" class="risk-results">
          <div class="risk-score-card" :class="'risk-' + riskResult.risk_level">
            <div class="risk-score-number">{{ riskResult.risk_score }}</div>
            <div class="risk-score-label">/ 100</div>
            <div class="risk-level-text">
              {{ riskResult.risk_level === 'high' ? 'Високий ризик' : riskResult.risk_level === 'medium' ? 'Середній ризик' : 'Низький ризик' }}
            </div>
          </div>

          <div class="risk-breakdown">
            <div class="risk-breakdown-item">
              <span class="breakdown-label">Цінові відхилення:</span>
              <span class="breakdown-value">{{ riskResult.price_risk_score }}/50</span>
            </div>
            <div class="risk-breakdown-item">
              <span class="breakdown-label">Дискримінаційні вимоги:</span>
              <span class="breakdown-value">{{ riskResult.discriminatory_risk_score }}/50</span>
            </div>
          </div>

          <!-- Price deviations -->
          <div v-if="riskResult.breakdown?.price_deviations?.length" class="risk-detail-section">
            <h3>Цінові відхилення</h3>
            <div v-for="(pd, idx) in riskResult.breakdown.price_deviations" :key="'pd-' + idx" class="risk-finding">
              <div class="finding-header">
                <span class="finding-name">{{ pd.item_name }}</span>
                <span class="risk-badge" :class="'risk-' + pd.risk_level">{{ pd.risk_level }}</span>
              </div>
              <div class="finding-details">
                <span v-if="pd.tender_price">Тендер: {{ formatPrice(pd.tender_price) }} грн</span>
                <span v-if="pd.median_market_price"> | Ринок: {{ formatPrice(pd.median_market_price) }} грн</span>
                <span v-if="pd.deviation_pct != null"> | Відхилення: {{ pd.deviation_pct }}%</span>
              </div>
              <div class="finding-reason">{{ pd.reason }}</div>
            </div>
          </div>

          <!-- Discriminatory requirements -->
          <div v-if="riskResult.breakdown?.discriminatory_analysis?.discriminatory_requirements?.length" class="risk-detail-section">
            <h3>Дискримінаційні вимоги</h3>
            <div v-for="(dr, idx) in riskResult.breakdown.discriminatory_analysis.discriminatory_requirements" :key="'dr-' + idx" class="risk-finding">
              <div class="finding-header">
                <span class="risk-badge" :class="'risk-' + dr.severity">{{ dr.severity }}</span>
                <span class="finding-type">{{ dr.type }}</span>
              </div>
              <blockquote class="finding-quote">{{ dr.text }}</blockquote>
              <div class="finding-reason">{{ dr.explanation }}</div>
            </div>
          </div>
        </div>
        <div v-else class="tab-empty">
          <p>Натисніть "Аналіз ризиків", щоб запустити перевірку</p>
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

    <AppLoader v-if="store.loading && !tender" :overlay="true" />

    <div v-if="store.error && !tender" class="error-page">
      <p>{{ store.error }}</p>
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
import PriceTrendChart from '@/components/tenders/PriceTrendChart.vue'

export default {
  name: 'TenderDetailView',
  components: {
    AppButton, AppLoader, StoreSelector, TenderTypeBadge,
    ProductTenderDetail, ServiceTenderDetail, WorkTenderDetail,
    PriceTrendChart,
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const store = useTendersStore()

    const tender = computed(() => store.currentTender)
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

    // Tabs
    const activeTab = ref('items')
    const tabs = [
      { key: 'items', label: 'Позиції' },
      { key: 'prices', label: 'Порівняння цін' },
      { key: 'analytics', label: 'Аналітика цін' },
      { key: 'risks', label: 'Ризики' },
    ]

    // Price history
    const priceHistory = ref(null)
    const loadingHistory = ref(false)
    const historyDays = ref(30)

    // Risk analysis
    const riskResult = ref(null)
    const analyzingRisks = ref(false)

    onMounted(() => {
      const id = Number(route.params.id)
      store.fetchTender(id)

      // Restore cached results
      const cachedAnalysis = store.getCachedAnalysis(id)
      if (cachedAnalysis) {
        analysisResults.value = cachedAnalysis
      }
      const cachedRisk = store.getCachedRisk(id)
      if (cachedRisk) {
        riskResult.value = cachedRisk
      }
      const cachedHistory = store.getCachedPriceHistory(id)
      if (cachedHistory) {
        priceHistory.value = cachedHistory
      }
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
        activeTab.value = 'prices'
        // Also load price history after analysis
        loadPriceHistory()
      } catch {
        // error is handled by store
      } finally {
        analyzing.value = false
      }
    }

    const loadPriceHistory = async () => {
      loadingHistory.value = true
      try {
        const data = await store.fetchPriceHistory(Number(route.params.id), historyDays.value)
        priceHistory.value = data
      } catch {
        // error is handled by store
      } finally {
        loadingHistory.value = false
      }
    }

    const runRiskAnalysis = async () => {
      analyzingRisks.value = true
      try {
        const result = await store.analyzeRisks(Number(route.params.id), selectedStores.value)
        if (result?.risk_details) {
          riskResult.value = result.risk_details
        }
        activeTab.value = 'risks'
      } catch {
        // error is handled by store
      } finally {
        analyzingRisks.value = false
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
      availableStores, processedAnalysis, activeTab, tabs,
      priceHistory, loadingHistory, historyDays, loadPriceHistory,
      riskResult, analyzingRisks, runRiskAnalysis,
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

/* Tabs */
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid var(--color-border);
  margin-bottom: var(--space-6);
}

.tab-btn {
  padding: var(--space-2) var(--space-4);
  border: none;
  background: none;
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-secondary);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: var(--color-heading);
}

.tab-btn.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.tab-empty {
  padding: var(--space-8);
  text-align: center;
  color: var(--color-text-secondary);
  font-style: italic;
}

/* Analytics */
.analytics-section h2, .risk-section h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-4);
}

.analytics-controls {
  margin-bottom: var(--space-4);
}

.analytics-controls select {
  padding: 0.3rem 0.5rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  font-size: var(--text-sm);
}

/* Risk analysis */
.risk-score-card {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-4);
  background: var(--color-surface);
  border: 2px solid var(--color-border);
}

.risk-score-card.risk-high {
  border-color: var(--color-danger);
  background: var(--color-danger-light);
}

.risk-score-card.risk-medium {
  border-color: var(--color-warning);
  background: var(--color-warning-bg);
}

.risk-score-card.risk-low {
  border-color: var(--color-success);
  background: var(--color-green-50);
}

.risk-score-number {
  font-size: 3rem;
  font-weight: var(--font-bold);
  line-height: 1;
}

.risk-score-label {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
}

.risk-level-text {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  margin-left: auto;
}

.risk-breakdown {
  display: flex;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.risk-breakdown-item {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  flex: 1;
}

.breakdown-label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.breakdown-value {
  font-weight: var(--font-bold);
  margin-left: var(--space-2);
}

.risk-detail-section {
  margin-top: var(--space-6);
}

.risk-detail-section h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-3);
}

.risk-finding {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  margin-bottom: var(--space-2);
}

.finding-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-1);
}

.finding-name {
  font-weight: var(--font-semibold);
  color: var(--color-heading);
}

.finding-type {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  text-transform: uppercase;
}

.risk-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  text-transform: uppercase;
}

.risk-badge.risk-high, .risk-high .risk-score-number { color: var(--color-danger); }
.risk-badge.risk-medium, .risk-medium .risk-score-number { color: var(--color-warning); }
.risk-badge.risk-low, .risk-low .risk-score-number { color: var(--color-success); }

.risk-badge.risk-high { background: var(--color-danger-light); }
.risk-badge.risk-medium { background: var(--color-warning-bg); }
.risk-badge.risk-low { background: var(--color-green-50); }

.finding-details {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.finding-reason {
  font-size: var(--text-sm);
  color: var(--color-text);
  margin-top: var(--space-1);
}

.finding-quote {
  margin: var(--space-2) 0;
  padding: var(--space-2) var(--space-3);
  border-left: 3px solid var(--color-warning);
  background: var(--color-warning-bg);
  font-size: var(--text-sm);
  font-style: italic;
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
