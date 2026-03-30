<template>
  <div class="product-detail">
    <h3>Товари ({{ items.length }})</h3>
    <table class="detail-table" v-if="items.length">
      <thead>
        <tr>
          <th>#</th>
          <th>Назва</th>
          <th>К-сть</th>
          <th>Од.</th>
          <th>Ціна/од.</th>
          <th>Сума</th>
          <th>ДК код</th>
          <th>ДСТУ</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, i) in items" :key="item.id">
          <td>{{ i + 1 }}</td>
          <td class="name-cell">{{ item.name }}</td>
          <td>{{ item.quantity }}</td>
          <td>{{ item.unit_name }}</td>
          <td class="price-cell">{{ formatPrice(item.unit_price) }}</td>
          <td class="price-cell">{{ formatPrice(item.unit_price * item.quantity) }}</td>
          <td>{{ item.dk_code || '—' }}</td>
          <td>{{ item.dstu_gost || '—' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'ProductTenderDetail',
  props: {
    items: { type: Array, required: true },
  },
  methods: {
    formatPrice(val) {
      if (val == null) return '—'
      return Number(val).toLocaleString('uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
  },
}
</script>

<style scoped>
.product-detail h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-3);
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.detail-table th {
  background: var(--color-gray-100);
  color: var(--color-text-secondary);
  padding: 10px 12px;
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid var(--color-border);
}

.detail-table td {
  padding: 10px 12px;
  text-align: center;
  color: var(--color-text);
  font-size: var(--text-sm);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
}

.name-cell {
  text-align: left !important;
  max-width: 300px;
  font-weight: var(--font-medium);
}

.price-cell {
  font-weight: var(--font-bold);
  color: var(--color-heading);
  white-space: nowrap;
}
</style>
