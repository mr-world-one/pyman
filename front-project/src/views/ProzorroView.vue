<template>
  <div class="prozorro">
    <div class="prozorro__inner">
      <div class="page-header">
        <div>
          <h1 class="page-header__title">Аналіз по ID Prozorro</h1>
          <p class="page-header__subtitle">
            Введіть ідентифікатор закупівлі — перевірте позиції за пів хвилини.
          </p>
        </div>
        <a href="#" class="doc-link">
          <AppIcon name="link" :size="14" /> Документація API
        </a>
      </div>

      <!-- Search panel -->
      <div class="search-panel">
        <FormGroup label="ID закупівлі Prozorro">
          <div class="search-row">
            <div class="search-row__input">
              <AppIcon name="search" :size="14" class="search-row__icon" />
              <input
                type="text"
                v-model.trim="tenderId"
                class="app-input app-input--with-icon mono"
                placeholder="UA-2023-01-01-000001-a"
                @keydown.enter="analyzeTender"
              />
            </div>
            <AppButton
              size="lg"
              :disabled="isLoading || selectedStores.length === 0 || !tenderId"
              :loading="isLoading"
              @click="analyzeTender"
            >
              Аналізувати
              <template #icon-right><AppIcon name="arrow-right" :size="14" /></template>
            </AppButton>
          </div>
        </FormGroup>

        <div class="stores-block">
          <StoreSelector v-model="selectedStores" :stores="availableStores" />
        </div>
      </div>

      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <!-- Summary -->
      <div v-if="analytics && analytics.length" class="summary-cards">
        <StatCard label="Товарів у тендері" :value="analytics.length" />
        <StatCard label="Знайдено в магазинах" :value="totalStoreMatches" :meta="coverageLabel" />
        <StatCard
          v-if="hasPricesTender"
          :label="overallSavings >= 0 ? 'Тендер дорожче' : 'Тендер дешевше'"
          :variant="overallSavings >= 0 ? 'danger' : 'brand'"
        >
          <template #value>
            {{ overallSavings >= 0 ? '+' : '' }}{{ overallSavings.toFixed(2) }} ₴
          </template>
        </StatCard>
        <StatCard label="Найвигідніший">
          <template #value>
            <span class="best-store">
              <span class="best-store__dot"></span>
              {{ bestDealStore || '—' }}
            </span>
          </template>
        </StatCard>
      </div>

      <!-- Results -->
      <div v-if="analytics && analytics.length" class="results">
        <div class="results__head">
          <div>
            <h3 class="results__title">Результати порівняння</h3>
            <p class="results__sub">Згруповано по тендерних позиціях</p>
          </div>
          <div class="results__actions">
            <button class="ghost-btn">
              <AppIcon name="filter" :size="14" /> Фільтр
            </button>
            <button class="ghost-btn">
              <AppIcon name="download" :size="14" /> Експорт
            </button>
          </div>
        </div>
        <div class="results__groups">
          <article
            v-for="group in analytics"
            :key="group.name"
            class="price-group"
          >
            <header class="price-group__head">
              <div>
                <h4 class="price-group__title">{{ group.name }}</h4>
                <div class="price-group__meta num">
                  <span v-if="group.tender_price > 0">
                    Тендер: <span class="price-group__meta-val">{{ group.tender_price.toFixed(2) }} ₴</span>
                  </span>
                  <span v-if="group.quantity" class="price-group__meta-sep">·</span>
                  <span v-if="group.quantity">
                    {{ group.quantity }} {{ group.unit_name || 'шт' }}
                  </span>
                  <span v-if="group.total_price" class="price-group__meta-sep">·</span>
                  <span v-if="group.total_price">
                    Всього: <span class="price-group__meta-val">{{ group.total_price.toFixed(2) }} ₴</span>
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
                    <th class="col-num">Ціна/кг</th>
                    <th class="col-num">Різниця</th>
                    <th class="col-num col-pct">%</th>
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
                      <AppBadge v-if="match.is_on_sale" variant="danger">Акція</AppBadge>
                      <span v-if="match.store_weight_g" class="weight-tag num">{{ formatWeight(match.store_weight_g) }}</span>
                    </td>
                    <td class="num col-num">
                      <div>{{ formatPrice(match.effective_price) }} ₴</div>
                      <div v-if="match.is_on_sale && match.original_price" class="old-price num">
                        {{ formatPrice(match.original_price) }} ₴
                      </div>
                    </td>
                    <td class="num col-num">
                      <template v-if="match.price_per_unit">
                        <div>{{ formatPrice(match.price_per_unit) }} ₴</div>
                        <div v-if="match.tender_price_per_unit" class="meta-sub num">
                          тендер: {{ formatPrice(match.tender_price_per_unit) }}
                        </div>
                      </template>
                      <span v-else class="dim">—</span>
                    </td>
                    <td :class="['num col-num', diffClass(match.diff)]">{{ formatDiff(match.diff) }}</td>
                    <td :class="['num col-num col-pct', diffClass(match.diff)]">
                      {{ formatPercent(match.diff, group.tender_price) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="price-group__empty">Не знайдено в жодному магазині</div>
          </article>
        </div>
      </div>

      <div v-else-if="tenderId && !isLoading && !error" class="empty-hint">
        <EmptyState
          icon-name="empty"
          title="Дані відсутні"
          description="Натисніть «Аналізувати», щоб перевірити позиції."
        />
      </div>
    </div>

    <AppLoader v-if="isLoading" :overlay="true" />
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { apiClient } from '@/api/config'
import AppButton from '@/components/AppButton.vue'
import AppLoader from '@/components/AppLoader.vue'
import AppIcon from '@/components/AppIcon.vue'
import AppBadge from '@/components/AppBadge.vue'
import StoreSelector from '@/components/StoreSelector.vue'
import StatCard from '@/components/StatCard.vue'
import FormGroup from '@/components/FormGroup.vue'
import EmptyState from '@/components/EmptyState.vue'

export default {
  name: 'Prozorro',
  components: { AppButton, AppLoader, AppIcon, AppBadge, StoreSelector, StatCard, FormGroup, EmptyState },
  setup() {
    const tenderId = ref('')
    const analytics = ref(null)
    const isLoading = ref(false)
    const error = ref(null)
    const availableStores = [
      { key: 'rozetka', name: 'Rozetka' },
      { key: 'silpo', name: 'Сільпо' },
      { key: 'epicentr', name: 'Епіцентр' },
    ]
    const selectedStores = ref(['rozetka', 'silpo', 'epicentr'])

    const hasPricesTender = computed(() => analytics.value?.some((g) => g.tender_price > 0) ?? false)

    const totalStoreMatches = computed(() =>
      analytics.value?.reduce((sum, g) => sum + g.matches.length, 0) ?? 0,
    )

    const coverageLabel = computed(() => {
      if (!analytics.value?.length) return ''
      const matched = analytics.value.filter((g) => g.matches.length).length
      const pct = Math.round((matched / analytics.value.length) * 100)
      return `${pct}% покриття`
    })

    const overallSavings = computed(() => {
      if (!analytics.value) return 0
      return analytics.value.reduce(
        (total, g) => g.matches.reduce((s, m) => (m.diff !== null ? s + m.diff : s), total),
        0,
      )
    })

    const bestDealStore = computed(() => {
      if (!analytics.value) return null
      const totals = {}
      for (const g of analytics.value) {
        for (const m of g.matches) {
          if (m.effective_price !== null) {
            totals[m.store_name] = (totals[m.store_name] ?? 0) + m.effective_price
          }
        }
      }
      return Object.entries(totals).reduce(
        (best, [name, total]) => (total < best[1] ? [name, total] : best),
        [null, Infinity],
      )[0]
    })

    const processMatchedItems = (matchedItems) => {
      if (!matchedItems?.length) return []
      return matchedItems.map((group) => {
        const tender = group.tender_item || {}
        const tenderPrice = parseFloat(tender.unit_price) || 0
        const matches = (group.matches || []).map((item) => {
          const effectivePrice = item.price_on_sale ? parseFloat(item.price_on_sale) : parseFloat(item.price) || null
          return {
            title: item.title || '—',
            store: item.store || '',
            store_name: item.store_name || '—',
            url: item.url || null,
            effective_price: effectivePrice,
            original_price: item.price_on_sale ? parseFloat(item.price) : null,
            is_on_sale: !!item.price_on_sale && item.price_on_sale !== item.price,
            diff: (effectivePrice !== null && tenderPrice > 0) ? tenderPrice - effectivePrice : null,
            store_weight_g: item.store_weight_g || null,
            price_per_unit: item.price_per_unit || null,
            tender_price_per_unit: item.tender_price_per_unit || null,
          }
        }).sort((a, b) => (a.effective_price ?? Infinity) - (b.effective_price ?? Infinity))

        return {
          name: tender.name || '',
          tender_price: tenderPrice,
          quantity: tender.quantity || null,
          unit_name: tender.unit_name || null,
          total_price: tender.total_price ? parseFloat(tender.total_price) : null,
          matches,
        }
      }).filter((item) => item.name)
    }

    const analyzeTender = async () => {
      if (!tenderId.value) return
      isLoading.value = true
      error.value = null
      analytics.value = null
      try {
        const response = await apiClient.get(`/search-tender/${tenderId.value}`, {
          params: { stores: selectedStores.value.join(',') },
        })
        analytics.value = processMatchedItems(response.data.matched_items)
      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Помилка сервера'
      } finally {
        isLoading.value = false
      }
    }

    const formatPrice = (val) => (val == null ? 'Н/Д' : Number(val).toFixed(2))
    const formatWeight = (g) => {
      if (!g) return ''
      return g >= 1000 ? (g / 1000).toFixed(g % 1000 === 0 ? 0 : 1) + ' кг' : g + ' г'
    }
    const formatDiff = (diff) => diff === null ? '—' : (diff >= 0 ? '+' : '−') + Math.abs(diff).toFixed(2) + ' ₴'
    const formatPercent = (diff, base) => {
      if (diff === null || !base) return '—'
      const pct = (diff / base) * 100
      return (pct >= 0 ? '+' : '') + pct.toFixed(1) + '%'
    }
    const diffClass = (diff) =>
      diff === null ? '' : diff > 0 ? 'price-higher' : diff < 0 ? 'price-lower' : 'price-equal'

    return {
      tenderId, analytics, isLoading, error,
      availableStores, selectedStores,
      hasPricesTender, totalStoreMatches, overallSavings, bestDealStore, coverageLabel,
      analyzeTender,
      formatPrice, formatWeight, formatDiff, formatPercent, diffClass,
    }
  },
}
</script>

<style scoped>
.prozorro {
  padding: calc(var(--header-height) + var(--space-8)) var(--space-6) var(--space-12);
}

.prozorro__inner {
  max-width: var(--container-max-width);
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-4);
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

.doc-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.doc-link:hover { color: var(--color-heading); }

.search-panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-soft);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.search-row {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.search-row__input {
  position: relative;
  flex: 1;
  min-width: 240px;
}

.search-row__icon {
  position: absolute;
  left: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-tertiary);
  pointer-events: none;
}

.app-input--with-icon { padding-left: 34px; }

.stores-block {
  padding-top: var(--space-3);
  border-top: 1px dashed var(--color-border);
}

/* Summary */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.best-store {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.best-store__dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-info);
}

