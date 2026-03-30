<template>
  <span class="tender-type-badge" :class="'type-' + type">{{ label }}</span>
</template>

<script>
const TYPE_LABELS = {
  product: 'Товари',
  service: 'Послуги',
  work: 'Роботи',
  consulting: 'Консалтинг',
  mixed: 'Змішаний',
}

export default {
  name: 'TenderTypeBadge',
  props: {
    type: { type: String, required: true },
  },
  computed: {
    label() {
      return TYPE_LABELS[this.type] || this.type
    },
  },
}
</script>

<style scoped>
.tender-type-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-bold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.type-product {
  background: var(--color-green-100);
  color: var(--color-green-700);
}

.type-service {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.type-work {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.type-consulting {
  background: var(--color-gray-100);
  color: var(--color-gray-700);
}

.type-mixed {
  background: var(--color-danger-light);
  color: var(--color-danger);
}
</style>
