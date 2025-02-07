<template>
  <div class="xpath-page">
    <div class="xpath-container">
      <h1>Додай X-Path</h1>
      <form @submit.prevent="handleSubmit" class="xpath-form">
        <div class="form-group">
          <label for="shop-url">Shop URL</label>
          <input type="url"
                 id="shop-url"
                 v-model="shopUrl"
                 placeholder="Enter shop website link"
                 required />
        </div>
        <div class="form-group">
          <label for="xpath">X-Path</label>
          <input type="text"
                 id="xpath"
                 v-model="xpath"
                 placeholder="Enter X-Path"
                 required />
        </div>
        <button type="submit">{{ isEdit ? 'Update' : 'Add' }} X-Path</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'XpathForm',
  setup() {
    const shopUrl = ref('')
    const xpath = ref('')
    const isEdit = ref(false)

    const handleSubmit = () => {
      // Тут можна додати логіку додавання/редагування X-Path (наприклад, API-запит)
      console.log("Shop URL:", shopUrl.value)
      console.log("X-Path:", xpath.value)
      alert(`Shop: ${shopUrl.value}\nX-Path: ${xpath.value}`)

      // Очистка полів (якщо потрібно)
      shopUrl.value = ''
      xpath.value = ''
      isEdit.value = false
    }

    return { shopUrl, xpath, isEdit, handleSubmit }
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
  }

    .xpath-container h1 {
      font-size: 2rem;
      color: #333;
      margin-bottom: 1.5rem;
    }

  .xpath-form {
    display: flex;
    flex-direction: column;
  }

  .form-group {
    margin-bottom: 1.5rem;
    text-align: left;
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
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
        outline: none;
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