/* Results */
.results {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}

.results__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.results__title {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
}

.results__sub {
  margin-top: 2px;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.results__actions { display: flex; gap: var(--space-2); }

.ghost-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 var(--space-3);
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  font-family: inherit;
  font-size: var(--text-sm);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
}

.ghost-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }

.results__groups {
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

/* Price group */
.price-group {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.price-group__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  gap: var(--space-3);
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

/* Table */
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
}

.data-table thead th.col-num { text-align: right; }
.data-table thead th.col-store { width: 160px; }
.data-table thead th.col-pct { width: 80px; }

.data-table tbody td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--color-border);
  vertical-align: top;
  color: var(--color-text);
}

.data-table tbody td.col-num { text-align: right; font-variant-numeric: tabular-nums; }

.data-table tr.row-hover:hover td { background: var(--color-bg-subtle); }

.data-table tr.best-row td,
.data-table tr.best-match td { background: var(--color-green-50); }

.name-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}

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

.weight-tag {
  display: inline-flex;
  align-items: center;
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  background: var(--color-info-bg);
  color: var(--color-info);
  font-size: 11px;
  font-weight: var(--font-semibold);
}

.old-price {
  font-size: 11px;
  color: var(--color-text-secondary);
  text-decoration: line-through;
  margin-top: 2px;
}

.meta-sub {
  font-size: 11px;
  color: var(--color-text-secondary);
  margin-top: 2px;
}

.dim { color: var(--color-text-tertiary); }

.price-higher { color: var(--color-danger); font-weight: var(--font-medium); }
.price-lower { color: var(--color-primary); font-weight: var(--font-medium); }
.price-equal { color: var(--color-text-secondary); }

.empty-hint { margin-top: var(--space-6); }

@media (max-width: 640px) {
  .prozorro { padding: calc(var(--header-height) + var(--space-6)) var(--space-4) var(--space-10); }
}
</style>
