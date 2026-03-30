<template>
  <div class="tender-form">
    <h3>Послуги</h3>

    <div v-for="(item, i) in items" :key="i" class="item-card">
      <div class="item-header">
        <span class="item-num">#{{ i + 1 }}</span>
        <button class="item-remove" @click="removeItem(i)" v-if="items.length > 1">&times;</button>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Назва послуги *</label>
          <input class="app-input" v-model="item.name" placeholder="Обслуговування серверного обладнання" required />
        </div>
        <div class="field">
          <label>Тип послуги *</label>
          <input class="app-input" v-model="item.service_type" placeholder="обслуговування" required />
        </div>
        <div class="field field-sm">
          <label>Кількість *</label>
          <input class="app-input" type="number" v-model.number="item.quantity" min="0" step="any" required />
        </div>
        <div class="field field-sm">
          <label>Одиниця *</label>
          <input class="app-input" v-model="item.unit_name" placeholder="послуга" required />
        </div>
        <div class="field field-sm">
          <label>Ціна за од. *</label>
          <input class="app-input" type="number" v-model.number="item.unit_price" min="0" step="0.01" required />
        </div>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Період (початок)</label>
          <input class="app-input" type="date" v-model="item.period_start" />
        </div>
        <div class="field">
          <label>Період (кінець)</label>
          <input class="app-input" type="date" v-model="item.period_end" />
        </div>
        <div class="field">
          <label>Локація</label>
          <input class="app-input" v-model="item.location" placeholder="м. Київ" />
        </div>
      </div>

      <div class="item-grid">
        <div class="field">
          <label>Вимоги до кваліфікації</label>
          <input class="app-input" v-model="item.qualification_requirements" />
        </div>
        <div class="field">
          <label>SLA опис</label>
          <input class="app-input" v-model="item.sla_description" />
        </div>
        <div class="field field-sm">
          <label>Ліцензія</label>
          <select class="app-input" v-model="item.license_required">
            <option :value="null">—</option>
            <option :value="true">Потрібна</option>
            <option :value="false">Не потрібна</option>
          </select>
        </div>
      </div>
    </div>

    <button class="add-item-btn" @click="addItem">+ Додати послугу</button>
  </div>
</template>

<script>
export default {
  name: 'ServiceTenderForm',
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
          name: '', service_type: '', quantity: 1, unit_name: 'послуга', unit_price: 0,
          period_start: '', period_end: '', qualification_requirements: '',
          location: '', sla_description: '', license_required: null,
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
.item-num { font-size: var(--text-sm); font-weight: var(--font-bold); color: var(--color-info); }
.item-remove { background: none; border: none; font-size: var(--text-xl); color: var(--color-danger); cursor: pointer; padding: 0; line-height: 1; }
.item-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: var(--space-3); margin-bottom: var(--space-2); }
.field { display: flex; flex-direction: column; gap: 0.3rem; }
.field-sm { max-width: 140px; }
.field label { font-size: var(--text-xs); font-weight: var(--font-semibold); color: var(--color-text-secondary); }
.add-item-btn { display: block; width: 100%; padding: var(--space-3); border: 2px dashed var(--color-info); border-radius: var(--radius-md); background: transparent; color: var(--color-info); font-size: var(--text-sm); font-weight: var(--font-semibold); cursor: pointer; transition: background var(--transition-fast); }
.add-item-btn:hover { background: var(--color-info-bg); }
</style>
