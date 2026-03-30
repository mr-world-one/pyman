<template>
  <div class="tender-create-page">
    <div class="tender-create-container">
      <h1>Створити тендер</h1>

      <form @submit.prevent="handleSubmit">
        <div class="form-section">
          <div class="form-grid">
            <div class="field">
              <label>Тип тендера *</label>
              <select class="app-input" v-model="form.tender_type" required>
                <option value="product">Товари</option>
                <option value="service">Послуги</option>
                <option value="work">Роботи</option>
              </select>
            </div>
            <div class="field">
              <label>Prozorro ID *</label>
              <input class="app-input" v-model.trim="form.prozorro_id" placeholder="UA-2024-01-01-000001-a" required />
            </div>
          </div>

          <div class="field">
            <label>Назва тендеру *</label>
            <input class="app-input" v-model.trim="form.title" placeholder="Закупівля продуктів харчування" required />
          </div>

          <div class="field">
            <label>Опис</label>
            <textarea class="app-input app-textarea" v-model="form.description" rows="3" placeholder="Детальний опис тендеру..."></textarea>
          </div>

          <div class="form-grid">
            <div class="field">
              <label>Замовник</label>
              <input class="app-input" v-model.trim="form.customer_name" placeholder="Назва організації" />
            </div>
            <div class="field">
              <label>Регіон</label>
              <input class="app-input" v-model.trim="form.region" placeholder="Київська область" />
            </div>
            <div class="field">
              <label>Очікувана вартість</label>
              <input class="app-input" type="number" v-model.number="form.expected_cost" min="0" step="0.01" />
            </div>
            <div class="field">
              <label>Загальна сума *</label>
              <input class="app-input" type="number" v-model.number="form.total_amount" min="0" step="0.01" required />
            </div>
          </div>

          <div v-if="form.tender_type === 'product'" class="field">
            <label>
              <input type="checkbox" v-model="form.warranty_required" />
              Гарантія обов'язкова
            </label>
          </div>
          <div v-if="form.tender_type === 'service'" class="field">
            <label>
              <input type="checkbox" v-model="form.requires_license" />
              Ліцензія обов'язкова
            </label>
          </div>
          <div v-if="form.tender_type === 'work'" class="field">
            <label>Проектна документація</label>
            <input class="app-input" v-model="form.project_documentation" placeholder="Посилання або опис" />
          </div>
        </div>

        <div class="form-section">
          <ProductTenderForm v-if="form.tender_type === 'product'" v-model="form.items" />
          <ServiceTenderForm v-if="form.tender_type === 'service'" v-model="form.items" />
          <WorkTenderForm v-if="form.tender_type === 'work'" v-model="form.items" />
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <div class="form-actions">
          <AppButton variant="ghost" type="button" @click="$router.back()">Скасувати</AppButton>
          <AppButton type="submit" :disabled="loading">
            {{ loading ? 'Створюємо...' : 'Створити тендер' }}
          </AppButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useTendersStore } from '@/stores/tenders'
import AppButton from '@/components/AppButton.vue'
import ProductTenderForm from '@/components/tenders/forms/ProductTenderForm.vue'
import ServiceTenderForm from '@/components/tenders/forms/ServiceTenderForm.vue'
import WorkTenderForm from '@/components/tenders/forms/WorkTenderForm.vue'

const DEFAULT_ITEMS = {
  product: [{ name: '', quantity: 1, unit_name: 'шт', unit_price: 0, dk_code: '', dstu_gost: '', brand: '', weight_per_unit_g: null, specifications: '', delivery_address: '', delivery_deadline: '', shelf_life_days: null }],
  service: [{ name: '', service_type: '', quantity: 1, unit_name: 'послуга', unit_price: 0, period_start: '', period_end: '', qualification_requirements: '', location: '', sla_description: '', license_required: null }],
  work: [{ name: '', work_type: '', quantity: 1, unit_name: 'м2', unit_price: 0, object_address: '', estimated_duration_days: 30, technical_specs: '', permit_required: null, subcontracting_allowed: null, materials_included: null, warranty_months: null }],
}

export default {
  name: 'TenderCreateView',
  components: { AppButton, ProductTenderForm, ServiceTenderForm, WorkTenderForm },
  setup() {
    const router = useRouter()
    const store = useTendersStore()
    const loading = ref(false)
    const error = ref(null)

    const form = ref({
      tender_type: 'product',
      prozorro_id: '',
      title: '',
      description: '',
      customer_name: '',
      region: '',
      expected_cost: null,
      total_amount: 0,
      warranty_required: false,
      requires_license: false,
      project_documentation: '',
      items: [...DEFAULT_ITEMS.product.map((i) => ({ ...i }))],
    })

    watch(() => form.value.tender_type, (newType) => {
      form.value.items = [...DEFAULT_ITEMS[newType].map((i) => ({ ...i }))]
    })

    const handleSubmit = async () => {
      loading.value = true
      error.value = null

      const payload = {
        tender_type: form.value.tender_type,
        prozorro_id: form.value.prozorro_id,
        title: form.value.title,
        description: form.value.description || null,
        customer_name: form.value.customer_name || null,
        region: form.value.region || null,
        expected_cost: form.value.expected_cost || null,
        total_amount: form.value.total_amount,
        items: form.value.items,
      }

      if (form.value.tender_type === 'product') {
        payload.warranty_required = form.value.warranty_required
      } else if (form.value.tender_type === 'service') {
        payload.requires_license = form.value.requires_license
      } else if (form.value.tender_type === 'work') {
        payload.project_documentation = form.value.project_documentation || null
      }

      try {
        const tender = await store.createTender(payload)
        router.push(`/tenders/${tender.id}`)
      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Помилка створення'
      } finally {
        loading.value = false
      }
    }

    return { form, loading, error, handleSubmit }
  },
}
</script>

<style scoped>
.tender-create-page {
  display: flex;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  padding-top: 100px;
}

.tender-create-container {
  max-width: 900px;
  width: 100%;
}

.tender-create-container h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin-bottom: var(--space-6);
}

.form-section {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  margin-bottom: var(--space-4);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  margin-bottom: var(--space-2);
}

.field label {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-secondary);
}

.app-textarea {
  resize: vertical;
  min-height: 80px;
}

.error-message {
  color: var(--color-danger);
  background: var(--color-danger-light);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-4);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
}
</style>
