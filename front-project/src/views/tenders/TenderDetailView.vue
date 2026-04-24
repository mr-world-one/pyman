<template>
  <div class="tender-detail">
    <div class="tender-detail__inner" v-if="tender">
      <!-- Breadcrumb -->
      <button class="breadcrumb" type="button" @click="$router.push('/tenders')">
        <AppIcon name="arrow-left" :size="14" /> До списку
      </button>

      <!-- Header row -->
      <div class="detail-header">
        <div class="detail-header__left">
          <div class="detail-header__badges">
            <TenderTypeBadge :type="tender.tender_type" />
            <AppBadge :variant="statusVariant" :show-dot="tender.status === 'active'">
              {{ statusLabel }}
            </AppBadge>
          </div>
          <h1 class="detail-header__title">{{ tender.title }}</h1>
          <div class="detail-meta">
            <span class="detail-meta__id mono">{{ tender.prozorro_id }}</span>
            <span v-if="tender.customer_name" class="detail-meta__dot">·</span>
            <span v-if="tender.customer_name">{{ tender.customer_name }}</span>
            <span v-if="tender.region" class="detail-meta__dot">·</span>
            <span v-if="tender.region">{{ tender.region }}</span>
            <span class="detail-meta__dot">·</span>
            <span>{{ formatDate(tender.created_at) }}</span>
          </div>
        </div>
        <div class="detail-header__actions">
          <AppButton
            v-if="tender.tender_type !== 'service'"
            variant="secondary"
            :disabled="analyzing"
            @click="showAnalysis = true"
          >
            <template #icon-left><AppIcon name="bar" :size="14" /></template>
            {{ analyzing ? 'Аналізуємо…' : 'Аналіз цін' }}
          </AppButton>
          <AppButton
            variant="secondary"
            :disabled="analyzingRisks"
            @click="runRiskAnalysis"
          >
            <template #icon-left><AppIcon name="shield" :size="14" /></template>
            {{ analyzingRisks ? 'Перевіряємо…' : 'Аналіз ризиків' }}
          </AppButton>
          <AppButton variant="danger" size="sm" @click="handleDelete">
            <template #icon-left><AppIcon name="trash" :size="14" /></template>
            Видалити
          </AppButton>
        </div>
      </div>

      <p v-if="tender.description" class="detail-description">{{ tender.description }}</p>

      <!-- Stat cards -->
      <div class="detail-stats">
        <StatCard
          label="Загальна сума"
          :value="`${formatPrice(tender.total_amount)} ${tender.currency || '₴'}`"
          :meta="`${tender.items?.length || 0} позицій`"
        />
        <StatCard
          v-if="tender.expected_cost"
          label="Очікувана вартість"
          :value="`${formatPrice(tender.expected_cost)} ${tender.currency || '₴'}`"
        />
        <StatCard
          label="Позицій"
          :value="tender.items?.length || 0"
        />
        <StatCard
          v-if="riskResult"
          :label="'Рівень ризику'"
          :variant="riskVariant"
        >
          <template #value>
            <div class="risk-value">
              <span :class="['risk-dot', `risk-${riskResult.risk_level}`]"></span>
              {{ riskResult.risk_score }}/100
            </div>
          </template>
          <template #meta>
            <div class="risk-pips">
              <span :class="['risk-pip', riskResult.risk_level !== 'low' ? `risk-${riskResult.risk_level}` : 'risk-low']"></span>
              <span :class="['risk-pip', riskResult.risk_level === 'high' ? 'risk-high' : (riskResult.risk_level === 'medium' ? 'risk-medium' : 'risk-off')]"></span>
              <span :class="['risk-pip', riskResult.risk_level === 'high' ? 'risk-high' : 'risk-off']"></span>
            </div>
          </template>
        </StatCard>
      </div>

      <!-- Tabs -->
      <AppTabs v-model="activeTab" :tabs="computedTabs">
        <!-- Items tab -->
        <section v-if="activeTab === 'items'" class="panel">
          <ProductTenderDetail v-if="tender.tender_type === 'product'" :items="tender.items" />
          <ServiceTenderDetail v-if="tender.tender_type === 'service'" :items="tender.items" />
          <WorkTenderDetail v-if="tender.tender_type === 'work'" :items="tender.items" />
        </section>

        <!-- Prices analysis -->
        <section v-if="activeTab === 'prices'" class="panel">
          <div v-if="!analysisResults" class="tab-empty">
            <EmptyState
              icon-name="bar"
              title="Аналіз цін ще не запускався"
              description='Натисніть "Аналіз цін", щоб порівняти позиції з магазинами.'
            >
              <AppButton @click="showAnalysis = true">Запустити аналіз</AppButton>
            </EmptyState>
          </div>
          <div v-else class="price-groups">
            <article
              v-for="group in processedAnalysis"
              :key="group.name"
              class="price-group"
            >
              <header class="price-group__head">
                <div>
                  <h3 class="price-group__title">{{ group.name }}</h3>
                  <div class="price-group__meta num">
                    Кількість: <span class="price-group__meta-val">{{ group.quantity }}</span>
                    <span v-if="group.tender_price" class="price-group__meta-sep">·</span>
                    <span v-if="group.tender_price">
                      Тендерна ціна:
                      <span class="price-group__meta-val">{{ formatPrice(group.tender_price) }} ₴</span>
                    </span>
                  </div>
                </div>
                <AppBadge variant="slate">{{ group.matches.length }} пропозицій</AppBadge>
              </header>
              <div v-if="group.matches.length" class="table-responsive">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th class="col-store">Магазин</th>
                      <th>Назва в магазині</th>
                      <th class="col-num">Ціна</th>
                      <th class="col-num">Різниця</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(match, idx) in group.matches"
                      :key="idx"
                      :class="['row-hover', { 'best-row best-match': idx === 0 }]"
                    >
                      <td>
                        <span class="store-cell">
                          <span :class="['store-dot', `store-${match.store}`]"></span>
                          {{ match.store_name }}
                        </span>
                        <div v-if="idx === 0" class="store-cell__best">Найкраща пропозиція</div>
                      </td>
                      <td class="name-cell">
                        <a v-if="match.url" :href="match.url" target="_blank" rel="noopener">{{ match.title }}</a>
                        <span v-else>{{ match.title }}</span>
                      </td>
                      <td class="num col-num">{{ formatPrice(match.effective_price) }} ₴</td>
                      <td
                        :class="[
                          'num col-num',
                          match.diff > 0 ? 'price-higher' : match.diff < 0 ? 'price-lower' : 'price-equal',
                        ]"
                      >
                        <template v-if="match.diff != null">
                          {{ match.diff >= 0 ? '+' : '−' }}{{ formatPrice(Math.abs(match.diff)) }} ₴
                        </template>
                        <template v-else>—</template>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="price-group__empty">Не знайдено в магазинах</div>
            </article>
          </div>
        </section>

        <!-- Analytics -->
        <section v-if="activeTab === 'analytics'" class="panel analytics-panel">
          <div class="analytics-head">
            <div>
              <h3 class="analytics-head__title">Аналітика цін</h3>
              <p class="analytics-head__sub">Тендер vs середній ринок</p>
            </div>
            <label class="period-select">
              <span>Період</span>
              <select v-model.number="historyDays" @change="loadPriceHistory">
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
        </section>

        <!-- Risks -->
        <section v-if="activeTab === 'risks'" class="panel">
          <div v-if="riskResult" class="risks">
            <div class="risk-score">
              <div :class="['risk-score__orb', `risk-${riskResult.risk_level}`]">
                <span class="num">{{ riskResult.risk_score }}</span>
                <small>/ 100</small>
              </div>
              <div>
                <h3 class="risk-score__title">
                  {{ riskLabel }}
                </h3>
                <div class="risk-score__sub num">
                  Ціна: <strong>{{ riskResult.price_risk_score }}</strong>/50 ·
                  Вимоги: <strong>{{ riskResult.discriminatory_risk_score }}</strong>/50
                </div>
              </div>
            </div>

            <ul class="risk-list">
              <li
                v-for="(pd, idx) in (riskResult.breakdown?.price_deviations || [])"
                :key="'pd-' + idx"
                class="risk-item"
              >
                <span :class="['risk-item__icon', `risk-${pd.risk_level}`]">
                  <AppIcon name="alert" :size="14" />
                </span>
                <div class="risk-item__body">
                  <div class="risk-item__head">
                    <span class="risk-item__name">{{ pd.item_name }}</span>
                    <AppBadge :variant="riskBadgeVariant(pd.risk_level)">
                      {{ riskLevelLabel(pd.risk_level) }}
                    </AppBadge>
                  </div>
                  <div v-if="pd.reason" class="risk-item__desc">{{ pd.reason }}</div>
                  <div class="risk-item__stats num">
                    <span v-if="pd.tender_price">Тендер: {{ formatPrice(pd.tender_price) }} ₴</span>
                    <span v-if="pd.median_market_price">Ринок: {{ formatPrice(pd.median_market_price) }} ₴</span>
                    <span v-if="pd.deviation_pct != null">Відхилення: {{ pd.deviation_pct }}%</span>
                  </div>
                </div>
              </li>
              <li
                v-for="(dr, idx) in (riskResult.breakdown?.discriminatory_analysis?.discriminatory_requirements || [])"
                :key="'dr-' + idx"
                class="risk-item"
              >
                <span :class="['risk-item__icon', `risk-${dr.severity}`]">
                  <AppIcon name="alert" :size="14" />
                </span>
                <div class="risk-item__body">
                  <div class="risk-item__head">
                    <span class="risk-item__name">{{ dr.type }}</span>
                    <AppBadge :variant="riskBadgeVariant(dr.severity)">
                      {{ riskLevelLabel(dr.severity) }}
                    </AppBadge>
                  </div>
                  <blockquote v-if="dr.text" class="risk-item__quote">{{ dr.text }}</blockquote>
                  <div v-if="dr.explanation" class="risk-item__desc">{{ dr.explanation }}</div>
                </div>
              </li>
            </ul>
          </div>
          <EmptyState
            v-else
            icon-name="shield"
            title="Аналіз ризиків ще не запускався"
            description='Натисніть "Аналіз ризиків", щоб запустити перевірку.'
          >
            <AppButton @click="runRiskAnalysis">Перевірити</AppButton>
          </EmptyState>
        </section>
      </AppTabs>

      <!-- Store selector modal -->
      <AppModal v-if="showAnalysis" v-model="showAnalysis" title="Вибір магазинів для аналізу">
        <StoreSelector v-model="selectedStores" :stores="availableStores" />
        <template #footer>
          <AppButton variant="secondary" @click="showAnalysis = false">Скасувати</AppButton>
          <AppButton :disabled="selectedStores.length === 0 || analyzing" :loading="analyzing" @click="runAnalysis">
            Запустити аналіз
          </AppButton>
        </template>
      </AppModal>
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
import AppIcon from '@/components/AppIcon.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppTabs from '@/components/AppTabs.vue'
import AppModal from '@/components/AppModal.vue'
import StatCard from '@/components/StatCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import StoreSelector from '@/components/StoreSelector.vue'
import TenderTypeBadge from '@/components/tenders/TenderTypeBadge.vue'
import ProductTenderDetail from '@/components/tenders/details/ProductTenderDetail.vue'
import ServiceTenderDetail from '@/components/tenders/details/ServiceTenderDetail.vue'
import WorkTenderDetail from '@/components/tenders/details/WorkTenderDetail.vue'
import PriceTrendChart from '@/components/tenders/PriceTrendChart.vue'

