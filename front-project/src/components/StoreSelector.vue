<template>
  <div class="store-selector">
    <label v-if="label" class="store-selector__label">{{ label }}</label>
    <div class="store-selector__list">
      <label
        v-for="store in stores"
        :key="store.key"
        class="store-selector__item"
      >
        <input
          type="checkbox"
          :value="store.key"
          :checked="modelValue.includes(store.key)"
          @change="toggle(store.key)"
        />
        {{ store.name }}
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StoreSelector',
  props: {
    modelValue: { type: Array, required: true },
    stores: { type: Array, required: true },
    label: { type: String, default: 'Оберіть магазини для порівняння:' },
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
  margin: var(--space-6) 0;
  text-align: left;
}

.store-selector__label {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  display: block;
  margin-bottom: var(--space-2);
}

.store-selector__list {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
  justify-content: center;
}

.store-selector__item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-weight: var(--font-medium);
  cursor: pointer;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast), border-color var(--transition-fast);
  font-size: var(--text-sm);
  color: var(--color-text);
}

.store-selector__item:hover {
  background: var(--color-green-50);
  border-color: var(--color-green-200);
}

.store-selector__item input[type='checkbox'] {
  width: auto;
  margin: 0;
  accent-color: var(--color-primary);
}
</style>
