<template>
  <div class="register-page">
    <div class="register">
      <h1>Реєстрація користувача</h1>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <form @submit.prevent="handleRegister" class="registration-form">
        <div class="form-group">
          <label for="name">
            Name <span class="required">*</span>
          </label>
          <input
            type="text"
            id="name"
            v-model="name"
            placeholder="Введіть ім'я"
            required
          />
        </div>
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
  </div>
</template>

<script>
import { ref } from 'vue'
import { authService } from '@/api/authService'
import { useRouter } from 'vue-router'

export default {
  name: 'RegistrationView',
  setup() {
    const router = useRouter()
    const name = ref('')
    const email = ref('')
    const password = ref('')
    const error = ref('')

    const handleRegister = async () => {
      try {
        error.value = '' // Clear previous errors
        const response = await authService.register({
          name: name.value,
          email: email.value,
          password: password.value
        })
        console.log('Registration successful:', response)
        
        // After successful registration, login the user
        const loginResponse = await authService.login(email.value, password.value)
        localStorage.setItem('token', loginResponse.access_token)
        router.push('/')
      } catch (err) {
        console.error('Registration error:', err)
        error.value = err.response?.data?.detail || 'Registration failed'
      }
    }

    return { 
      name,
      email, 
      password, 
      error, 
      handleRegister 
    }
  }
}
</script>

<style scoped>

.register-page {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 100px;
    min-height: 100vh;
}

.register {
  max-width: 500px;
  width: 100%;
  margin: 0 auto;
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
  background: linear-gradient(135deg, #41ec22, #27ac0f);
  color: white;
  padding: 0.8rem;
  font-size: 1.1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background-color: #0056b3;
}
.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 20px;
  text-align: center;
}

button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}
</style>
