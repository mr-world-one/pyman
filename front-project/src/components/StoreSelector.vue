<template>
  <div class="store-selector">
    <div v-if="label" class="store-selector__label">{{ label }}</div>
    <div class="store-selector__list">
      <label
        v-for="store in stores"
        :key="store.key"
        :class="['store-chip', `store-chip--${store.key}`, { 'is-active': modelValue.includes(store.key) }]"
      >
        <input
          type="checkbox"
          :value="store.key"
          :checked="modelValue.includes(store.key)"
          class="store-chip__input"
          @change="toggle(store.key)"
        />
        <span class="store-chip__dot" aria-hidden="true"></span>
        <span class="store-chip__name">{{ store.name }}</span>
        <AppIcon v-if="modelValue.includes(store.key)" name="check" :size="14" class="store-chip__check" />
      </label>
    </div>
  </div>
</template>

<script>
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'StoreSelector',
  components: { AppIcon },
  props: {
    modelValue: { type: Array, required: true },
    stores: { type: Array, required: true },
    label: { type: String, default: 'Магазини для звірки' },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    function toggle(key) {
      const newValue = props.modelValue.includes(key)
        ? props.modelValue.filter((k) => k !== key)
        : [...props.modelValue, key]
      emit('update:modelValue', newValue)
    }
    return { toggle }
  },
}
</script>

<style scoped>
.store-selector {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.store-selector__label {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--color-text);
}

.store-selector__list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.store-chip {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  height: 36px;
  padding: 0 var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface);
  font-size: var(--text-sm);
  color: var(--color-text);
  cursor: pointer;
  transition: background var(--transition-fast), border-color var(--transition-fast), color var(--transition-fast);
  user-select: none;
}

.store-chip:hover:not(.is-active) {
  background: var(--color-bg-subtle);
  border-color: var(--color-border-hover);
}

.store-chip.is-active {
  background: var(--color-green-50);
  border-color: var(--color-green-200);
  color: var(--color-green-700);
}

.store-chip__input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.store-chip__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-slate-400);
  flex-shrink: 0;
}

.store-chip--rozetka .store-chip__dot { background: var(--color-info); }
.store-chip--silpo .store-chip__dot { background: var(--color-primary); }
.store-chip--epicentr .store-chip__dot { background: var(--color-warning); }

.store-chip__check {
  color: currentColor;
}
</style>