const STATUS_LABELS = { active: 'Активний', closed: 'Завершений', cancelled: 'Скасований' }
const STATUS_VARIANTS = { active: 'brand', closed: 'slate', cancelled: 'danger' }
const RISK_LABELS = { high: 'Високий ризик', medium: 'Середній ризик', low: 'Низький ризик' }
const RISK_BADGE = { high: 'danger', medium: 'warn', low: 'info' }

export default {
  name: 'TenderDetailView',
  components: {
    AppButton, AppLoader, AppIcon, AppBadge, AppTabs, AppModal, StatCard, EmptyState,
    StoreSelector, TenderTypeBadge,
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
    ]

    const activeTab = ref('items')
    const computedTabs = computed(() => [
      { key: 'items', label: 'Позиції', count: tender.value?.items?.length },
      { key: 'prices', label: 'Аналіз цін' },
      { key: 'analytics', label: 'Аналітика' },
      { key: 'risks', label: 'Ризики' },
    ])

    const priceHistory = ref(null)
    const loadingHistory = ref(false)
    const historyDays = ref(30)

    const riskResult = ref(null)
    const analyzingRisks = ref(false)

    const statusLabel = computed(() => STATUS_LABELS[tender.value?.status] || tender.value?.status)
    const statusVariant = computed(() => STATUS_VARIANTS[tender.value?.status] || 'slate')
    const riskLabel = computed(() => RISK_LABELS[riskResult.value?.risk_level] || '')
    const riskVariant = computed(() => {
      if (!riskResult.value) return null
      return riskResult.value.risk_level === 'high' ? 'danger'
        : riskResult.value.risk_level === 'medium' ? 'warn'
        : 'brand'
    })

    onMounted(() => {
      const id = Number(route.params.id)
      store.fetchTender(id)
      const cachedAnalysis = store.getCachedAnalysis(id)
      if (cachedAnalysis) analysisResults.value = cachedAnalysis
      const cachedRisk = store.getCachedRisk(id)
      if (cachedRisk) riskResult.value = cachedRisk
      const cachedHistory = store.getCachedPriceHistory(id)
      if (cachedHistory) priceHistory.value = cachedHistory
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
        loadPriceHistory()
      } catch { /* error in store */ } finally {
        analyzing.value = false
      }
    }

    const loadPriceHistory = async () => {
      loadingHistory.value = true
      try {
        const data = await store.fetchPriceHistory(Number(route.params.id), historyDays.value)
        priceHistory.value = data
      } catch { /* error in store */ } finally {
        loadingHistory.value = false
      }
    }

    const runRiskAnalysis = async () => {
      analyzingRisks.value = true
      try {
        const result = await store.analyzeRisks(Number(route.params.id), selectedStores.value)
        if (result?.risk_details) riskResult.value = result.risk_details
        activeTab.value = 'risks'
      } catch { /* error in store */ } finally {
        analyzingRisks.value = false
      }
    }

    const handleDelete = async () => {
      if (!confirm('Видалити цей тендер?')) return
      try {
        await store.deleteTender(Number(route.params.id))
        router.push('/tenders')
      } catch { /* error in store */ }
    }

    const formatPrice = (val) => {
      if (val == null) return '—'
      return Number(val).toLocaleString('uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('uk-UA')
    }

    const riskLevelLabel = (lvl) => RISK_LABELS[lvl]?.replace(' ризик', '') || lvl
    const riskBadgeVariant = (lvl) => RISK_BADGE[lvl] || 'slate'

    return {
      store, tender, showAnalysis, analyzing, analysisResults, selectedStores,
      availableStores, processedAnalysis, activeTab, computedTabs,
      priceHistory, loadingHistory, historyDays, loadPriceHistory,
      riskResult, analyzingRisks, runRiskAnalysis,
      runAnalysis, handleDelete, formatPrice, formatDate,
      statusLabel, statusVariant, riskLabel, riskVariant,
      riskLevelLabel, riskBadgeVariant,
    }
  },
}
</script>

