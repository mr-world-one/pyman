<template>
  <div class="product-detail">
    <div v-if="!items || !items.length" class="detail-empty">Позицій немає</div>
    <div v-else class="table-responsive">
      <table class="data-table">
        <thead>
          <tr>
            <th class="col-idx">#</th>
            <th>Назва</th>
            <th class="col-num">К-сть</th>
            <th class="col-short">Од.</th>
            <th class="col-num">Ціна/од.</th>
            <th class="col-num">Сума</th>
            <th class="col-short">ДК код</th>
            <th class="col-short">ДСТУ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, i) in items" :key="item.id" class="row-hover">
            <td class="col-idx mono">{{ (i + 1).toString().padStart(3, '0') }}</td>
            <td class="name-cell">{{ item.name }}</td>
            <td class="num col-num">{{ item.quantity }}</td>
            <td class="col-short">{{ item.unit_name }}</td>
            <td class="num col-num">
              <span v-if="item.unit_price != null">{{ formatPrice(item.unit_price) }}</span>
              <span v-else class="dim">—</span>
              <PriceSourceBadge :source="item.price_source" />
            </td>
            <td class="num col-num emph">
              <span v-if="item.unit_price != null">{{ formatPrice(item.unit_price * item.quantity) }}</span>
              <span v-else class="dim">—</span>
            </td>
            <td class="col-short mono">{{ item.dk_code || '—' }}</td>
            <td class="col-short mono">{{ item.dstu_gost || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import PriceSourceBadge from '@/components/tenders/PriceSourceBadge.vue'

export default {
  name: 'ProductTenderDetail',
  components: { PriceSourceBadge },
  props: { items: { type: Array, required: true } },
  methods: {
    formatPrice(val) {
      if (val == null) return '—'
      return Number(val).toLocaleString('uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
  },
}
</script>

<style scoped>
.product-detail { width: 100%; }

.detail-empty {
  padding: var(--space-8);
  text-align: center;
  color: var(--color-text-secondary);
  font-style: italic;
}

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
.data-table thead th.col-idx { width: 60px; }
.data-table thead th.col-short { width: 100px; }

.data-table tbody td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
}

.data-table tbody td.col-num { text-align: right; font-variant-numeric: tabular-nums; }
.data-table tbody td.col-idx { color: var(--color-text-secondary); font-size: 11.5px; }
.data-table tbody td.col-short { color: var(--color-text-secondary); font-size: var(--text-sm); }

.data-table tr.row-hover:hover td { background: var(--color-bg-subtle); }

.name-cell { max-width: 360px; color: var(--color-heading); font-weight: var(--font-medium); }

.emph { color: var(--color-heading); font-weight: var(--font-semibold); }

.dim { color: var(--color-text-tertiary); }
</style>
