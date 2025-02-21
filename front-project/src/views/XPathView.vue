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
            <label for="shop-url">Shop URL</label>
            <input type="url" id="shop-url" v-model="shopUrl" placeholder="Введіть посилання на сайт" required />
          </div>
          <div class="form-group">
            <label for="xpath">X-Path</label>
            <input type="text" id="xpath" v-model="xpath" placeholder="Введіть X-Path" required />
          </div>
          <button type="submit">Додати X-Path</button>
        </form>
      </div>

      <div v-else-if="formType === 'edit'">
        <h2>Редагувати X-Path</h2>
        <form @submit.prevent="handleEdit" class="xpath-form">
          <div class="form-group">
            <label for="shop-name-edit">Назва магазину</label>
            <input type="text" id="shop-name-edit" v-model="shopName" placeholder="Введіть назву магазину" required />
          </div>
          <button type="submit">Редагувати X-Path</button>
        </form>
      </div>

      <div v-else-if="formType === 'delete'">
        <h2>Видалити X-Path</h2>
        <form @submit.prevent="handleDelete" class="xpath-form">
          <div class="form-group">
            <label for="shop-name-delete">Назва магазину</label>
            <input type="text" id="shop-name-delete" v-model="shopName" placeholder="Введіть назву магазину" required />
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
      // Поля для форми додавання
      const shopUrl = ref('')
      const xpath = ref('')
      // Поле для редагування та видалення (назва магазину)
      const shopName = ref('')

      const handleAdd = () => {
        console.log("Додавання X-Path:")
        console.log("Shop URL:", shopUrl.value)
        console.log("X-Path:", xpath.value)
        alert(`Додано X-Path:\nShop URL: ${shopUrl.value}\nX-Path: ${xpath.value}`)
        // Очистка полів форми
        shopUrl.value = ''
        xpath.value = ''
      }
      const handleEdit = () => {
        console.log("Редагування X-Path для магазину:", shopName.value)
        alert(`Редагувати X-Path для магазину: ${shopName.value}`)
        shopName.value = ''
      }
      const handleDelete = () => {
        console.log("Видалення X-Path для магазину:", shopName.value)
        alert(`Видалити X-Path для магазину: ${shopName.value}`)
        shopName.value = ''
      }

      return { formType, shopUrl, xpath, shopName, handleAdd, handleEdit, handleDelete }
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