<style scoped>
.tender-detail {
  padding: calc(var(--header-height) + var(--space-8)) var(--space-6) var(--space-12);
}

.tender-detail__inner {
  max-width: var(--container-max-width);
  margin: 0 auto;
}

.breadcrumb {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  margin-bottom: var(--space-3);
}

.breadcrumb:hover { color: var(--color-heading); }

.detail-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.detail-header__left { min-width: 0; flex: 1; }

.detail-header__badges {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
  margin-bottom: var(--space-3);
}

.detail-header__title {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
  color: var(--color-heading);
  max-width: 880px;
  line-height: 1.2;
}

.detail-meta {
  margin-top: var(--space-3);
  display: flex;
  flex-wrap: wrap;
  gap: 6px 10px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  align-items: center;
}

.detail-meta__id {
  color: var(--color-text);
  font-size: var(--text-sm);
}

.detail-meta__dot { color: var(--color-text-tertiary); }

.detail-header__actions {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.detail-description {
  margin-top: var(--space-5);
  max-width: 880px;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: 1.65;
}

.detail-stats {
  margin-top: var(--space-6);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

/* Risk value inside StatCard */
.risk-value {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.risk-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.risk-high { background: var(--color-danger); }
.risk-medium { background: var(--color-warning); }
.risk-low { background: var(--color-primary); }
.risk-off { background: var(--color-border); }

.risk-pips {
  display: flex;
  gap: 4px;
  margin-top: 6px;
}

.risk-pip {
  flex: 1;
  height: 4px;
  border-radius: 2px;
  background: var(--color-border);
}

.risk-pip.risk-high { background: var(--color-danger); }
.risk-pip.risk-medium { background: var(--color-warning); }
.risk-pip.risk-low { background: var(--color-primary); }

/* Panels */
.panel {
  padding: var(--space-5);
}

.tab-empty { padding: var(--space-5); }

/* Price groups */
.price-groups {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.price-group {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  overflow: hidden;
}

.price-group__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.price-group__title {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
  letter-spacing: 0;
}

.price-group__meta {
  margin-top: 2px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.price-group__meta-val { color: var(--color-text); }
.price-group__meta-sep { margin: 0 6px; color: var(--color-text-tertiary); }

.price-group__empty {
  padding: var(--space-5);
  color: var(--color-text-secondary);
  font-style: italic;
  font-size: var(--text-sm);
}

/* Data table */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}

.data-table thead th {
  background: var(--color-bg-subtle);
  color: var(--color-text-secondary);
  padding: 10px 14px;
  text-align: left;
  font-size: 11px;
  font-weight: var(--font-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 1;
}

.data-table thead th.col-num { text-align: right; }
.data-table thead th.col-store { width: 160px; }

.data-table tbody td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  vertical-align: top;
}

.data-table tbody td.col-num { text-align: right; font-variant-numeric: tabular-nums; }

.data-table tr.row-hover:hover td { background: var(--color-bg-subtle); }

.data-table tr.best-row td,
.data-table tr.best-match td { background: var(--color-green-50); }

.name-cell a { color: var(--color-primary); }
.name-cell a:hover { text-decoration: underline; }

.store-cell {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: var(--font-medium);
}

.store-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-slate-400);
}

.store-dot.store-rozetka { background: var(--color-info); }
.store-dot.store-silpo { background: var(--color-primary); }
.store-dot.store-epicentr { background: var(--color-warning); }

.store-cell__best {
  margin-top: 2px;
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-primary);
  font-weight: var(--font-semibold);
}

.price-higher {
  color: var(--color-danger);
  font-weight: var(--font-medium);
}

.price-lower {
  color: var(--color-primary);
  font-weight: var(--font-medium);
}

.price-equal { color: var(--color-text-secondary); }

/* Analytics */
.analytics-panel { padding: var(--space-5); }

.analytics-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.analytics-head__title {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
}

.analytics-head__sub {
  margin-top: 2px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.period-select {
  display: inline-flex;
  flex-direction: column;
  gap: 4px;
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--color-text);
}

.period-select select {
  height: 32px;
  padding: 0 var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  font-size: var(--text-sm);
  font-family: inherit;
  color: var(--color-text);
}

/* Risks */
.risks { display: flex; flex-direction: column; gap: var(--space-5); }

.risk-score {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
}

.risk-score__orb {
  display: inline-flex;
  align-items: baseline;
  justify-content: center;
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-lg);
  background: var(--color-bg-subtle);
  font-size: var(--text-4xl);
  font-weight: var(--font-semibold);
  color: var(--color-heading);
  font-variant-numeric: tabular-nums;
}

