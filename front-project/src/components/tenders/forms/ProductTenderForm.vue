<template>
  <div class="tender-form">
    <h3>Товари</h3>

    <div v-for="(item, i) in items" :key="i" class="item-card">
      <div class="item-header">
        <span class="item-num">#{{ i + 1 }}</span>
        <button class="item-remove" @click="removeItem(i)" v-if="items.length > 1">&times;</button>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Назва товару *</label>
          <input class="app-input" v-model="item.name" placeholder="Молоко пастеризоване 2.5%" required />
        </div>
        <div class="field field-sm">
          <label>Кількість *</label>
          <input class="app-input" type="number" v-model.number="item.quantity" min="0" step="any" required />
        </div>
        <div class="field field-sm">
          <label>Одиниця *</label>
          <input class="app-input" v-model="item.unit_name" placeholder="шт" required />
        </div>
        <div class="field field-sm">
          <label>Ціна за од. *</label>
          <input class="app-input" type="number" v-model.number="item.unit_price" min="0" step="0.01" required />
        </div>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Код ДК 021:2015</label>
          <input class="app-input" v-model="item.dk_code" placeholder="15500000-3" />
        </div>
        <div class="field">
          <label>ДСТУ/ГОСТ</label>
          <input class="app-input" v-model="item.dstu_gost" placeholder="ДСТУ 4399:2005" />
        </div>
        <div class="field">
          <label>Бренд</label>
          <input class="app-input" v-model="item.brand" placeholder="Галичина" />
        </div>
        <div class="field field-sm">
          <label>Вага (г)</label>
          <input class="app-input" type="number" v-model.number="item.weight_per_unit_g" min="0" />
        </div>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Специфікація</label>
          <input class="app-input" v-model="item.specifications" placeholder="Технічні вимоги..." />
        </div>
        <div class="field">
          <label>Адреса доставки</label>
          <input class="app-input" v-model="item.delivery_address" />
        </div>
        <div class="field field-sm">
          <label>Термін доставки</label>
          <input class="app-input" v-model="item.delivery_deadline" placeholder="10 днів" />
        </div>
        <div class="field field-sm">
          <label>Термін придатності (дн.)</label>
          <input class="app-input" type="number" v-model.number="item.shelf_life_days" min="0" />
        </div>
      </div>
    </div>

    <button class="add-item-btn" @click="addItem">+ Додати товар</button>
  </div>
</template>

<script>
export default {
  name: 'ProductTenderForm',
  props: {
    modelValue: { type: Array, required: true },
  },
  emits: ['update:modelValue'],
  computed: {
    items: {
      get() { return this.modelValue },
      set(val) { this.$emit('update:modelValue', val) },
    },
  },
  methods: {
    addItem() {
      this.items = [
        ...this.items,
        {
          name: '', quantity: 1, unit_name: 'шт', unit_price: 0,
          dk_code: '', dstu_gost: '', brand: '', weight_per_unit_g: null,
          specifications: '', delivery_address: '', delivery_deadline: '', shelf_life_days: null,
        },
      ]
    },
    removeItem(index) {
      this.items = this.items.filter((_, i) => i !== index)
    },
  },
}
</script>

<style scoped>
.tender-form h3 {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-4);
}

.item-card {
  background: var(--color-gray-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  margin-bottom: var(--space-3);
}

.item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.item-num {
  font-size: var(--text-sm);
  font-weight: var(--font-bold);
  color: var(--color-green-600);
}

.item-remove {
  background: none;
  border: none;
  font-size: var(--text-xl);
  color: var(--color-danger);
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.item-remove:hover {
  color: var(--color-red-700);
}

.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: var(--space-3);
  margin-bottom: var(--space-2);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.field-sm {
  max-width: 140px;
}

.field label {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  color: var(--color-text-secondary);
}

.add-item-btn {
  display: block;
  width: 100%;
  padding: var(--space-3);
  border: 2px dashed var(--color-green-300);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-green-600);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  cursor: pointer;
  transition: background var(--transition-fast), border-color var(--transition-fast);
}

.add-item-btn:hover {
  background: var(--color-green-50);
  border-color: var(--color-green-500);
}
</style>
