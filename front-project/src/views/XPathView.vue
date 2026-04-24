<template>
  <div class="xpath">
    <div class="xpath__inner">
      <div class="page-header">
        <div>
          <h1 class="page-header__title">X-Path селектори</h1>
          <p class="page-header__subtitle">
            Керування селекторами для парсингу сторінок магазинів.
          </p>
        </div>
        <div class="page-header__chip">
          <AppIcon name="shield" :size="14" /> admin
        </div>
      </div>

      <div class="xpath-card">
        <div class="xpath-tabs">
          <button
            :class="['xpath-tab', { 'is-active': formType === 'add' }]"
            type="button"
            @click="formType = 'add'"
          >
            Додати
          </button>
          <button
            :class="['xpath-tab', { 'is-active': formType === 'edit' }]"
            type="button"
            @click="formType = 'edit'"
          >
            Редагувати
          </button>
          <button
            :class="['xpath-tab xpath-tab--danger', { 'is-active': formType === 'delete' }]"
            type="button"
            @click="formType = 'delete'"
          >
            Видалити
          </button>
        </div>

        <!-- ADD -->
        <div v-if="formType === 'add'" class="xpath-body">
          <form @submit.prevent="handleAdd" class="xpath-form">
            <FormGroup label="Назва магазину" html-for="shop-name" required>
              <input id="shop-name" type="text" v-model="formData.name" class="app-input" placeholder="Rozetka" required />
            </FormGroup>
            <FormGroup label="URL магазину" html-for="shop-url" required>
              <input id="shop-url" type="url" v-model="formData.url" class="app-input mono" placeholder="https://rozetka.com.ua" required />
            </FormGroup>
            <FormGroup label="Title X-Path" html-for="title-xpath" required>
              <input id="title-xpath" type="text" v-model="formData.title_xpath" class="app-input mono" placeholder='//h1[@class="title"]/text()' required />
            </FormGroup>
            <FormGroup label="Available X-Path" html-for="available-xpath" required>
              <input id="available-xpath" type="text" v-model="formData.available_xpath" class="app-input mono" required />
            </FormGroup>
            <FormGroup label="Price X-Path" html-for="price-xpath" required>
              <input id="price-xpath" type="text" v-model="formData.price_xpath" class="app-input mono" required />
            </FormGroup>
            <FormGroup label="Price Without Sale X-Path" html-for="price-ws" required>
              <input id="price-ws" type="text" v-model="formData.price_without_sale_xpath" class="app-input mono" required />
            </FormGroup>
            <FormGroup label="Price On Sale X-Path" html-for="price-os" required>
              <input id="price-os" type="text" v-model="formData.price_on_sale_xpath" class="app-input mono" required />
            </FormGroup>
            <div class="xpath-actions">
              <AppButton type="submit">Зберегти</AppButton>
              <AppButton type="button" variant="secondary">Тестувати</AppButton>
            </div>
          </form>
        </div>

        <!-- EDIT -->
        <div v-else-if="formType === 'edit'" class="xpath-body">
          <form @submit.prevent="handleEdit" class="xpath-form">
            <FormGroup label="Назва магазину" html-for="shop-name-edit" required>
              <input id="shop-name-edit" type="text" v-model="formData.name" class="app-input" required />
            </FormGroup>
            <FormGroup label="URL магазину" html-for="shop-url-edit">
              <input id="shop-url-edit" type="url" v-model="formData.url" class="app-input mono" />
            </FormGroup>
            <FormGroup label="Title X-Path" html-for="title-xpath-edit">
              <input id="title-xpath-edit" type="text" v-model="formData.title_xpath" class="app-input mono" />
            </FormGroup>
            <FormGroup label="Available X-Path" html-for="available-xpath-edit">
              <input id="available-xpath-edit" type="text" v-model="formData.available_xpath" class="app-input mono" />
            </FormGroup>
            <FormGroup label="Price X-Path" html-for="price-xpath-edit">
              <input id="price-xpath-edit" type="text" v-model="formData.price_xpath" class="app-input mono" />
            </FormGroup>
            <FormGroup label="Price Without Sale X-Path" html-for="price-ws-edit">
              <input id="price-ws-edit" type="text" v-model="formData.price_without_sale_xpath" class="app-input mono" />
            </FormGroup>
            <FormGroup label="Price On Sale X-Path" html-for="price-os-edit">
              <input id="price-os-edit" type="text" v-model="formData.price_on_sale_xpath" class="app-input mono" />
            </FormGroup>
            <div class="xpath-actions">
              <AppButton type="submit">Оновити</AppButton>
            </div>
          </form>
        </div>

        <!-- DELETE -->
        <div v-else-if="formType === 'delete'" class="xpath-body">
          <form @submit.prevent="handleDelete" class="xpath-form xpath-form--narrow">
            <FormGroup label="Назва магазину" html-for="shop-name-delete" required>
              <input id="shop-name-delete" type="text" v-model="formData.name" class="app-input" required />
            </FormGroup>
            <p class="xpath-warning">
              <AppIcon name="alert" :size="14" />
              Цю дію неможливо відмінити.
            </p>
            <AppButton type="submit" variant="danger">Видалити X-Path</AppButton>
          </form>
        </div>

        <!-- Preview panel shown below form on add -->
        <aside v-if="formType === 'add'" class="xpath-preview">
          <div class="xpath-preview__head">
            <span class="xpath-preview__title">
              <AppIcon name="code" :size="14" /> Прев'ю парсингу
            </span>
            <span class="xpath-preview__status">
              <span class="xpath-preview__dot"></span> 3/3 успішно
            </span>
          </div>
          <div class="xpath-preview__list mono">
            <div class="xpath-preview__row">
              <div class="xpath-preview__url">rozetka.com.ua/papir-a4-80/p123456/</div>
              <div class="xpath-preview__match">
                <span>"152 грн"</span>
                <span class="xpath-preview__result">→ 152.00</span>
              </div>
            </div>
            <div class="xpath-preview__row">
              <div class="xpath-preview__url">rozetka.com.ua/ruchka-bic/p98765/</div>
              <div class="xpath-preview__match">
                <span>"14 грн 20 коп"</span>
                <span class="xpath-preview__result">→ 14.20</span>
              </div>
            </div>
            <div class="xpath-preview__row">
              <div class="xpath-preview__url">rozetka.com.ua/papka-reg/p55432/</div>
              <div class="xpath-preview__match">
                <span>"72,90 грн"</span>
                <span class="xpath-preview__result">→ 72.90</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { apiClient } from '@/api/config'
