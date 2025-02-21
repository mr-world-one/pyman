<template>
  <div class="signin-page">
    <div class="signin">
      <h1>Увійдіть у свій акаунт</h1>
      <form class="signin-form" @submit.prevent="login">
        <div class="form-group">
          <label for="email">Електронна пошта<span class="required">*</span></label>
          <input type="email" id="email" v-model="email" placeholder="Введіть вашу електронну пошту" required />
        </div>
        <div class="form-group">
          <label for="password">Пароль<span class="required">*</span></label>
          <input type="password" id="password" v-model="password" placeholder="Введіть ваш пароль" required />
        </div>
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
    name: 'SignIn',
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

    button:hover {
      background-color: #0056b3;
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
