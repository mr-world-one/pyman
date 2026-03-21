<template>
  <div class="excel-page">
    <div class="excel-container">
      <h1>Завантаження Excel документа</h1>
      <p>Перетягніть файл сюди або натисніть, щоб вибрати Excel документ для перевірки та аналізу.</p>

      <div
        class="drop-area"
        @dragover.prevent
        @dragenter.prevent
        @drop.prevent="handleDrop"
        @click="triggerFileInput"
      >
        <p v-if="!fileName">Перетягніть файл сюди або натисніть, щоб вибрати</p>
        <p v-else>Вибраний файл: {{ fileName }}</p>
      </div>
      <input type="file" ref="fileInput" @change="handleFileChange" accept=".xlsx, .xls" hidden />

      <StoreSelector v-if="fileName" v-model="selectedStores" :stores="availableStores" />

      <AppButton
        v-if="fileName"
        size="lg"
        :disabled="selectedStores.length === 0"
        style="margin-top: var(--space-4)"
        @click="handleUpload"
      >
        Завантажити та перевірити
      </AppButton>

      <div v-if="comparisonData" class="results-container">
        <h2>Результати порівняння</h2>
        <div class="table-responsive">
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
                <td :class="getDifferenceClass(item)">{{ getPriceDifference(item) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <AppLoader v-if="isLoading" :overlay="true" />
  </div>
</template>

<script>
import { ref } from 'vue';
import { apiClient } from '@/api/config';
import { useToast } from '@/composables/useToast';
import AppButton from '@/components/AppButton.vue';
import AppLoader from '@/components/AppLoader.vue';
import StoreSelector from '@/components/StoreSelector.vue';

export default {
  name: 'ExcelUpload',
  components: { AppButton, AppLoader, StoreSelector },
  setup() {
    const toast = useToast();
    const fileName = ref('');
    const fileData = ref(null);
    const fileInput = ref(null);
    const comparisonData = ref(null);
    const storeData = ref(null);
    const isLoading = ref(false);
    const availableStores = [
      { key: 'rozetka', name: 'Rozetka' },
      { key: 'silpo', name: 'Сільпо' },
      { key: 'epicentr', name: 'Епіцентр' },
      { key: 'citadel', name: 'Citadel' },
    ];
    const selectedStores = ref(['rozetka']);

    const triggerFileInput = () => fileInput.value.click();

    const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (file) {
        fileName.value = file.name;
        fileData.value = file;
      }
    };

    const handleDrop = (event) => {
      const file = event.dataTransfer.files[0];
      if (file) {
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
          toast.error(response.data.message || response.data);
          return;
        }
        comparisonData.value = response.data.excel_data;
        storeData.value = response.data.store_data;
        fileName.value = '';
        fileData.value = null;
      } catch (error) {
        toast.error(error.response?.data?.detail || 'Сталася помилка під час обробки файлу');
      } finally {
        isLoading.value = false;
      }
    };

    const areNamesSimilar = (name1, name2) => {
      const clean = (s) => s.trim().toLowerCase().replace(/[^a-zа-яїієґ0-9\s]/g, '');
      const n1 = clean(name1);
      const n2 = clean(name2);
      if (n1.length < 3 || n2.length < 3) return n1.includes(n2) || n2.includes(n1);
      const words1 = n1.split(/\s+/).filter((w) => w.length > 1);
      const words2 = n2.split(/\s+/).filter((w) => w.length > 1);
      const common = words1.filter((w) => words2.some((w2) => w2.includes(w) || w.includes(w2)));
      return common.length / Math.max(words1.length, words2.length, 1) >= 0.15;
    };

    const getLowestStorePrice = (productName) => {
      if (!storeData.value?.length) return null;
      const matches = storeData.value.filter((item) => areNamesSimilar(productName, item.title));
      if (!matches.length) return null;
      const best = matches.reduce((min, item) => {
        const price = item.price_on_sale || item.price;
        const minPrice = min.price_on_sale || min.price;
        return price < minPrice ? item : min;
      });
      return {
        price: (best.price_on_sale || best.price)?.toFixed?.(2) ?? (best.price_on_sale || best.price),
        store_name: best.store_name || '—',
      };
    };

    const getPriceDifference = (item) => {
      const storeInfo = getLowestStorePrice(item.product_name);
      if (!storeInfo) return '—';
      const diff = parseFloat(item.original_price_uah) - parseFloat(storeInfo.price);
      return diff >= 0 ? `+${diff.toFixed(2)} грн` : `${diff.toFixed(2)} грн`;
    };

    const getDifferenceClass = (item) => {
      const storeInfo = getLowestStorePrice(item.product_name);
      if (!storeInfo) return '';
      const diff = parseFloat(item.original_price_uah) - parseFloat(storeInfo.price);
      return diff > 0 ? 'price-higher' : diff < 0 ? 'price-lower' : 'price-equal';
    };

    return {
      fileName, fileInput, comparisonData, isLoading,
      availableStores, selectedStores,
      triggerFileInput, handleFileChange, handleDrop, handleUpload,
      getLowestStorePrice, getPriceDifference, getDifferenceClass,
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
}

.excel-container {
  background: var(--color-surface);
  padding: 2.5rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  max-width: 900px;
  width: 100%;
  text-align: center;
  font-family: var(--font-body);
  border: 2px solid var(--color-green-500);
}

.excel-container h1 {
  font-size: var(--text-4xl);
  color: var(--color-heading);
  margin-bottom: var(--space-4);
}

.excel-container p {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-6);
}

.drop-area {
  border: 3px dashed var(--color-green-500);
  border-radius: var(--radius-md);
  padding: 2.5rem;
  cursor: pointer;
  transition: background-color var(--transition-base);
  color: var(--color-text-secondary);
}

.drop-area:hover {
  background-color: var(--color-green-50);
}

.results-container {
  margin-top: var(--space-8);
}

.results-container h2 {
  font-size: var(--text-3xl);
  color: var(--color-heading);
  margin-bottom: var(--space-6);
  font-weight: var(--font-bold);
}

.modern-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 12px;
  font-family: var(--font-body);
}

.modern-table th {
  background: var(--color-gray-100);
  color: var(--color-heading);
  padding: 16px;
  font-size: var(--text-sm);
  font-weight: var(--font-bold);
  text-align: center;
  border-bottom: 3px solid var(--color-green-500);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.modern-table td {
  padding: 16px;
  text-align: center;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.table-row:hover td {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.price-higher {
  color: var(--color-danger);
  font-weight: var(--font-bold);
  background: var(--color-danger-light);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
}

.price-lower {
  color: var(--color-success);
  font-weight: var(--font-bold);
  background: var(--color-green-50);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
}

.price-equal {
  color: var(--color-text-secondary);
  font-weight: var(--font-bold);
  background: var(--color-gray-100);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
}
</style>
