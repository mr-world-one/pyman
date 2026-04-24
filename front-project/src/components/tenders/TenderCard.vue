<template>
  <article class="tender-card" :class="`status-${tender.status}`" @click="$emit('click', tender)">
    <div class="tender-card__top">
      <TenderTypeBadge :type="tender.tender_type" />
      <AppBadge :variant="statusVariant" :show-dot="tender.status === 'active'">
        {{ statusLabel }}
      </AppBadge>
    </div>

    <h3 class="tender-card__title">{{ tender.title }}</h3>

    <div class="tender-card__meta">
      <div class="tender-card__id mono">{{ tender.prozorro_id }}</div>
      <div v-if="tender.customer_name" class="tender-card__customer">{{ tender.customer_name }}</div>
    </div>

    <div class="tender-card__footer">
      <div v-if="tender.total_amount">
        <div class="tender-card__label">Сума</div>
        <div class="tender-card__amount num">
          {{ formatPrice(tender.total_amount) }} <span class="tender-card__currency">₴</span>
        </div>
      </div>
      <div class="tender-card__aside">
        <div class="tender-card__items num">{{ tender.items_count }} позицій</div>
        <div class="tender-card__date">{{ formatDate(tender.created_at) }}</div>
      </div>
    </div>
  </article>
</template>

<script>
import TenderTypeBadge from './TenderTypeBadge.vue'
import AppBadge from '@/components/AppBadge.vue'

const STATUS_LABELS = {
  active: 'Активний',
  closed: 'Завершений',
  cancelled: 'Скасований',
}

const STATUS_VARIANTS = {
  active: 'brand',
  closed: 'slate',
  cancelled: 'danger',
}

export default {
  name: 'TenderCard',
  components: { TenderTypeBadge, AppBadge },
  props: {
    tender: { type: Object, required: true },
  },
  emits: ['click'],
  computed: {
    statusLabel() { return STATUS_LABELS[this.tender.status] || this.tender.status },
    statusVariant() { return STATUS_VARIANTS[this.tender.status] || 'slate' },
  },
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
  padding: var(--space-5);
  cursor: pointer;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.tender-card:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--shadow-soft);
}

.tender-card__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
}

.tender-card__title {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
  color: var(--color-heading);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  letter-spacing: 0;
  transition: color var(--transition-fast);
}

.tender-card:hover .tender-card__title {
  color: var(--color-primary);
}

.tender-card__meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.tender-card__id {
  font-size: 11.5px;
  color: var(--color-text-secondary);
}

.tender-card__customer {
  font-size: var(--text-sm);
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tender-card__footer {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
  margin-top: auto;
}

.tender-card__label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-text-secondary);
}

.tender-card__amount {
  font-size: 17px;
  font-weight: var(--font-semibold);
  color: var(--color-heading);
  margin-top: 2px;
}

.tender-card__currency {
  color: var(--color-text-secondary);
  font-weight: var(--font-normal);
}

.tender-card__aside {
  text-align: right;
  font-size: 11.5px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.tender-card__items { color: var(--color-text); }
</style>