import { useToast } from '@/composables/useToast'
import FormGroup from '@/components/FormGroup.vue'
import AppButton from '@/components/AppButton.vue'
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'XPathView',
  components: { FormGroup, AppButton, AppIcon },
  setup() {
    const toast = useToast()
    const formType = ref('add')
    const formData = ref({
      name: '', url: '', title_xpath: '', available_xpath: '',
      price_xpath: '', price_without_sale_xpath: '', price_on_sale_xpath: '',
    })

    const resetForm = () => {
      formData.value = {
        name: '', url: '', title_xpath: '', available_xpath: '',
        price_xpath: '', price_without_sale_xpath: '', price_on_sale_xpath: '',
      }
    }

    const handleAdd = async () => {
      try {
        await apiClient.post('/xpath/store/', {
          name: formData.value.name,
          url: formData.value.url,
          title_xpath: formData.value.title_xpath,
          available_xpath: formData.value.available_xpath,
          price_xpath: formData.value.price_xpath,
          price_without_sale_xpath: formData.value.price_without_sale_xpath,
          price_on_sale_xpath: formData.value.price_on_sale_xpath,
        })
        toast.success(`X-Path для "${formData.value.name}" додано успішно`)
        resetForm()
      } catch {
        toast.error('Помилка при додаванні X-Path')
      }
    }

    const handleEdit = async () => {
      try {
        await apiClient.put(`/xpath/store/${formData.value.name}`, {
          url: formData.value.url || undefined,
          title_xpath: formData.value.title_xpath || undefined,
          available_xpath: formData.value.available_xpath || undefined,
          price_xpath: formData.value.price_xpath || undefined,
          price_without_sale_xpath: formData.value.price_without_sale_xpath || undefined,
          price_on_sale_xpath: formData.value.price_on_sale_xpath || undefined,
        })
        toast.success(`X-Path для "${formData.value.name}" оновлено`)
        resetForm()
      } catch {
        toast.error('Помилка при редагуванні X-Path')
      }
    }

    const handleDelete = async () => {
      try {
        await apiClient.delete(`/xpath/store/${formData.value.name}`)
        toast.success(`X-Path для "${formData.value.name}" видалено`)
        resetForm()
      } catch {
        toast.error('Помилка при видаленні X-Path')
      }
    }

    return { formType, formData, handleAdd, handleEdit, handleDelete }
  },
}
</script>

<style scoped>
.xpath {
  padding: calc(var(--header-height) + var(--space-8)) var(--space-6) var(--space-12);
}

.xpath__inner {
  max-width: var(--container-max-width);
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.page-header__title {
  font-size: clamp(1.75rem, 3vw, 2rem);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
}

.page-header__subtitle {
  margin-top: 4px;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.page-header__chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  background: var(--color-bg-subtle);
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
}

.xpath-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}

.xpath-tabs {
  display: flex;
  gap: 4px;
  padding: 0 var(--space-2);
  border-bottom: 1px solid var(--color-border);
}

.xpath-tab {
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
}

.xpath-tab::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 2px;
  background: transparent;
  transition: background var(--transition-fast);
}

.xpath-tab:hover { color: var(--color-text); }

.xpath-tab.is-active {
  color: var(--color-heading);
  font-weight: var(--font-medium);
}

.xpath-tab.is-active::after { background: var(--color-primary); }

.xpath-tab--danger.is-active { color: var(--color-danger); }
.xpath-tab--danger.is-active::after { background: var(--color-danger); }

.xpath-body {
  padding: var(--space-6);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
}

.xpath-body .xpath-form + .xpath-preview,
.xpath-body .xpath-preview + .xpath-form { align-self: start; }

.xpath-form {
  display: flex;
  flex-direction: column;
}

.xpath-form--narrow { max-width: 420px; }

.xpath-actions {
  margin-top: var(--space-2);
  display: flex;
  gap: var(--space-2);
}

.xpath-warning {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-sm);
  color: var(--color-warning);
  padding: var(--space-2) var(--space-3);
  background: var(--color-warning-bg);
  border: 1px solid var(--color-warning-border);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-3);
}

/* Preview */
.xpath-preview {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg-subtle);
  overflow: hidden;
}

.xpath-preview__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 36px;
  padding: 0 var(--space-4);
  border-bottom: 1px solid var(--color-border);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.xpath-preview__title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.xpath-preview__status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--color-primary);
}

.xpath-preview__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
}

.xpath-preview__list {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  font-size: 12.5px;
}

.xpath-preview__row {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  padding: var(--space-3);
}

.xpath-preview__url {
  font-size: 11px;
  color: var(--color-text-secondary);
}

.xpath-preview__match {
  margin-top: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  color: var(--color-text);
}

.xpath-preview__result { color: var(--color-primary); }

@media (max-width: 900px) {
  .xpath-body { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .xpath { padding: calc(var(--header-height) + var(--space-6)) var(--space-4) var(--space-10); }
}
</style>
