<template>
  <div class="signin-page">
    <div class="signin">
      <h1>Увійдіть у свій акаунт</h1>
      <div v-if="error" class="error-message">{{ error }}</div>
      <form class="signin-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Електронна пошта<span class="required">*</span></label>
          <input type="email" id="email" v-model="email" placeholder="Введіть вашу електронну пошту" required />
        </div>
        <div class="form-group">
          <label for="password">Пароль<span class="required">*</span></label>
          <input type="password" id="password" v-model="password" placeholder="Введіть ваш пароль" required />
        </div>
        <button type="submit" :disabled="loading" @click="console.log('Button clicked')">
          {{ loading ? 'Вхід...' : 'Увійти' }}
        </button>
      </form>
      <p class="register-link">
        Ще не зареєстровані? <router-link to="/register">Зареєструйтеся!</router-link>
      </p>
    </div>
  </div>
</template>

<script>
  import { ref } from 'vue';
  import { authService } from '@/api/authService';
  import { useRouter } from 'vue-router';

  export default {
    name: 'SignIn',
    setup() {
      const router = useRouter();
      const email = ref('');
      const password = ref('');
      const error = ref('');
      const loading = ref(false);

      const handleLogin = async () => {
        console.log('handleLogin called with:', { email: email.value, password: password.value });
        if (loading.value) return; // Запобігаємо повторним клікам
        loading.value = true;

        try {
          error.value = ''; // Очищаємо попередні помилки
          const response = await authService.login(email.value, password.value);
          console.log('Успішний вхід, response:', response);
          if (response.access_token) {
            console.log('Token saved, redirecting to /');
            router.push('/');
          } else {
            throw new Error('No access token in response');
          }
        } catch (err) {
          console.error('Помилка входу:', err);
          error.value = err.response?.data?.detail || err.message || 'Помилка входу. Перевірте email або пароль';
        } finally {
          loading.value = false;
        }
      };

      return {
        email,
        password,
        error,
        loading,
        handleLogin
      };
    }
  };
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@300;600;700&display=swap');

  .signin-page {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 100px;
    min-height: 100vh;
  }

  .signin {
    max-width: 500px;
    width: 100%;
    margin: 0 auto;
    padding: 30px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    font-family: 'Raleway', sans-serif;
  }

    .signin h1 {
      text-align: center;
      margin-bottom: 20px;
      font-size: 2rem;
      color: #333;
    }

  .signin-form {
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

    button:hover:not(:disabled) {
      background-color: #0056b3;
    }

    button:disabled {
      background: #cccccc;
      cursor: not-allowed;
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

  .register-link {
    margin-top: 1.5rem;
    font-size: 1rem;
    text-align: center;
  }

    .register-link a {
      color: #41ec22;
      text-decoration: none;
      font-weight: bold;
    }

      .register-link a:hover {
        text-decoration: underline;
      }
</style>
