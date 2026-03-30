<template>
  <div class="tender-card" @click="$emit('click', tender)">
    <div class="card-top">
      <TenderTypeBadge :type="tender.tender_type" />
      <span class="tender-status" :class="'status-' + tender.status">{{ tender.status }}</span>
    </div>

    <h3 class="card-title">{{ tender.title }}</h3>

    <div class="card-meta">
      <span class="meta-id">{{ tender.prozorro_id }}</span>
      <span v-if="tender.customer_name" class="meta-customer">{{ tender.customer_name }}</span>
    </div>

    <div class="card-footer">
      <span class="card-amount" v-if="tender.total_amount">
        {{ formatPrice(tender.total_amount) }} грн
      </span>
      <span class="card-items">{{ tender.items_count }} позицій</span>
      <span class="card-date">{{ formatDate(tender.created_at) }}</span>
    </div>
  </div>
</template>

<script>
import TenderTypeBadge from './TenderTypeBadge.vue'

export default {
  name: 'TenderCard',
  components: { TenderTypeBadge },
  props: {
    tender: { type: Object, required: true },
  },
  emits: ['click'],
  methods: {
    formatPrice(val) {
      if (val == null) return '—'
      return Number(val).toLocaleString('uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('uk-UA')
    },
  },
}
</script>

<style scoped>
.tender-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4) var(--space-5);
  cursor: pointer;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast), border-color var(--transition-fast);
}

.tender-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-green-300);
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.tender-status {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-full);
}

.status-active { background: var(--color-green-100); color: var(--color-green-700); }
.status-closed { background: var(--color-gray-100); color: var(--color-gray-600); }
.status-cancelled { background: var(--color-danger-light); color: var(--color-danger); }

.card-title {
  font-size: var(--text-base);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-2);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  margin-bottom: var(--space-3);
}

.meta-id {
  font-size: var(--text-xs);
  color: var(--color-info);
  font-weight: var(--font-medium);
  font-family: monospace;
}

.meta-customer {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.card-footer {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-3);
}

.card-amount {
  font-weight: var(--font-bold);
  color: var(--color-heading);
}

.card-items {
  font-weight: var(--font-medium);
}

.card-date {
  margin-left: auto;
  font-size: var(--text-xs);
}
</style>
