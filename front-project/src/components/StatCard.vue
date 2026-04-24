<template>
  <div class="stat-card" :class="variant && `stat-card--${variant}`">
    <div class="stat-card__label">
      <slot name="label">{{ label }}</slot>
    </div>
    <div class="stat-card__value">
      <slot name="value">{{ value }}</slot>
    </div>
    <div v-if="$slots.meta || meta" class="stat-card__meta">
      <slot name="meta">{{ meta }}</slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    label: { type: String, default: '' },
    value: { type: [String, Number], default: '' },
    meta: { type: String, default: '' },
    variant: {
      type: String,
      default: null,
      validator: (v) => v === null || ['neutral', 'brand', 'danger', 'warn'].includes(v),
    },
  },
}
</script>

<style scoped>
.stat-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  box-shadow: var(--shadow-soft);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-card__label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-text-secondary);
  font-weight: var(--font-medium);
}

.stat-card__value {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
  color: var(--color-heading);
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
}

.stat-card__meta {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  font-variant-numeric: tabular-nums;
}

.stat-card--danger .stat-card__value { color: var(--color-danger); }
.stat-card--brand .stat-card__value { color: var(--color-primary); }
.stat-card--warn .stat-card__value { color: var(--color-warning); }
</style>
