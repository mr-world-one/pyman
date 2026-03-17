<template>
  <div class="tender-page">
    <div class="tender-container">
      <h1>Пошук тендеру</h1>
      <p>Введіть ID Prozorro-тендеру для аналізу:</p>
      <form @submit.prevent="analyzeTender">
        <input type="text"
               v-model.trim="tenderId"
               placeholder="Введіть ID тендеру (наприклад, UA-2023-01-01-000001-a)"
               required />

        <div class="store-selector">
          <label>Оберіть магазини для порівняння:</label>
          <div class="store-checkboxes">
            <label v-for="store in availableStores" :key="store.key" class="store-checkbox">
              <input type="checkbox" :value="store.key" v-model="selectedStores" />
              {{ store.name }}
            </label>
          </div>
        </div>

        <button type="submit" :disabled="isLoading || selectedStores.length === 0">Аналізувати</button>
      </form>
      <div v-if="isLoading" class="loading-overlay">
        <div aria-busy="true" aria-label="Loading" role="progressbar" class="loading-container">
          <div class="swing">
            <div class="swing-l"></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div class="swing-r"></div>
          </div>
          <div class="shadow">
            <div class="shadow-l"></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div class="shadow-r"></div>
          </div>
        </div>
        <p class="loading-text">Виконується аналіз, це може трішки тривати...</p>
      </div>
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="analytics && analytics.length" class="results-container">
        <h2>Результати порівняння</h2>

        <!-- Summary cards -->
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
          <div class="summary-card" :class="overallSavings >= 0 ? 'card-positive' : 'card-negative'" v-if="hasPricesTender">
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

        <!-- Table per prozorro item -->
        <div v-for="group in analytics" :key="group.name" class="product-group">
          <div class="product-header">
            <div class="product-name">{{ group.name }}</div>
            <div class="product-meta">
              <span class="meta-badge tender-badge" v-if="group.tender_price > 0">Тендер: <strong>{{ group.tender_price.toFixed(2) }} грн</strong></span>
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
              <tr v-for="(match, idx) in group.matches" :key="idx" class="table-row" :class="{ 'best-match': idx === 0 }">
                <td>
                  <span class="store-badge" :class="'store-' + match.store">{{ match.store_name }}</span>
                </td>
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
                <td :class="getDifferenceClass(match.diff)">
                  {{ formatDiff(match.diff) }}
                </td>
                <td :class="getDifferenceClass(match.diff)">
                  {{ formatPercent(match.diff, group.tender_price) }}
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="no-matches">
            Не знайдено в жодному магазині
          </div>
        </div>
      </div>
      <div v-else-if="tenderId && !isLoading">
        <p>Дані відсутні або товари не знайдені.</p>
      </div>
    </div>
  </div>
</template>

