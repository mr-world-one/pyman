<template>
  <div class="app-tabs">
    <div class="app-tabs__list" role="tablist">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="['app-tabs__btn', { 'is-active': tab.key === modelValue }]"
        :aria-selected="tab.key === modelValue"
        role="tab"
        type="button"
        @click="$emit('update:modelValue', tab.key)"
      >
        {{ tab.label }}
        <span v-if="tab.count != null" class="app-tabs__count num">{{ tab.count }}</span>
      </button>
    </div>
    <div class="app-tabs__panel">
      <slot :active="modelValue" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppTabs',
  props: {
    tabs: { type: Array, required: true },
    modelValue: { type: String, required: true },
  },
  emits: ['update:modelValue'],
}
</script>

<style scoped>
.app-tabs {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}

.app-tabs__list {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0 var(--space-2);
  border-bottom: 1px solid var(--color-border);
  overflow-x: auto;
}

.app-tabs__btn {
  position: relative;
  height: 44px;
  padding: 0 var(--space-3);
  background: transparent;
  border: none;
  font-family: inherit;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: color var(--transition-fast);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.app-tabs__btn::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 2px;
  background: transparent;
  transition: background var(--transition-fast);
}

.app-tabs__btn:hover {
  color: var(--color-text);
}

.app-tabs__btn.is-active {
  color: var(--color-heading);
  font-weight: var(--font-medium);
}

.app-tabs__btn.is-active::after {
  background: var(--color-primary);
}

.app-tabs__count {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  font-variant-numeric: tabular-nums;
}
</style>
