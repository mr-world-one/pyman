<template>
  <div class="excel-page">
    <div class="excel-container">
      <h1>Завантаження Excel документа</h1>
      <p>Перетягніть файл сюди або натисніть, щоб вибрати Excel документ для перевірки та аналізу.</p>
      <div class="drop-area" @dragover.prevent @dragenter.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
        <p v-if="!fileName">Перетягніть файл сюди або натисніть, щоб вибрати</p>
        <p v-else>Вибраний файл: {{ fileName }}</p>
      </div>
      <input type="file" ref="fileInput" @change="handleFileChange" accept=".xlsx, .xls" hidden />

      <div class="store-selector" v-if="fileName">
        <label>Оберіть магазини для порівняння:</label>
        <div class="store-checkboxes">
          <label v-for="store in availableStores" :key="store.key" class="store-checkbox">
            <input type="checkbox" :value="store.key" v-model="selectedStores" />
            {{ store.name }}
          </label>
        </div>
      </div>

      <button v-if="fileName" @click="handleUpload" :disabled="selectedStores.length === 0">Завантажити та перевірити</button>
      <div v-if="comparisonData" class="results-container">
        <h2>Результати порівняння</h2>
        <table class="modern-table">
          <thead>
            <tr>
              <th>Назва товару</th>
              <th>Ціна з тендеру</th>
              <th>Ціна з магазину</th>
              <th>Магазин</th>
              <th>Різниця</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in comparisonData" :key="item.product_name" class="table-row">
              <td>{{ item.product_name }}</td>
              <td>{{ item.original_price_uah.toFixed(2) }} грн</td>
              <td>{{ getLowestStorePrice(item.product_name)?.price || 'Н/Д' }} {{ getLowestStorePrice(item.product_name) ? 'грн' : '' }}</td>
              <td>{{ getLowestStorePrice(item.product_name)?.store_name || '—' }}</td>
              <td :class="getDifferenceClass(item)">
                {{ getPriceDifference(item) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Анімація завантаження -->
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
  </div>
</template>

<script>
  import { ref } from 'vue';
  import { apiClient } from '@/api/config';

  export default {
    name: 'ExcelUpload',
    setup() {
      const fileName = ref('');
      const fileData = ref(null);
      const fileInput = ref(null);
      const comparisonData = ref(null);
      const storeData = ref(null);
      const isLoading = ref(false);
      const availableStores = ref([
        { key: 'rozetka', name: 'Rozetka' },
        { key: 'silpo', name: 'Сільпо' },
        { key: 'epicentr', name: 'Епіцентр' },
        { key: 'citadel', name: 'Citadel' },
      ]);
      const selectedStores = ref(['rozetka']);

      const triggerFileInput = () => {
        fileInput.value.click();
      };

      const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
          fileName.value = file.name;
          fileData.value = file;
        }
      };

      const handleDrop = (event) => {
        const files = event.dataTransfer.files;
        if (files.length) {
          const file = files[0];
          fileName.value = file.name;
          fileData.value = file;
        }
      };

      const handleUpload = async () => {
        if (!fileData.value) return;

        const formData = new FormData();
        formData.append('file', fileData.value);

        isLoading.value = true;

        try {
          const storesParam = selectedStores.value.join(',');
          const response = await apiClient.post(`/excel-page?stores=${storesParam}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });

          if (typeof response.data === 'string' || response.data.status === 'error') {
            alert(`Помилка: ${response.data.message || response.data}`);
            return;
          }

          comparisonData.value = response.data.excel_data;
          storeData.value = response.data.store_data;
          fileName.value = '';
          fileData.value = null;
        } catch (error) {
          console.error('Помилка:', error);
          alert(error.response?.data?.detail || 'Сталася помилка під час обробки файлу');
        } finally {
          isLoading.value = false;
        }
      };

      const areNamesSimilar = (name1, name2) => {
        const cleanName1 = name1.trim().toLowerCase().replace(/[^a-zа-яїієґ0-9\s]/g, '');
        const cleanName2 = name2.trim().toLowerCase().replace(/[^a-zа-яїієґ0-9\s]/g, '');
        const words1 = cleanName1.split(/\s+/).filter(word => word.length > 1);
        const words2 = cleanName2.split(/\s+/).filter(word => word.length > 1);
        if (cleanName1.length < 3 || cleanName2.length < 3) {
          return cleanName1.includes(cleanName2) || cleanName2.includes(cleanName1);
        }
        const commonWords = words1.filter(word => words2.some(w => w.includes(word) || word.includes(w)));
        const similarity = commonWords.length / Math.max(words1.length, words2.length, 1);
        return similarity >= 0.15;
      };

      const getLowestStorePrice = (productName) => {
        if (!storeData.value || storeData.value.length === 0) return null;

        const matchingItems = storeData.value.filter(item =>
          areNamesSimilar(productName, item.title)
        );

        if (matchingItems.length === 0) return null;

        const best = matchingItems.reduce((min, item) => {
          const price = item.price_on_sale || item.price;
          const minPrice = min.price_on_sale || min.price;
          return (price < minPrice) ? item : min;
        });

        return {
          price: (best.price_on_sale || best.price)?.toFixed?.(2) || best.price_on_sale || best.price,
          store_name: best.store_name || '—',
        };
      };

      const getPriceDifference = (item) => {
        const tenderPrice = parseFloat(item.original_price_uah);
        const storeInfo = getLowestStorePrice(item.product_name);
        if (!storeInfo) return '—';
        const diff = tenderPrice - parseFloat(storeInfo.price);
        return diff >= 0 ? `+${diff.toFixed(2)} грн` : `${diff.toFixed(2)} грн`;
      };

      const getDifferenceClass = (item) => {
        const storeInfo = getLowestStorePrice(item.product_name);
        if (!storeInfo) return '';
        const diff = parseFloat(item.original_price_uah) - parseFloat(storeInfo.price);
        return diff > 0 ? 'price-higher' : diff < 0 ? 'price-lower' : 'price-equal';
      };

      return {
        fileName,
        fileData,
        fileInput,
        comparisonData,
        storeData,
        isLoading,
        availableStores,
        selectedStores,
        triggerFileInput,
        handleFileChange,
        handleDrop,
        handleUpload,
        getLowestStorePrice,
        getPriceDifference,
        getDifferenceClass
      };
    },
  };
</script>

<style scoped>
  .excel-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
    padding-top: 100px;
    position: relative;
  }

  .excel-container {
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

    .excel-container h1 {
      font-size: 2.5rem;
      color: #333;
      margin-bottom: 1rem;
    }

    .excel-container p {
      font-size: 1.2rem;
      color: #444;
      margin-bottom: 1.5rem;
    }

  .drop-area {
    border: 3px dashed #0efc3d;
    border-radius: 8px;
    padding: 2.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

    .drop-area:hover {
      background-color: rgba(0, 255, 0, 0.1);
    }

  .store-selector {
    margin: 1.5rem 0;
    text-align: left;
  }

    .store-selector label {
      font-size: 1.1rem;
      font-weight: 600;
      color: #333;
    }

  .store-checkboxes {
    display: flex;
    gap: 1.2rem;
    flex-wrap: wrap;
    margin-top: 0.5rem;
    justify-content: center;
  }

  .store-checkbox {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-weight: 500 !important;
    cursor: pointer;
    padding: 0.4rem 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    transition: background 0.2s;
  }

    .store-checkbox:hover {
      background: rgba(14, 252, 61, 0.1);
    }

    .store-checkbox input[type='checkbox'] {
      width: auto;
      margin: 0;
    }

  button {
    margin-top: 1.5rem;
    padding: 0.85rem 2rem;
    font-size: 1.1rem;
    background: linear-gradient(135deg, #41ec22, #27ac0f);
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s ease;
  }

    button:hover {
      background: linear-gradient(135deg, #27ac0f, #41ec22);
      transform: scale(1.05);
    }

  /* Стилі для таблиці */
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
      font-size: 1.6rem; /* Збільшено розмір */
      font-weight: 800; /* Жирніший текст */
      text-align: center;
      border-bottom: 3px solid #0efc3d; /* Яскравіша межа */
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .modern-table td {
      padding: 16px;
      text-align: center;
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Посилена тінь */
      font-size: 1.4rem; /* Збільшено розмір */
      font-weight: 700; /* Жирніший текст */
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

  .table-row:hover td {
    transform: translateY(-4px); /* Посилений ефект ховеру */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Глибша тінь при ховері */
  }

  .price-higher {
    color: #e63946;
    font-weight: 800; /* Жирніший текст */
    background: rgba(230, 57, 70, 0.15); /* Легкий фон для акценту */
    padding: 6px 10px;
    border-radius: 6px;
  }

  .price-lower {
    color: #2a9d8f;
    font-weight: 800; /* Жирніший текст */
    background: rgba(42, 157, 143, 0.15); /* Легкий фон для акценту */
    padding: 6px 10px;
    border-radius: 6px;
  }

  .price-equal {
    color: #666;
    font-weight: 800; /* Жирніший текст */
    background: rgba(102, 102, 102, 0.15); /* Легкий фон для акценту */
    padding: 6px 10px;
    border-radius: 6px;
  }

  /* Стилі для анімації завантаження */
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

    /* Градієнт від зеленого до червоного */
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
