<template>
  <div class="xpath-page">
    <div class="xpath-container">
      <h1>Керування X-Path</h1>
      <div class="form-type-buttons">
        <button @click="formType = 'add'" :class="{ active: formType === 'add' }">Додати</button>
        <button @click="formType = 'edit'" :class="{ active: formType === 'edit' }">Редагувати</button>
        <button @click="formType = 'delete'" :class="{ active: formType === 'delete' }">Видалити</button>
      </div>

      <div v-if="formType === 'add'">
        <h2>Додати X-Path</h2>
        <form @submit.prevent="handleAdd" class="xpath-form">
          <div class="form-group">
            <label for="shop-name">Назва магазину</label>
            <input type="text" id="shop-name" v-model="formData.name" placeholder="Введіть назву магазину" required />
          </div>
          <div class="form-group">
            <label for="shop-url">Shop URL</label>
            <input type="url" id="shop-url" v-model="formData.url" placeholder="Введіть посилання на сайт" required />
          </div>
          <div class="form-group">
            <label for="title-xpath">Title X-Path</label>
            <input type="text" id="title-xpath" v-model="formData.title_xpath" placeholder="Введіть X-Path для заголовка" required />
          </div>
          <div class="form-group">
            <label for="available-xpath">Available X-Path</label>
            <input type="text" id="available-xpath" v-model="formData.available_xpath" placeholder="Введіть X-Path для наявності" required />
          </div>
          <div class="form-group">
            <label for="price-xpath">Price X-Path</label>
            <input type="text" id="price-xpath" v-model="formData.price_xpath" placeholder="Введіть X-Path для ціни" required />
          </div>
          <div class="form-group">
            <label for="price-without-sale-xpath">Price Without Sale X-Path</label>
            <input type="text" id="price-without-sale-xpath" v-model="formData.price_without_sale_xpath" placeholder="Введіть X-Path для ціни без знижки" required />
          </div>
          <div class="form-group">
            <label for="price-on-sale-xpath">Price On Sale X-Path</label>
            <input type="text" id="price-on-sale-xpath" v-model="formData.price_on_sale_xpath" placeholder="Введіть X-Path для ціни зі знижкою" required />
          </div>
          <button type="submit">Додати X-Path</button>
        </form>
      </div>

      <div v-else-if="formType === 'edit'">
        <h2>Редагувати X-Path</h2>
        <form @submit.prevent="handleEdit" class="xpath-form">
          <div class="form-group">
            <label for="shop-name-edit">Назва магазину</label>
            <input type="text" id="shop-name-edit" v-model="formData.name" placeholder="Введіть назву магазину" required />
          </div>
          <div class="form-group">
            <label for="shop-url-edit">Shop URL</label>
            <input type="url" id="shop-url-edit" v-model="formData.url" placeholder="Введіть посилання на сайт" />
          </div>
          <div class="form-group">
            <label for="title-xpath-edit">Title X-Path</label>
            <input type="text" id="title-xpath-edit" v-model="formData.title_xpath" placeholder="Введіть X-Path для заголовка" />
          </div>
          <div class="form-group">
            <label for="available-xpath-edit">Available X-Path</label>
            <input type="text" id="available-xpath-edit" v-model="formData.available_xpath" placeholder="Введіть X-Path для наявності" />
          </div>
          <div class="form-group">
            <label for="price-xpath-edit">Price X-Path</label>
            <input type="text" id="price-xpath-edit" v-model="formData.price_xpath" placeholder="Введіть X-Path для ціни" />
          </div>
          <div class="form-group">
            <label for="price-without-sale-xpath-edit">Price Without Sale X-Path</label>
            <input type="text" id="price-without-sale-xpath-edit" v-model="formData.price_without_sale_xpath" placeholder="Введіть X-Path для ціни без знижки" />
          </div>
          <div class="form-group">
            <label for="price-on-sale-xpath-edit">Price On Sale X-Path</label>
            <input type="text" id="price-on-sale-xpath-edit" v-model="formData.price_on_sale_xpath" placeholder="Введіть X-Path для ціни зі знижкою" />
          </div>
          <button type="submit">Редагувати X-Path</button>
        </form>
      </div>

      <div v-else-if="formType === 'delete'">
        <h2>Видалити X-Path</h2>
        <form @submit.prevent="handleDelete" class="xpath-form">
          <div class="form-group">
            <label for="shop-name-delete">Назва магазину</label>
            <input type="text" id="shop-name-delete" v-model="formData.name" placeholder="Введіть назву магазину" required />
          </div>
          <button type="submit">Видалити X-Path</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  import { ref } from 'vue'

  export default {
    name: 'Xpath',
    setup() {
      // Режим форми: 'add', 'edit', 'delete'
      const formType = ref('add')
      // Єдина форма для всіх операцій
      const formData = ref({
        name: '',
        url: '',
        title_xpath: '',
        available_xpath: '',
        price_xpath: '',
        price_without_sale_xpath: '',
        price_on_sale_xpath: ''
      })

      const handleAdd = async () => {
        try {
          const response = await fetch('http://localhost:8000/stores', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              name: formData.value.name,
              url: formData.value.url,
              title_xpath: formData.value.title_xpath,
              available_xpath: formData.value.available_xpath,
              price_xpath: formData.value.price_xpath,
              price_without_sale_xpath: formData.value.price_without_sale_xpath,
              price_on_sale_xpath: formData.value.price_on_sale_xpath
            })
          })
          const result = await response.json()
          console.log("Додавання X-Path:", result)
          alert(`Додано X-Path:\n${JSON.stringify(result, null, 2)}`)
          formData.value = { ...formData.value, name: '', url: '', title_xpath: '', available_xpath: '', price_xpath: '', price_without_sale_xpath: '', price_on_sale_xpath: '' }
        } catch (error) {
          console.error("Помилка додавання:", error)
          alert('Помилка при додаванні X-Path')
        }
      }

      const handleEdit = async () => {
        try {
          const response = await fetch(`http://localhost:8000/stores/${formData.value.name}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              url: formData.value.url || undefined,
              title_xpath: formData.value.title_xpath || undefined,
              available_xpath: formData.value.available_xpath || undefined,
              price_xpath: formData.value.price_xpath || undefined,
              price_without_sale_xpath: formData.value.price_without_sale_xpath || undefined,
              price_on_sale_xpath: formData.value.price_on_sale_xpath || undefined
            })
          })
          const result = await response.json()
          console.log("Редагування X-Path:", result)
          alert(`Редаговано X-Path для магазину: ${formData.value.name}`)
          formData.value = { ...formData.value, name: '', url: '', title_xpath: '', available_xpath: '', price_xpath: '', price_without_sale_xpath: '', price_on_sale_xpath: '' }
        } catch (error) {
          console.error("Помилка редагування:", error)
          alert('Помилка при редагуванні X-Path')
        }
      }

      const handleDelete = async () => {
        try {
          const response = await fetch(`http://localhost:8000/stores/${formData.value.name}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
          })
          const result = await response.json()
          console.log("Видалення X-Path:", result)
          alert(`Видалено X-Path для магазину: ${formData.value.name}`)
          formData.value = { ...formData.value, name: '' }
        } catch (error) {
          console.error("Помилка видалення:", error)
          alert('Помилка при видаленні X-Path')
        }
      }

      return { formType, formData, handleAdd, handleEdit, handleDelete }
    }
  }
</script>

<style scoped>
  .xpath-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
    padding-top: 100px;
  }

  .xpath-container {
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    width: 100%;
    text-align: center;
    margin: 50px auto 0 auto;
  }

    .xpath-container h1 {
      font-size: 2rem;
      color: #333;
      margin-bottom: 1.5rem;
    }

  .form-type-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

    .form-type-buttons button {
      padding: 0.5rem 1rem;
      font-size: 1rem;
      background: #ccc;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.3s ease;
    }

      .form-type-buttons button.active {
        background: linear-gradient(135deg, #41ec22, #27ac0f);
        color: #fff;
      }

  .xpath-form {
    display: flex;
    flex-direction: column;
    text-align: left;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

    .form-group label {
      display: block;
      font-weight: bold;
      margin-bottom: 0.5rem;
      color: #444;
    }

    .form-group input {
      width: 100%;
      padding: 0.75rem;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1rem;
      transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

      .form-group input:focus {
        border-color: #007bff;
        outline: none;
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
      }

  button {
    padding: 0.75rem;
    font-size: 1.1rem;
    background: linear-gradient(135deg, #41ec22, #27ac0f);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

    button:hover {
      background-color: #0056b3;
    }
</style>
