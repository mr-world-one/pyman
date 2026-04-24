<template>
  <div class="empty-state">
    <div class="empty-state__icon">
      <slot name="icon">
        <AppIcon :name="iconName" :size="22" />
      </slot>
    </div>
    <h3 class="empty-state__title">{{ title }}</h3>
    <p v-if="description" class="empty-state__description">{{ description }}</p>
    <div v-if="$slots.default" class="empty-state__actions">
      <slot />
    </div>
  </div>
</template>

<script>
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'EmptyState',
  components: { AppIcon },
  props: {
    iconName: { type: String, default: 'empty' },
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
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background: var(--color-bg-subtle);
}

.empty-state__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
}

.empty-state__title {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
  color: var(--color-heading);
  margin-bottom: var(--space-2);
}

.empty-state__description {
  font-size: var(--text-base);
  max-width: 400px;
  margin: 0 auto;
  line-height: 1.6;
  color: var(--color-text-secondary);
}

.empty-state__actions {
  margin-top: var(--space-5);
  display: flex;
  justify-content: center;
  gap: var(--space-2);
  flex-wrap: wrap;
}
</style>