<script>
  import { apiClient } from '@/api/config';

  export default {
    name: 'Prozorro',
    data() {
      return {
        tenderId: '',
        analytics: null,
        isLoading: false,
        error: null,
        availableStores: [
          { key: 'rozetka', name: 'Rozetka' },
          { key: 'silpo', name: 'Сільпо' },
          { key: 'epicentr', name: 'Епіцентр' },
          { key: 'citadel', name: 'Citadel' },
        ],
        selectedStores: ['rozetka', 'silpo', 'epicentr'],
      };
    },
    computed: {
      hasPricesTender() {
        if (!this.analytics) return false;
        return this.analytics.some(g => g.tender_price > 0);
      },
      totalStoreMatches() {
        if (!this.analytics) return 0;
        return this.analytics.reduce((sum, g) => sum + g.matches.length, 0);
      },
      overallSavings() {
        if (!this.analytics) return 0;
        let total = 0;
        let count = 0;
        for (const g of this.analytics) {
          for (const m of g.matches) {
            if (m.diff !== null) {
              total += m.diff;
              count++;
            }
          }
        }
        return total;
      },
      bestDealStore() {
        if (!this.analytics) return null;
        const storeTotals = {};
        for (const g of this.analytics) {
          for (const m of g.matches) {
            if (m.effective_price !== null) {
              if (!storeTotals[m.store_name]) storeTotals[m.store_name] = 0;
              storeTotals[m.store_name] += m.effective_price;
            }
          }
        }
        let best = null;
        let bestTotal = Infinity;
        for (const [name, total] of Object.entries(storeTotals)) {
          if (total < bestTotal) {
            bestTotal = total;
            best = name;
          }
        }
        return best;
      },
    },
    methods: {
      async analyzeTender() {
        this.isLoading = true;
        this.error = null;
        this.analytics = null;

        try {
          const storesParam = this.selectedStores.join(',');
          const searchResponse = await apiClient.get(
            `/search-tender/${this.tenderId}`,
            { params: { stores: storesParam } }
          );

          this.analytics = this.processMatchedItems(
            searchResponse.data.matched_items
          );
        } catch (error) {
          this.error = error.response?.data?.detail || error.message || 'Помилка сервера';
        } finally {
          this.isLoading = false;
        }
      },
      processMatchedItems(matchedItems) {
        if (!matchedItems || !matchedItems.length) return [];

        return matchedItems.map((group) => {
          const tender = group.tender_item || {};
          const name = tender.name || '';
          const tenderPrice = parseFloat(tender.unit_price) || 0;

          const matches = (group.matches || []).map((item) => {
            const effectivePrice = item.price_on_sale
              ? parseFloat(item.price_on_sale)
              : parseFloat(item.price) || null;
            const originalPrice = item.price_on_sale
              ? parseFloat(item.price) : null;
            return {
              title: item.title || '—',
              store: item.store || '',
              store_name: item.store_name || '—',
              url: item.url || null,
              effective_price: effectivePrice,
              original_price: originalPrice,
              is_on_sale: !!item.price_on_sale && item.price_on_sale !== item.price,
              is_available: item.is_available,
              diff: (effectivePrice !== null && tenderPrice > 0) ? tenderPrice - effectivePrice : null,
              store_weight_g: item.store_weight_g || null,
              tender_weight_g: item.tender_weight_g || null,
              price_per_unit: item.price_per_unit || null,
              tender_price_per_unit: item.tender_price_per_unit || null,
            };
          }).sort((a, b) => (a.effective_price || Infinity) - (b.effective_price || Infinity));

          return {
            name,
            tender_price: tenderPrice,
            quantity: tender.quantity || null,
            unit_name: tender.unit_name || null,
            total_price: tender.total_price ? parseFloat(tender.total_price) : null,
            matches,
          };
        }).filter((item) => item.name);
      },
      formatPrice(val) {
        if (val === null || val === undefined) return 'Н/Д';
        return Number(val).toFixed(2);
      },
      formatWeight(grams) {
        if (!grams) return '';
        if (grams >= 1000) return (grams / 1000).toFixed(grams % 1000 === 0 ? 0 : 1) + ' кг';
        return grams + ' г';
      },
      formatDiff(diff) {
        if (diff === null) return '—';
        return (diff >= 0 ? '+' : '') + diff.toFixed(2) + ' грн';
      },
      formatPercent(diff, base) {
        if (diff === null || !base) return '—';
        const pct = (diff / base) * 100;
        return (pct >= 0 ? '+' : '') + pct.toFixed(1) + '%';
      },
      getDifferenceClass(diff) {
        if (diff === null) return '';
        return diff > 0 ? 'price-higher' : diff < 0 ? 'price-lower' : 'price-equal';
      },
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
    background: #ffffff;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    max-width: 1100px;
    width: 100%;
    text-align: center;
    font-family: 'Raleway', sans-serif;
    border: 2px solid #0efc3d;
    color: #333;
  }

    .tender-container h1 {
      font-size: 2.5rem;
      color: #333;
      margin-bottom: 1rem;
      font-weight: 700;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
    }

    .tender-container p {
      font-size: 1.2rem;
      color: #444;
      margin-bottom: 1.5rem;
    }

  form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input {
    width: 100%;
    padding: 12px;
    font-size: 1.2rem;
    border: 2px dashed #0efc3d;
    border-radius: 8px;
    outline: none;
    transition: background-color 0.3s ease, border-color 0.3s ease;
    margin-bottom: 1.5rem;
    text-align: center;
    color: #333;
    background: #fff;
  }

    input:focus {
      background-color: rgba(0, 255, 0, 0.1);
      border-color: #b2221e;
    }

  button {
    padding: 0.85rem 2rem;
    font-size: 1.1rem;
    background: linear-gradient(135deg, #41ec22, #27ac0f);
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.2s ease;
  }

    button:hover {
      background: linear-gradient(135deg, #27ac0f, #41ec22);
      transform: scale(1.03);
    }

    button:disabled {
      background: #ccc;
      cursor: not-allowed;
      transform: none;
    }

  /* Summary cards */
  .summary-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0 2rem;
  }

  .summary-card {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
  }

    .summary-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

  .summary-icon {
    font-size: 1.8rem;
    margin-bottom: 0.3rem;
  }

  .summary-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: #222;
    margin-bottom: 0.2rem;
  }

  .summary-label {
    font-size: 0.85rem;
    color: #666;
    font-weight: 500;
  }

  .card-positive .summary-value { color: #e63946; }
  .card-negative .summary-value { color: #2a9d8f; }

  /* Product groups */
  .product-group {
    margin-bottom: 2rem;
    text-align: left;
  }

  .product-header {
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
  }

  .product-name {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
  }

  .product-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .meta-badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #333;
  }

  .tender-badge {
    background: #dbeafe;
    color: #1e40af;
  }

  .qty-badge {
    background: #f3e8ff;
    color: #7c3aed;
  }

  .total-badge {
    background: #fef3c7;
    color: #92400e;
  }

  .results-container {
    margin-top: 2rem;
  }

    .results-container h2 {
      font-size: 2rem;
      color: #333;
      margin-bottom: 1rem;
      font-weight: 700;
    }

  /* Table */
  .modern-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Raleway', sans-serif;
    margin-bottom: 0.5rem;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  }

    .modern-table th {
      background: #f8fafc;
      color: #475569;
      padding: 10px 14px;
      font-size: 0.8rem;
      font-weight: 700;
      text-align: center;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 2px solid #e2e8f0;
    }

    .modern-table td {
      padding: 10px 14px;
      text-align: center;
      color: #334155;
      font-size: 0.95rem;
      font-weight: 500;
      border-bottom: 1px solid #f1f5f9;
      background: #fff;
      vertical-align: middle;
    }

    .modern-table td a {
      color: #2563eb;
      text-decoration: none;
      font-weight: 600;
    }

      .modern-table td a:hover {
        text-decoration: underline;
        color: #1d4ed8;
      }

  .table-row:hover td {
    background: #f8fafc;
  }

  .best-match td {
    background: #f0fdf4;
  }

  .best-match:hover td {
    background: #dcfce7;
  }

  /* Product title cell */
  .product-title-cell {
    text-align: left !important;
    max-width: 320px;
  }

  .sale-tag {
    display: inline-block;
    background: #fee2e2;
    color: #dc2626;
    font-size: 0.65rem;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: 4px;
    margin-left: 6px;
    vertical-align: middle;
    text-transform: uppercase;
  }

  .weight-tag {
    display: inline-block;
    background: #e0f2fe;
    color: #0369a1;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 4px;
    margin-left: 6px;
    vertical-align: middle;
  }

  .normalized-price {
    font-weight: 600;
    color: #334155;
  }

  .normalized-label {
    display: block;
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .no-data {
    color: #cbd5e1;
  }

  /* Price cell */
  .price-cell {
    white-space: nowrap;
  }

  .current-price {
    font-weight: 700;
    color: #1a1a1a;
  }

  .old-price {
    display: block;
    font-size: 0.8rem;
    color: #94a3b8;
    text-decoration: line-through;
  }

  /* Store badges */
  .store-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 700;
    white-space: nowrap;
  }

  .store-rozetka { background: #e8f5e9; color: #2e7d32; }
  .store-silpo { background: #fff3e0; color: #e65100; }
  .store-epicentr { background: #e3f2fd; color: #1565c0; }
  .store-citadel { background: #fce4ec; color: #c62828; }

  /* Price diff badges */
  .price-higher {
    color: #dc2626;
    font-weight: 700;
    background: #fef2f2;
    border-radius: 6px;
  }

  .price-lower {
    color: #059669;
    font-weight: 700;
    background: #ecfdf5;
    border-radius: 6px;
  }

  .price-equal {
    color: #6b7280;
    font-weight: 700;
    background: #f3f4f6;
    border-radius: 6px;
  }

  .no-matches {
    padding: 0.8rem 1.2rem;
    color: #9ca3af;
    font-style: italic;
    font-size: 0.95rem;
  }

  /* Store selector */
  .store-selector {
    margin: 1.5rem 0;
    text-align: left;
  }

    .store-selector label {
      font-size: 1.1rem;
      font-weight: 600;
      color: #333;
    }

  .store-checkboxes {
    display: flex;
    gap: 1.2rem;
    flex-wrap: wrap;
    margin-top: 0.5rem;
    justify-content: center;
  }

  .store-checkbox {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-weight: 500 !important;
    cursor: pointer;
    padding: 0.4rem 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    transition: background 0.2s;
    color: #333;
  }

    .store-checkbox:hover {
      background: rgba(14, 252, 61, 0.1);
    }

    .store-checkbox input[type='checkbox'] {
      width: auto;
      margin: 0;
    }

  .error-message {
    color: #e63946;
    font-size: 1.2rem;
    margin-top: 2rem;
  }

  /* Loading */
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .loading-container {
    position: relative;
  }

  .swing div {
    border-radius: 50%;
    float: left;
    height: 1.5em;
    width: 1.5em;
    margin: 0 0.3em;
  }

    .swing div:nth-of-type(1) { background: linear-gradient(to right, #0efc3d, #41ec22); }
    .swing div:nth-of-type(2) { background: linear-gradient(to right, #41ec22, #6be34e); }
    .swing div:nth-of-type(3) { background: linear-gradient(to right, #6be34e, #95d97b); }
    .swing div:nth-of-type(4) { background: linear-gradient(to right, #95d97b, #bfcf9c); }
    .swing div:nth-of-type(5) { background: linear-gradient(to right, #bfcf9c, #e8c5be); }
    .swing div:nth-of-type(6) { background: linear-gradient(to right, #e8c5be, #ff8080); }
    .swing div:nth-of-type(7) { background: linear-gradient(to right, #ff8080, #ff0000); }

  .shadow {
    clear: left;
    padding-top: 1.5em;
    text-align: center;
  }

    .shadow div {
      filter: blur(1px);
      float: left;
      width: 1.5em;
      height: 0.25em;
      border-radius: 50%;
      background: #e3dbd2;
      margin: 0 0.3em;
    }

    .shadow .shadow-l { background: #d5d8d6; }
    .shadow .shadow-r { background: #eed3ca; }

  .swing-l { animation: ball-l 0.425s ease-in-out infinite alternate; }
  .swing-r { animation: ball-r 0.425s ease-in-out infinite alternate; }
  .shadow-l { animation: shadow-l-n 0.425s ease-in-out infinite alternate; }
  .shadow-r { animation: shadow-r-n 0.425s ease-in-out infinite alternate; }

  @keyframes ball-l {
    0%, 50% { transform: rotate(0) translateX(0); }
    100% { transform: rotate(50deg) translateX(-2.5em); }
  }

  @keyframes ball-r {
    0% { transform: rotate(-50deg) translateX(2.5em); }
    50%, 100% { transform: rotate(0) translateX(0); }
  }

  @keyframes shadow-l-n {
    0%, 50% { opacity: 0.5; transform: translateX(0); }
    100% { opacity: 0.125; transform: translateX(-1.75em); }
  }

  @keyframes shadow-r-n {
    0% { opacity: 0.125; transform: translateX(1.75em); }
    50%, 100% { opacity: 0.5; transform: translateX(0); }
  }

  .loading-text {
    color: #fff;
    font-size: 1.5rem;
    margin-top: 2rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
</style>
