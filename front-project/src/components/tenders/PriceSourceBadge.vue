<template>
  <span v-if="source && source !== 'tender'" :class="['price-source', `price-source--${source}`]" :title="title">
    {{ label }}
  </span>
</template>

<script>
const LABELS = {
  tender: 'тендер',
  market_estimate: 'ринок',
  manual: 'введено',
  unknown: '—',
}

const TITLES = {
  tender: 'Ціна з тендерної документації',
  market_estimate: 'Оцінка на основі актуальних цін магазинів',
  manual: 'Ціну введено вручну',
  unknown: 'Ціна не вказана',
}

export default {
  name: 'PriceSourceBadge',
  props: {
    source: { type: String, default: 'tender' },
  },
  computed: {
    label() { return LABELS[this.source] || this.source },
    title() { return TITLES[this.source] || '' },
  },
}
</script>

<style scoped>
.price-source {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 1px 6px;
  margin-left: 6px;
  border-radius: var(--radius-full);
  font-size: 10px;
  font-weight: var(--font-medium);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  line-height: 1.4;
  vertical-align: middle;
  font-variant-numeric: normal;
  font-family: var(--font-body);
  white-space: nowrap;
}

.price-source--market_estimate {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.price-source--manual {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.price-source--unknown {
  background: var(--color-slate-100);
  color: var(--color-text-secondary);
}
</style>
