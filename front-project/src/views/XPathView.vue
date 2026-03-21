<template>
  <PageContainer max-width="md" centered>
    <CardPanel>
      <h1 class="page-title">Керування X-Path</h1>
      <div class="tab-buttons">
        <AppButton
          :variant="formType === 'add' ? 'primary' : 'ghost'"
          size="sm"
          @click="formType = 'add'"
        >
          Додати
        </AppButton>
        <AppButton
          :variant="formType === 'edit' ? 'primary' : 'ghost'"
          size="sm"
          @click="formType = 'edit'"
        >
          Редагувати
        </AppButton>
        <AppButton
          :variant="formType === 'delete' ? 'danger' : 'ghost'"
          size="sm"
          @click="formType = 'delete'"
        >
          Видалити
        </AppButton>
      </div>

      <div v-if="formType === 'add'">
        <h2 class="section-subtitle">Додати X-Path</h2>
        <form @submit.prevent="handleAdd" class="xpath-form">
          <FormGroup label="Назва магазину" html-for="shop-name" required>
            <input type="text" id="shop-name" v-model="formData.name" class="app-input" placeholder="Введіть назву магазину" required />
          </FormGroup>
          <FormGroup label="URL магазину" html-for="shop-url" required>
            <input type="url" id="shop-url" v-model="formData.url" class="app-input" placeholder="Введіть посилання на сайт" required />
          </FormGroup>
          <FormGroup label="Title X-Path" html-for="title-xpath" required>
            <input type="text" id="title-xpath" v-model="formData.title_xpath" class="app-input" placeholder="Введіть X-Path для заголовка" required />
          </FormGroup>
          <FormGroup label="Available X-Path" html-for="available-xpath" required>
            <input type="text" id="available-xpath" v-model="formData.available_xpath" class="app-input" placeholder="Введіть X-Path для наявності" required />
          </FormGroup>
          <FormGroup label="Price X-Path" html-for="price-xpath" required>
            <input type="text" id="price-xpath" v-model="formData.price_xpath" class="app-input" placeholder="Введіть X-Path для ціни" required />
          </FormGroup>
          <FormGroup label="Price Without Sale X-Path" html-for="price-without-sale-xpath" required>
            <input type="text" id="price-without-sale-xpath" v-model="formData.price_without_sale_xpath" class="app-input" placeholder="Введіть X-Path для ціни без знижки" required />
          </FormGroup>
          <FormGroup label="Price On Sale X-Path" html-for="price-on-sale-xpath" required>
            <input type="text" id="price-on-sale-xpath" v-model="formData.price_on_sale_xpath" class="app-input" placeholder="Введіть X-Path для ціни зі знижкою" required />
          </FormGroup>
          <AppButton type="submit" size="lg" style="width: 100%">Додати X-Path</AppButton>
        </form>
      </div>

      <div v-else-if="formType === 'edit'">
        <h2 class="section-subtitle">Редагувати X-Path</h2>
        <form @submit.prevent="handleEdit" class="xpath-form">
          <FormGroup label="Назва магазину" html-for="shop-name-edit" required>
            <input type="text" id="shop-name-edit" v-model="formData.name" class="app-input" placeholder="Введіть назву магазину" required />
          </FormGroup>
          <FormGroup label="URL магазину" html-for="shop-url-edit">
            <input type="url" id="shop-url-edit" v-model="formData.url" class="app-input" placeholder="Введіть посилання на сайт" />
          </FormGroup>
          <FormGroup label="Title X-Path" html-for="title-xpath-edit">
            <input type="text" id="title-xpath-edit" v-model="formData.title_xpath" class="app-input" placeholder="Введіть X-Path для заголовка" />
          </FormGroup>
          <FormGroup label="Available X-Path" html-for="available-xpath-edit">
            <input type="text" id="available-xpath-edit" v-model="formData.available_xpath" class="app-input" placeholder="Введіть X-Path для наявності" />
          </FormGroup>
          <FormGroup label="Price X-Path" html-for="price-xpath-edit">
            <input type="text" id="price-xpath-edit" v-model="formData.price_xpath" class="app-input" placeholder="Введіть X-Path для ціни" />
          </FormGroup>
          <FormGroup label="Price Without Sale X-Path" html-for="price-without-sale-xpath-edit">
            <input type="text" id="price-without-sale-xpath-edit" v-model="formData.price_without_sale_xpath" class="app-input" placeholder="Введіть X-Path для ціни без знижки" />
          </FormGroup>
          <FormGroup label="Price On Sale X-Path" html-for="price-on-sale-xpath-edit">
            <input type="text" id="price-on-sale-xpath-edit" v-model="formData.price_on_sale_xpath" class="app-input" placeholder="Введіть X-Path для ціни зі знижкою" />
          </FormGroup>
          <AppButton type="submit" size="lg" style="width: 100%">Редагувати X-Path</AppButton>
        </form>
      </div>

      <div v-else-if="formType === 'delete'">
        <h2 class="section-subtitle">Видалити X-Path</h2>
        <form @submit.prevent="handleDelete" class="xpath-form">
          <FormGroup label="Назва магазину" html-for="shop-name-delete" required>
            <input type="text" id="shop-name-delete" v-model="formData.name" class="app-input" placeholder="Введіть назву магазину" required />
          </FormGroup>
          <AppButton type="submit" variant="danger" size="lg" style="width: 100%">Видалити X-Path</AppButton>
        </form>
      </div>
    </CardPanel>
  </PageContainer>
</template>

<script>
import { ref } from 'vue'
import { apiClient } from '@/api/config'
import { useToast } from '@/composables/useToast'
import PageContainer from '@/components/PageContainer.vue'
import CardPanel from '@/components/CardPanel.vue'
import FormGroup from '@/components/FormGroup.vue'
import AppButton from '@/components/AppButton.vue'

export default {
  name: 'XPathView',
  components: { PageContainer, CardPanel, FormGroup, AppButton },
  setup() {
    const toast = useToast()
    const formType = ref('add')
    const formData = ref({
      name: '',
      url: '',
      title_xpath: '',
      available_xpath: '',
      price_xpath: '',
      price_without_sale_xpath: '',
      price_on_sale_xpath: '',
    })

    const resetForm = () => {
      formData.value = {
        name: '',
        url: '',
        title_xpath: '',
        available_xpath: '',
        price_xpath: '',
        price_without_sale_xpath: '',
        price_on_sale_xpath: '',
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
      } catch (error) {
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
      } catch (error) {
        toast.error('Помилка при редагуванні X-Path')
      }
    }

    const handleDelete = async () => {
      try {
        await apiClient.delete(`/xpath/store/${formData.value.name}`)
        toast.success(`X-Path для "${formData.value.name}" видалено`)
        resetForm()
      } catch (error) {
        toast.error('Помилка при видаленні X-Path')
      }
    }

    return { formType, formData, handleAdd, handleEdit, handleDelete }
  },
}
</script>

<style scoped>
.page-title {
  text-align: center;
  font-size: var(--text-2xl);
  margin-bottom: var(--space-6);
}

.tab-buttons {
  display: flex;
  justify-content: center;
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.section-subtitle {
  font-size: var(--text-lg);
  color: var(--color-heading);
  margin-bottom: var(--space-4);
  text-align: center;
}

.xpath-form {
  display: flex;
  flex-direction: column;
}
</style>
