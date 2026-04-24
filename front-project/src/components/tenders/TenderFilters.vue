<template>
  <div class="tender-filters">
    <div class="filter-search">
      <AppIcon name="search" :size="14" class="filter-search__icon" />
      <input
        class="app-input filter-search__input"
        placeholder="Пошук за назвою або ID"
        :value="search"
        @input="search = $event.target.value"
      />
    </div>

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
import { ref } from 'vue'
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'TenderFilters',
  components: { AppIcon },
  props: {
    modelValue: { type: Object, required: true },
  },
  emits: ['update:modelValue'],
  setup() {
    const search = ref('')
    return { search }
  },
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
  flex-wrap: wrap;
  gap: var(--space-2);
  align-items: flex-end;
}

.filter-search {
  position: relative;
  flex: 1;
  min-width: 240px;
  max-width: 420px;
}

.filter-search__icon {
  position: absolute;
  left: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-tertiary);
  pointer-events: none;
}

.filter-search__input {
  height: 36px;
  padding-left: 34px;
  font-size: var(--text-base);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.filter-label {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
}

.filter-select {
  height: 36px;
  padding: 0 var(--space-6) 0 var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--text-base);
  font-family: var(--font-body);
  cursor: pointer;
  transition: border-color var(--transition-fast);
  min-width: 140px;
  appearance: none;
  background-image: linear-gradient(45deg, transparent 50%, currentColor 50%),
                    linear-gradient(135deg, currentColor 50%, transparent 50%);
  background-position: calc(100% - 16px) 14px, calc(100% - 12px) 14px;
  background-size: 4px 4px;
  background-repeat: no-repeat;
  color: var(--color-text);
}

.filter-select:focus {
  outline: none;
  border-color: var(--color-slate-900);
  box-shadow: 0 0 0 3px rgb(15 23 42 / 0.08);
}

[data-theme="dark"] .filter-select:focus {
  border-color: var(--color-slate-300);
  box-shadow: 0 0 0 3px rgb(241 245 249 / 0.12);
}
</style>
