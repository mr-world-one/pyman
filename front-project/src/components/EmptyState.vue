<template>
  <div class="empty-state">
    <div class="empty-state__icon">{{ icon }}</div>
    <h3 class="empty-state__title">{{ title }}</h3>
    <p v-if="description" class="empty-state__description">{{ description }}</p>
    <slot />
  </div>
</template>

<script>
export default {
  name: 'EmptyState',
  props: {
    icon: { type: String, default: '\u{1F4CB}' },
    title: { type: String, default: 'Дані відсутні' },
    description: { type: String, default: '' },
  },
}
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: var(--space-12) var(--space-4);
  color: var(--color-text-secondary);
}

.empty-state__icon {
  font-size: 3rem;
  margin-bottom: var(--space-4);
  opacity: 0.6;
}

.empty-state__title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-gray-600);
  margin-bottom: var(--space-2);
}

.empty-state__description {
  font-size: var(--text-sm);
  max-width: 400px;
  margin: 0 auto;
  line-height: 1.6;
}
</style>
