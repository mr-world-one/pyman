<template>
  <div class="tender-page">
    <div class="tender-container">
      <h1>Пошук тендеру</h1>
      <p>Введіть ID Prozorro-тендеру для аналізу:</p>

      <form @submit.prevent="analyzeTender">
        <input
          type="text"
          v-model.trim="tenderId"
          placeholder="Введіть ID тендеру (наприклад, UA-2023-01-01-000001-a)"
          required
        />
        <StoreSelector v-model="selectedStores" :stores="availableStores" />
        <AppButton
          type="submit"
          size="lg"
          :disabled="isLoading || selectedStores.length === 0"
          style="margin-top: var(--space-2)"
        >
          Аналізувати
        </AppButton>
      </form>

      <div v-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>

      <div v-else-if="analytics && analytics.length" class="results-container">
        <h2>Результати порівняння</h2>

        <div class="summary-cards">
          <div class="summary-card">
            <div class="summary-icon">📦</div>
            <div class="summary-value">{{ analytics.length }}</div>
            <div class="summary-label">Товарів у тендері</div>
          </div>
          <div class="summary-card">
            <div class="summary-icon">🏪</div>
            <div class="summary-value">{{ totalStoreMatches }}</div>
            <div class="summary-label">Знайдено в магазинах</div>
          </div>
          <div v-if="hasPricesTender" class="summary-card" :class="overallSavings >= 0 ? 'card-positive' : 'card-negative'">
            <div class="summary-icon">{{ overallSavings >= 0 ? '📈' : '📉' }}</div>
            <div class="summary-value">{{ overallSavings >= 0 ? '+' : '' }}{{ overallSavings.toFixed(2) }} грн</div>
            <div class="summary-label">Тендер {{ overallSavings >= 0 ? 'дорожче' : 'дешевше' }} ринку</div>
          </div>
          <div class="summary-card">
            <div class="summary-icon">💰</div>
            <div class="summary-value">{{ bestDealStore || '—' }}</div>
            <div class="summary-label">Найвигідніший магазин</div>
          </div>
        </div>

        <div v-for="group in analytics" :key="group.name" class="product-group">
          <div class="product-header">
            <div class="product-name">{{ group.name }}</div>
            <div class="product-meta">
              <span class="meta-badge tender-badge" v-if="group.tender_price > 0">
                Тендер: <strong>{{ group.tender_price.toFixed(2) }} грн</strong>
              </span>
              <span class="meta-badge tender-badge" v-else>Тендер: <strong>Не вказано</strong></span>
              <span class="meta-badge qty-badge" v-if="group.quantity">{{ group.quantity }} {{ group.unit_name || 'шт' }}</span>
              <span class="meta-badge total-badge" v-if="group.total_price">Всього: {{ group.total_price.toFixed(2) }} грн</span>
            </div>
          </div>

          <table class="modern-table" v-if="group.matches.length">
            <thead>
              <tr>
                <th>Магазин</th>
                <th>Назва в магазині</th>
                <th>Ціна</th>
                <th>Ціна/кг</th>
                <th>Різниця</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(match, idx) in group.matches"
                :key="idx"
                class="table-row"
                :class="{ 'best-match': idx === 0 }"
              >
                <td><span class="store-badge" :class="'store-' + match.store">{{ match.store_name }}</span></td>
                <td class="product-title-cell">
                  <a :href="match.url" target="_blank" rel="noopener" v-if="match.url">{{ match.title }}</a>
                  <span v-else>{{ match.title }}</span>
                  <span class="sale-tag" v-if="match.is_on_sale">АКЦІЯ</span>
                  <span class="weight-tag" v-if="match.store_weight_g">{{ formatWeight(match.store_weight_g) }}</span>
                </td>
                <td class="price-cell">
                  <span class="current-price">{{ formatPrice(match.effective_price) }} грн</span>
                  <span class="old-price" v-if="match.is_on_sale && match.original_price">{{ formatPrice(match.original_price) }} грн</span>
                </td>
                <td class="price-cell">
                  <template v-if="match.price_per_unit">
                    <span class="normalized-price">{{ formatPrice(match.price_per_unit) }} грн</span>
                    <span class="normalized-label" v-if="match.tender_price_per_unit">
                      тендер: {{ formatPrice(match.tender_price_per_unit) }}
                    </span>
                  </template>
                  <span v-else class="no-data">—</span>
                </td>
                <td :class="getDifferenceClass(match.diff)">{{ formatDiff(match.diff) }}</td>
                <td :class="getDifferenceClass(match.diff)">{{ formatPercent(match.diff, group.tender_price) }}</td>
              </tr>
            </tbody>
          </table>
          <div v-else class="no-matches">Не знайдено в жодному магазині</div>
        </div>
      </div>

      <div v-else-if="tenderId && !isLoading">
        <p>Дані відсутні або товари не знайдені.</p>
      </div>
    </div>

    <AppLoader v-if="isLoading" :overlay="true" />
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { apiClient } from '@/api/config';
import AppButton from '@/components/AppButton.vue';
import AppLoader from '@/components/AppLoader.vue';
import StoreSelector from '@/components/StoreSelector.vue';