.risk-score__orb.risk-high { color: var(--color-danger); background: var(--color-red-50); }
.risk-score__orb.risk-medium { color: var(--color-warning); background: var(--color-warning-bg); }
.risk-score__orb.risk-low { color: var(--color-primary); background: var(--color-green-50); }

.risk-score__orb small {
  margin-left: 4px;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.risk-score__title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
}

.risk-score__sub {
  margin-top: 4px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.risk-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.risk-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-5);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
}

.risk-item:last-child { border-bottom: none; }

.risk-item__icon {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
}

.risk-item__icon.risk-high { color: var(--color-danger); background: var(--color-red-50); border-color: var(--color-red-100); }
.risk-item__icon.risk-medium { color: var(--color-warning); background: var(--color-warning-bg); border-color: var(--color-warning-border); }
.risk-item__icon.risk-low { color: var(--color-info); background: var(--color-info-bg); border-color: var(--color-info-border); }

.risk-item__body { flex: 1; min-width: 0; }

.risk-item__head {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.risk-item__name {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
}

.risk-item__desc {
  margin-top: 6px;
  font-size: 13.5px;
  color: var(--color-text-secondary);
  line-height: 1.55;
}

.risk-item__quote {
  margin-top: 8px;
  padding: var(--space-3) var(--space-4);
  border-left: 2px solid var(--color-border);
  font-size: var(--text-sm);
  color: var(--color-text);
  font-style: italic;
  background: var(--color-bg-subtle);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

.risk-item__stats {
  margin-top: 8px;
  display: flex;
  gap: var(--space-4);
  flex-wrap: wrap;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* Error page */
.error-page {
  text-align: center;
  padding: var(--space-16);
  color: var(--color-danger);
}

.error-page p { margin-bottom: var(--space-4); }

@media (max-width: 640px) {
  .tender-detail { padding: calc(var(--header-height) + var(--space-6)) var(--space-4) var(--space-10); }
  .detail-header { flex-direction: column; }
  .detail-header__actions { width: 100%; }
  .risk-score { flex-direction: column; align-items: flex-start; }
  .panel { padding: var(--space-4); }
}
</style>
