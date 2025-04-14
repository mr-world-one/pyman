<template>
  <div class="tender-page">
    <div class="tender-container">
      <h1>Пошук тендеру</h1>
      <p>Введіть ID Prozorro-тендеру для аналізу:</p>
      <form @submit.prevent="analyzeTender">
        <input type="text"
               v-model.trim="tenderId"
               placeholder="Введіть ID тендеру (наприклад, UA-2023-01-01-000001-a)"
               required />
        <button type="submit" :disabled="isLoading">Аналізувати</button>
      </form>
      <div v-if="isLoading" class="loading-overlay">
        <div aria-busy="true" aria-label="Loading" role="progressbar" class="loading-container">
          <div class="swing">
            <div class="swing-l"></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div class="swing-r"></div>
          </div>
          <div class="shadow">
            <div class="shadow-l"></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div class="shadow-r"></div>
          </div>
        </div>
        <p class="loading-text">Виконується аналіз, це може трішки тривати...</p>
      </div>
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>
      <div v-else-if="analytics && analytics.length" class="results-container">
        <h2>Результати порівняння</h2>
        <table class="modern-table">
          <thead>
            <tr>
              <th>Назва товару</th>
              <th>Ціна з тендеру</th>
              <th>Ціна з Rozetka</th>
              <th>Різниця</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in analytics" :key="item.name" class="table-row">
              <td>
                <a :href="item.rozetka_url" target="_blank" v-if="item.rozetka_url">{{ item.name }}</a>
                <span v-else>{{ item.name }}</span>
              </td>
              <td>{{ item.tender_price.toFixed(2) }} грн</td>
              <td>{{ item.rozetka_price ? item.rozetka_price.toFixed(2) + ' грн' : 'Н/Д' }}</td>
              <td :class="getDifferenceClass(item)">
                {{ getPriceDifference(item) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="tenderId && !isLoading">
        <p>Дані відсутні або товари не знайдені.</p>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'Prozorro',
    data() {
      return {
        tenderId: '',
        analytics: null,
        isLoading: false,
        error: null,
      };
    },
    methods: {
      async analyzeTender() {
        this.isLoading = true;
        this.error = null;
        this.analytics = null;

        try {
          //// GET-запит до /contract_info/{contract_id}
          //const contractResponse = await axios.get(`http://localhost:8000/contract_info/${this.tenderId}`);
          //const tenderData = contractResponse.data;

          // POST-запит до /search-tender
          const searchResponse = await axios.get(`http://localhost:8000/search-tender/${this.tenderId}`
          );

          this.analytics = this.processAnalytics(searchResponse.data.prozorro_data, searchResponse.data.rozetka_data);
        } catch (error) {
          this.error = error.response?.data?.detail || error.message || 'Помилка сервера';
        } finally {
          this.isLoading = false;
        }
      },
      processAnalytics(prozorroData, rozetkaData) {
        return prozorroData.map((tenderItem) => {
          const name = tenderItem.name || '';
          const tenderPrice = parseFloat(tenderItem.unit_price) || 0;

          // Зіставляємо з rozetka_data
          const rozetkaItem = rozetkaData.find((item) => this.areNamesSimilar(name, item.title)) || {};

          return {
            name,
            tender_price: tenderPrice,
            rozetka_price: rozetkaItem.price_on_sale ? parseFloat(rozetkaItem.price_on_sale) : parseFloat(rozetkaItem.price) || null,
            rozetka_url: rozetkaItem.url || null,
            price_difference: rozetkaItem.price_on_sale || rozetkaItem.price ? tenderPrice - parseFloat(rozetkaItem.price_on_sale || rozetkaItem.price) : null,
          };
        }).filter((item) => item.name && item.tender_price);
      },
      areNamesSimilar(name1, name2) {
        if (!name1 || !name2) return false;
        const cleanName1 = name1.trim().toLowerCase().replace(/[^a-z0-9\s]/g, '');
        const cleanName2 = name2.trim().toLowerCase().replace(/[^a-z0-9\s]/g, '');
        const words1 = cleanName1.split(/\s+/).filter((word) => word.length > 1);
        const words2 = cleanName2.split(/\s+/).filter((word) => word.length > 1);
        if (cleanName1.length < 3 || cleanName2.length < 3) {
          return cleanName1.includes(cleanName2) || cleanName2.includes(cleanName1);
        }
        const commonWords = words1.filter((word) => words2.some((w) => w.includes(word) || word.includes(w)));
        const similarity = commonWords.length / Math.max(words1.length, words2.length, 1);
        return similarity >= 0.15;
      },
      getPriceDifference(item) {
        if (!item.rozetka_price) return '—';
        const diff = item.price_difference;
        return diff >= 0 ? `+${diff.toFixed(2)} грн` : `${diff.toFixed(2)} грн`;
      },
      getDifferenceClass(item) {
        if (!item.rozetka_price) return '';
        const diff = item.price_difference;
        return diff > 0 ? 'price-higher' : diff < 0 ? 'price-lower' : 'price-equal';
      },
    },
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
    max-width: 900px;
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

    button:disabled {
      background: #ccc;
      cursor: not-allowed;
      transform: none;
    }

  .results-container {
    margin-top: 2rem;
  }

    .results-container h2 {
      font-size: 2rem;
      color: #333;
      margin-bottom: 1.5rem;
      font-weight: 700;
    }

  .modern-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 12px;
    font-family: 'Raleway', sans-serif;
  }

    .modern-table th {
      background: linear-gradient(135deg, #f5f7fa, #e0e4e8);
      color: #222;
      padding: 16px;
      font-size: 1.6rem;
      font-weight: 800;
      text-align: center;
      border-bottom: 3px solid #0efc3d;
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .modern-table td {
      padding: 16px;
      text-align: center;
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      font-size: 1.4rem;
      font-weight: 700;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

      .modern-table td a {
        color: #2a9d8f;
        text-decoration: none;
        font-weight: 700;
      }

        .modern-table td a:hover {
          text-decoration: underline;
        }

  .table-row:hover td {
    transform: translateY(-4px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }

  .price-higher {
    color: #e63946;
    font-weight: 800;
    background: rgba(230, 57, 70, 0.15);
    padding: 6px 10px;
    border-radius: 6px;
  }

  .price-lower {
    color: #2a9d8f;
    font-weight: 800;
    background: rgba(42, 157, 143, 0.15);
    padding: 6px 10px;
    border-radius: 6px;
  }

  .price-equal {
    color: #666;
    font-weight: 800;
    background: rgba(102, 102, 102, 0.15);
    padding: 6px 10px;
    border-radius: 6px;
  }

  .error-message {
    color: #e63946;
    font-size: 1.2rem;
    margin-top: 2rem;
  }

  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .loading-container {
    position: relative;
  }

  .swing div {
    border-radius: 50%;
    float: left;
    height: 1.5em;
    width: 1.5em;
    margin: 0 0.3em;
  }

    .swing div:nth-of-type(1) {
      background: linear-gradient(to right, #0efc3d, #41ec22);
    }

    .swing div:nth-of-type(2) {
      background: linear-gradient(to right, #41ec22, #6be34e);
    }

    .swing div:nth-of-type(3) {
      background: linear-gradient(to right, #6be34e, #95d97b);
    }

    .swing div:nth-of-type(4) {
      background: linear-gradient(to right, #95d97b, #bfcf9c);
    }

    .swing div:nth-of-type(5) {
      background: linear-gradient(to right, #bfcf9c, #e8c5be);
    }

    .swing div:nth-of-type(6) {
      background: linear-gradient(to right, #e8c5be, #ff8080);
    }

    .swing div:nth-of-type(7) {
      background: linear-gradient(to right, #ff8080, #ff0000);
    }

  .shadow {
    clear: left;
    padding-top: 1.5em;
    text-align: center;
  }

    .shadow div {
      filter: blur(1px);
      float: left;
      width: 1.5em;
      height: 0.25em;
      border-radius: 50%;
      background: #e3dbd2;
      margin: 0 0.3em;
    }

    .shadow .shadow-l {
      background: #d5d8d6;
    }

    .shadow .shadow-r {
      background: #eed3ca;
    }

  .swing-l {
    animation: ball-l 0.425s ease-in-out infinite alternate;
  }

  .swing-r {
    animation: ball-r 0.425s ease-in-out infinite alternate;
  }

  .shadow-l {
    animation: shadow-l-n 0.425s ease-in-out infinite alternate;
  }

  .shadow-r {
    animation: shadow-r-n 0.425s ease-in-out infinite alternate;
  }

  @keyframes ball-l {
    0%, 50% {
      transform: rotate(0) translateX(0);
    }

    100% {
      transform: rotate(50deg) translateX(-2.5em);
    }
  }

  @keyframes ball-r {
    0% {
      transform: rotate(-50deg) translateX(2.5em);
    }

    50%, 100% {
      transform: rotate(0) translateX(0);
    }
  }

  @keyframes shadow-l-n {
    0%, 50% {
      opacity: 0.5;
      transform: translateX(0);
    }

    100% {
      opacity: 0.125;
      transform: translateX(-1.75em);
    }
  }

  @keyframes shadow-r-n {
    0% {
      opacity: 0.125;
      transform: translateX(1.75em);
    }

    50%, 100% {
      opacity: 0.5;
      transform: translateX(0);
    }
  }

  .loading-text {
    color: #fff;
    font-size: 1.5rem;
    margin-top: 2rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
</style>