export default {
  name: 'Prozorro',
  components: { AppButton, AppLoader, StoreSelector },
  setup() {
    const tenderId = ref('');
    const analytics = ref(null);
    const isLoading = ref(false);
    const error = ref(null);
    const availableStores = [
      { key: 'rozetka', name: 'Rozetka' },
      { key: 'silpo', name: 'Сільпо' },
      { key: 'epicentr', name: 'Епіцентр' },
      { key: 'citadel', name: 'Citadel' },
    ];
    const selectedStores = ref(['rozetka', 'silpo', 'epicentr']);

    const hasPricesTender = computed(() => analytics.value?.some((g) => g.tender_price > 0) ?? false);

    const totalStoreMatches = computed(
      () => analytics.value?.reduce((sum, g) => sum + g.matches.length, 0) ?? 0
    );

    const overallSavings = computed(() => {
      if (!analytics.value) return 0;
      return analytics.value.reduce((total, g) =>
        g.matches.reduce((s, m) => (m.diff !== null ? s + m.diff : s), total), 0
      );
    });

    const bestDealStore = computed(() => {
      if (!analytics.value) return null;
      const totals = {};
      for (const g of analytics.value) {
        for (const m of g.matches) {
          if (m.effective_price !== null) {
            totals[m.store_name] = (totals[m.store_name] ?? 0) + m.effective_price;
          }
        }
      }
      return Object.entries(totals).reduce(
        (best, [name, total]) => (total < best[1] ? [name, total] : best),
        [null, Infinity]
      )[0];
    });

    const processMatchedItems = (matchedItems) => {
      if (!matchedItems?.length) return [];
      return matchedItems.map((group) => {
        const tender = group.tender_item || {};
        const tenderPrice = parseFloat(tender.unit_price) || 0;
        const matches = (group.matches || []).map((item) => {
          const effectivePrice = item.price_on_sale ? parseFloat(item.price_on_sale) : parseFloat(item.price) || null;
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
          };
        }).sort((a, b) => (a.effective_price ?? Infinity) - (b.effective_price ?? Infinity));

        return {
          name: tender.name || '',
          tender_price: tenderPrice,
          quantity: tender.quantity || null,
          unit_name: tender.unit_name || null,
          total_price: tender.total_price ? parseFloat(tender.total_price) : null,
          matches,
        };
      }).filter((item) => item.name);
    };

    const analyzeTender = async () => {
      isLoading.value = true;
      error.value = null;
      analytics.value = null;
      try {
        const response = await apiClient.get(`/search-tender/${tenderId.value}`, {
          params: { stores: selectedStores.value.join(',') },
        });
        analytics.value = processMatchedItems(response.data.matched_items);
      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Помилка сервера';
      } finally {
        isLoading.value = false;
      }
    };

    const formatPrice = (val) => (val == null ? 'Н/Д' : Number(val).toFixed(2));
    const formatWeight = (g) => {
      if (!g) return '';
      return g >= 1000 ? (g / 1000).toFixed(g % 1000 === 0 ? 0 : 1) + ' кг' : g + ' г';
    };
    const formatDiff = (diff) => diff === null ? '—' : (diff >= 0 ? '+' : '') + diff.toFixed(2) + ' грн';
    const formatPercent = (diff, base) => {
      if (diff === null || !base) return '—';
      const pct = (diff / base) * 100;
      return (pct >= 0 ? '+' : '') + pct.toFixed(1) + '%';
    };
    const getDifferenceClass = (diff) =>
      diff === null ? '' : diff > 0 ? 'price-higher' : diff < 0 ? 'price-lower' : 'price-equal';

    return {
      tenderId, analytics, isLoading, error,
      availableStores, selectedStores,
      hasPricesTender, totalStoreMatches, overallSavings, bestDealStore,
      analyzeTender,
      formatPrice, formatWeight, formatDiff, formatPercent, getDifferenceClass,
    };
  },
};
</script>

<style scoped>
.tender-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 2rem;
  padding-top: 100px;
}

.tender-container {
  background: var(--color-surface);
  padding: 2.5rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  max-width: 1100px;
  width: 100%;
  text-align: center;
  font-family: var(--font-body);
  border: 2px solid var(--color-green-500);
  color: var(--color-text);
}

.tender-container h1 {
  font-size: var(--text-4xl);
  color: var(--color-heading);
  margin-bottom: var(--space-4);
  font-weight: var(--font-bold);
}

