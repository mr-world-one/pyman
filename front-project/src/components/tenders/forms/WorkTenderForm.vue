<template>
  <div class="tender-form">
    <h3>Роботи</h3>

    <div v-for="(item, i) in items" :key="i" class="item-card">
      <div class="item-header">
        <span class="item-num">#{{ i + 1 }}</span>
        <button class="item-remove" @click="removeItem(i)" v-if="items.length > 1">&times;</button>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Назва роботи *</label>
          <input class="app-input" v-model="item.name" placeholder="Капітальний ремонт покрівлі" required />
        </div>
        <div class="field">
          <label>Тип роботи *</label>
          <input class="app-input" v-model="item.work_type" placeholder="будівництво" required />
        </div>
        <div class="field field-sm">
          <label>Кількість *</label>
          <input class="app-input" type="number" v-model.number="item.quantity" min="0" step="any" required />
        </div>
        <div class="field field-sm">
          <label>Одиниця *</label>
          <input class="app-input" v-model="item.unit_name" placeholder="м2" required />
        </div>
        <div class="field field-sm">
          <label>Ціна за од. *</label>
          <input class="app-input" type="number" v-model.number="item.unit_price" min="0" step="0.01" required />
        </div>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Адреса об'єкта *</label>
          <input class="app-input" v-model="item.object_address" placeholder="м. Київ, вул. Хрещатик 1" required />
        </div>
        <div class="field field-sm">
          <label>Тривалість (днів) *</label>
          <input class="app-input" type="number" v-model.number="item.estimated_duration_days" min="1" required />
        </div>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Технічні специфікації</label>
          <input class="app-input" v-model="item.technical_specs" />
        </div>
        <div class="field field-sm">
          <label>Дозвіл</label>
          <select class="app-input" v-model="item.permit_required">
            <option :value="null">—</option>
            <option :value="true">Потрібен</option>
            <option :value="false">Не потрібен</option>
          </select>
        </div>
        <div class="field field-sm">
          <label>Субпідряд</label>
          <select class="app-input" v-model="item.subcontracting_allowed">
            <option :value="null">—</option>
            <option :value="true">Дозволено</option>
            <option :value="false">Заборонено</option>
          </select>
        </div>
        <div class="field field-sm">
          <label>Матеріали вкл.</label>
          <select class="app-input" v-model="item.materials_included">
            <option :value="null">—</option>
            <option :value="true">Так</option>
            <option :value="false">Ні</option>
          </select>
        </div>
        <div class="field field-sm">
          <label>Гарантія (міс.)</label>
          <input class="app-input" type="number" v-model.number="item.warranty_months" min="0" />
        </div>
      </div>
    </div>

    <button class="add-item-btn" @click="addItem">+ Додати роботу</button>
  </div>
</template>

<script>
export default {
  name: 'WorkTenderForm',
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
          name: '', work_type: '', quantity: 1, unit_name: 'м2', unit_price: 0,
          object_address: '', estimated_duration_days: 30, technical_specs: '',
          permit_required: null, subcontracting_allowed: null,
          materials_included: null, warranty_months: null,
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
.tender-form h3 { font-size: var(--text-lg); font-weight: var(--font-bold); color: var(--color-heading); margin-bottom: var(--space-4); }
.item-card { background: var(--color-gray-50); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-4); margin-bottom: var(--space-3); }
.item-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-3); }
.item-num { font-size: var(--text-sm); font-weight: var(--font-bold); color: var(--color-warning); }
.item-remove { background: none; border: none; font-size: var(--text-xl); color: var(--color-danger); cursor: pointer; padding: 0; line-height: 1; }
.item-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: var(--space-3); margin-bottom: var(--space-2); }
.field { display: flex; flex-direction: column; gap: 0.3rem; }
.field-sm { max-width: 140px; }
.field label { font-size: var(--text-xs); font-weight: var(--font-semibold); color: var(--color-text-secondary); }
.add-item-btn { display: block; width: 100%; padding: var(--space-3); border: 2px dashed var(--color-warning); border-radius: var(--radius-md); background: transparent; color: var(--color-warning); font-size: var(--text-sm); font-weight: var(--font-semibold); cursor: pointer; transition: background var(--transition-fast); }
.add-item-btn:hover { background: var(--color-warning-bg); }
</style>
