<template>
  <div class="register">
    <h1>Реєстрація користувача</h1>
    <form @submit.prevent="handleRegister" class="registration-form">
      <div class="form-group">
        <label for="email">
          Email <span class="required">*</span>
        </label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="Введіть email"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">
          Password <span class="required">*</span>
        </label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Введіть пароль"
          required
        />
      </div>
      <button type="submit">Зареєструватися!</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'RegistrationView',
  setup() {
    const username = ref('')
    const email = ref('')
    const password = ref('')

    const handleRegister = () => {
      // Тут можна додати логіку реєстрації (наприклад, звернення до API)
      alert(`Користувач ${username.value} зареєстрований!`)
      // Очистка полів форми (розкоментуйте ці рядки, якщо потрібне очищення)
      // username.value = ''
      // email.value = ''
      // password.value = ''
    }

    return { username, email, password, handleRegister }
  },
}
</script>


<style scoped>
.register {
  max-width: 500px;
  margin: 50px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Raleway', sans-serif;
}

.register h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2rem;
  color: #333;
}

.registration-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 5px;
  display: block;
  color: #444;
}

.required {
  color: red;
  margin-left: 4px;
}

input {
  width: 100%;
  padding: 12px 15px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}

button {
  padding: 12px 15px;
  font-size: 1.1rem;
  background-color: #007bff;
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
