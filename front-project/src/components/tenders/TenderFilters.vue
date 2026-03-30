<template>
  <div class="tender-filters">
    <div class="filter-group">
      <label class="filter-label">Тип</label>
      <select class="filter-select" :value="modelValue.tender_type" @change="update('tender_type', $event.target.value || null)">
        <option value="">Всі типи</option>
        <option value="product">Товари</option>
        <option value="service">Послуги</option>
        <option value="work">Роботи</option>
        <option value="consulting">Консалтинг</option>
        <option value="mixed">Змішаний</option>
      </select>
    </div>

    <div class="filter-group">
      <label class="filter-label">Статус</label>
      <select class="filter-select" :value="modelValue.status" @change="update('status', $event.target.value || null)">
        <option value="">Всі</option>
        <option value="active">Активні</option>
        <option value="closed">Закриті</option>
        <option value="cancelled">Скасовані</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TenderFilters',
  props: {
    modelValue: { type: Object, required: true },
  },
  emits: ['update:modelValue'],
  methods: {
    update(key, value) {
      this.$emit('update:modelValue', { ...this.modelValue, [key]: value, page: 1 })
    },
  },
}
</script>

<style scoped>
.tender-filters {
  display: flex;
  gap: var(--space-4);
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.filter-label {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-select {
  padding: 0.5rem 0.8rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--text-sm);
  font-family: var(--font-body);
  cursor: pointer;
  transition: border-color var(--transition-fast);
  min-width: 140px;
}

.filter-select:focus {
  outline: none;
  border-color: var(--color-green-500);
}
</style>
