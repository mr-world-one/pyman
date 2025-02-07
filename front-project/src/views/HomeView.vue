<template>
  <div class="home-page">
    <div class="welcome-container">
      <div class="welcome-text">
        <h1>Порівнюйте реальні ціни із вказаними у тендерах!</h1>
        <p>Приватні чи державні - немає значення. Ви можете все на нашому сайті!</p>
      </div>
    </div>
    <div class="login-box">
      <form class="login-form" @submit.prevent="login">
        <h2>Увійдіть у свій акаунт</h2>
        <input type="email" v-model="email" placeholder="Введіть вашу електронну пошту" required />
        <input type="password" v-model="password" placeholder="Введіть ваш пароль" required />
        <button type="submit">Увійти</button>
      </form>
      <p class="register-link">
        Ще не зареєстровані? <router-link to="/register">Зареєструйтеся!</router-link>
      </p>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Home',
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: {
      login() {
        console.log("Вхід: ", this.email, this.password);
        // Додайте логіку входу тут
      }
    }
  };
</script>

<style scoped>
  .home-page {
    text-align: center;
    padding: 2rem;
    padding-top: 150px;
    margin: 5% auto;
  }

  .welcome-container {
    width: 100%;
    text-align: center;
    margin-bottom: 2rem;
  }

  .welcome-text {
    white-space: nowrap;
  }

    .welcome-text h1 {
      font-size: 2rem;
      color: #333;
      margin-bottom: 0.5rem;
      white-space: nowrap;
    }

    .welcome-text p {
      font-size: 1.1rem;
      color: #555;
      white-space: nowrap;
    }

  .login-box {
    background: #fff;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    max-width: 500px;
    margin: 0 auto;
  }

  .login-form {
    display: flex;
    flex-direction: column;
  }

    .login-form input {
      margin-bottom: 1rem;
      padding: 0.8rem;
      font-size: 1rem;
      border: 1px solid #ddd;
      border-radius: 8px;
      transition: all 0.3s ease;
    }

      .login-form input:focus {
        border-color: #007bff;
        box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
        outline: none;
      }

    .login-form button {
      background: linear-gradient(135deg, #41ec22, #27ac0f);
      color: white;
      padding: 0.8rem;
      font-size: 1.1rem;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s;
    }

      .login-form button:hover {
        background: linear-gradient(135deg, #0056b3, #004099);
      }

  .register-link {
    margin-top: 1.5rem;
    font-size: 1rem;
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
