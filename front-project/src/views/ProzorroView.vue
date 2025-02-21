<template>
  <div class="tender-page">
    <div class="tender-container">
      <h1>Пошук тендеру</h1>
      <p>Введіть ID Prozorro-тендеру для аналізу:</p>
      <form @submit.prevent="analyzeTender">
        <input type="text" v-model="tenderId" placeholder="Введіть ID тендеру" required />
        <button type="submit">Аналізувати</button>
      </form>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Prozorro",
    data() {
      return {
        tenderId: ""
      };
    },
    methods: {
      analyzeTender() {
        if (this.tenderId.trim()) {
          this.$router.push(`/analyze/${this.tenderId}`);
        }
      }
    }
  };
</script>

<style scoped>
  .tender-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
    padding-top: 100px;
  }

  .tender-container {
    background: #ffffff;
    padding: 2.5rem;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    max-width: 600px;
    width: 100%;
    text-align: center;
    font-family: 'Raleway', sans-serif;
    border: 2px solid #0efc3d;
  }

    .tender-container h1 {
      font-size: 2.5rem;
      color: #333;
      margin-bottom: 1rem;
      font-weight: 700;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.15);
    }

    .tender-container p {
      font-size: 1.2rem;
      color: #444;
      margin-bottom: 1.5rem;
    }

  form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input {
    width: 100%;
    padding: 12px;
    font-size: 1.2rem;
    border: 2px dashed #0efc3d;
    border-radius: 8px;
    outline: none;
    transition: background-color 0.3s ease, border-color 0.3s ease;
    margin-bottom: 1.5rem;
    text-align: center;
  }

    input:focus {
      background-color: rgba(0, 255, 0, 0.1);
      border-color: #b2221e;
    }

  button {
    padding: 0.85rem 2rem;
    font-size: 1.1rem;
    background: linear-gradient(135deg, #41ec22, #27ac0f);
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.2s ease;
  }

    button:hover {
      background: linear-gradient(135deg, #27ac0f, #41ec22);
      transform: scale(1.03);
    }
</style>