.tender-container p {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-6);
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

input {
  width: 100%;
  padding: 12px;
  font-size: var(--text-lg);
  border: 2px dashed var(--color-green-500);
  border-radius: var(--radius-md);
  outline: none;
  transition: background-color var(--transition-base), border-color var(--transition-base);
  margin-bottom: var(--space-6);
  text-align: center;
  color: var(--color-text);
  background: var(--color-surface);
}

input:focus {
  background-color: var(--color-green-50);
  border-color: var(--color-danger);
}

.error-message {
  color: var(--color-danger);
  font-size: var(--text-lg);
  margin-top: var(--space-8);
}

/* Summary cards */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
  margin: var(--space-6) 0 var(--space-8);
}

.summary-card {
  background: var(--color-gray-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 1.2rem 1rem;
  text-align: center;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.summary-icon { font-size: 1.8rem; margin-bottom: 0.3rem; }
.summary-value { font-size: var(--text-xl); font-weight: var(--font-bold); color: var(--color-heading); margin-bottom: 0.2rem; }
.summary-label { font-size: var(--text-sm); color: var(--color-text-secondary); font-weight: var(--font-medium); }

.card-positive .summary-value { color: var(--color-danger); }
.card-negative .summary-value { color: var(--color-success); }

/* Product groups */
.results-container { margin-top: var(--space-8); }
.results-container h2 { font-size: var(--text-3xl); color: var(--color-heading); margin-bottom: var(--space-4); font-weight: var(--font-bold); }

.product-group { margin-bottom: var(--space-8); text-align: left; }

.product-header {
  background: var(--color-green-50);
  border: 1px solid var(--color-green-200);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  margin-bottom: var(--space-2);
}

.product-name { font-size: var(--text-base); font-weight: var(--font-bold); color: var(--color-heading); margin-bottom: var(--space-2); }
.product-meta { display: flex; flex-wrap: wrap; gap: var(--space-2); }

.meta-badge {
  display: inline-block;
  padding: 0.25rem 0.7rem;
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
}

.tender-badge { background: var(--color-info-bg); color: var(--color-info); }
.qty-badge { background: var(--color-primary-light); color: var(--color-primary); }
.total-badge { background: var(--color-warning-bg); color: var(--color-warning); }

/* Table */
.modern-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-body);
  margin-bottom: var(--space-2);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.modern-table th {
  background: var(--color-gray-100);
  color: var(--color-text-secondary);
  padding: 10px 14px;
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid var(--color-border);
}

.modern-table td {
  padding: 10px 14px;
  text-align: center;
  color: var(--color-text);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  vertical-align: middle;
}

.modern-table td a { color: var(--color-info); text-decoration: none; font-weight: var(--font-semibold); }
.modern-table td a:hover { text-decoration: underline; }

.table-row:hover td { background: var(--color-gray-50); }
.best-match td { background: var(--color-green-50); }
.best-match:hover td { background: var(--color-green-100); }

.product-title-cell { text-align: left !important; max-width: 320px; }

.sale-tag {
  display: inline-block;
  background: var(--color-danger-light);
  color: var(--color-danger);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  margin-left: 6px;
  vertical-align: middle;
  text-transform: uppercase;
}

.weight-tag {
  display: inline-block;
  background: var(--color-info-bg);
  color: var(--color-info);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  margin-left: 6px;
  vertical-align: middle;
}

.normalized-price { font-weight: var(--font-semibold); color: var(--color-text); }
.normalized-label { display: block; font-size: var(--text-xs); color: var(--color-text-secondary); }
.no-data { color: var(--color-gray-300); }
.price-cell { white-space: nowrap; }
.current-price { font-weight: var(--font-bold); color: var(--color-heading); }
.old-price { display: block; font-size: var(--text-xs); color: var(--color-text-secondary); text-decoration: line-through; }

.store-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  white-space: nowrap;
}

.store-rozetka { background: var(--color-green-100); color: var(--color-green-700); }
.store-silpo { background: var(--color-warning-bg); color: var(--color-warning); }
.store-epicentr { background: var(--color-info-bg); color: var(--color-info); }
.store-citadel { background: var(--color-danger-light); color: var(--color-danger); }

.price-higher { color: var(--color-danger); font-weight: var(--font-bold); background: var(--color-danger-light); border-radius: var(--radius-sm); }
.price-lower { color: var(--color-success); font-weight: var(--font-bold); background: var(--color-green-50); border-radius: var(--radius-sm); }
.price-equal { color: var(--color-text-secondary); font-weight: var(--font-bold); background: var(--color-gray-100); border-radius: var(--radius-sm); }

.no-matches { padding: 0.8rem 1.2rem; color: var(--color-text-secondary); font-style: italic; font-size: var(--text-sm); }
</style>
