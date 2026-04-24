<template>
  <div class="excel">
    <div class="excel__inner">
      <div class="page-header">
        <h1 class="page-header__title">Перевірка Excel-прайсу</h1>
        <p class="page-header__subtitle">
          Завантажте файл з позиціями — checkIT звірить кожну з ринком.
        </p>
      </div>

      <div class="excel-layout">
        <!-- Drop zone -->
        <div class="dropzone-card">
          <div
            class="dropzone"
            :class="{ 'is-dragging': isDragging }"
            @dragenter.prevent="isDragging = true"
            @dragover.prevent
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <div class="dropzone__icon"><AppIcon name="upload" :size="18" /></div>
            <h3 class="dropzone__title">Перетягніть файл або натисніть, щоб обрати</h3>
            <p class="dropzone__hint">.xlsx, .xls — до 10 МБ</p>
            <button type="button" class="dropzone__btn" @click.stop="triggerFileInput">
              Обрати файл
            </button>
          </div>
          <input type="file" ref="fileInput" @change="handleFileChange" accept=".xlsx, .xls" hidden />

          <div v-if="fileName" class="file-preview">
            <span class="file-preview__chip">
              <AppIcon name="file" :size="14" />
            </span>
            <div class="file-preview__body">
              <div class="file-preview__name">{{ fileName }}</div>
              <div class="file-preview__meta num">готово до перевірки</div>
            </div>
            <button type="button" class="file-preview__clear" aria-label="Прибрати" @click="clearFile">
              <AppIcon name="x" :size="14" />
            </button>
          </div>

          <div class="excel-actions">
            <AppButton
              size="lg"
              :disabled="!fileData || selectedStores.length === 0 || isLoading"
              :loading="isLoading"
              @click="handleUpload"
            >
              Завантажити та перевірити
              <template #icon-right><AppIcon name="arrow-right" :size="14" /></template>
            </AppButton>
            <a href="#" class="tmpl-link">Завантажити шаблон</a>
          </div>
        </div>

        <!-- Sidebar -->
        <aside class="sidebar">
          <div class="sidebar-card">
            <h4 class="sidebar-card__title">Магазини для звірки</h4>
            <StoreSelector
              v-model="selectedStores"
              :stores="availableStores"
              label=""
            />
          </div>
          <div class="sidebar-card">
            <h4 class="sidebar-card__title">Формат файлу</h4>
            <ul class="format-list">
              <li>
                <AppIcon name="check" :size="14" class="format-list__icon" />
                Колонки: Назва, Кількість, Од., Ціна
              </li>
              <li>
                <AppIcon name="check" :size="14" class="format-list__icon" />
                Перший рядок — заголовки
              </li>
              <li>
                <AppIcon name="check" :size="14" class="format-list__icon" />
                Назва товару — українською або англійською
              </li>
            </ul>
          </div>
        </aside>
      </div>

      <!-- Results -->
      <div v-if="comparisonData" class="results">
        <div class="results__head">
          <div>
            <h3 class="results__title">Результати перевірки</h3>
            <p class="results__sub num">
              {{ comparisonData.length }} рядків
            </p>
          </div>
          <div class="results__actions">
            <button class="ghost-btn">
              <AppIcon name="filter" :size="14" /> Тільки відхилення
            </button>
            <button class="ghost-btn ghost-btn--bordered">
              <AppIcon name="download" :size="14" /> Експорт XLSX
            </button>
          </div>
        </div>
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>Назва товару</th>
                <th class="col-num">Ціна з тендеру</th>
                <th class="col-num">Ціна з магазину</th>
                <th class="col-store">Магазин</th>
                <th class="col-num">Різниця</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in comparisonData" :key="item.product_name" class="row-hover">
                <td>{{ item.product_name }}</td>
                <td class="num col-num">{{ item.original_price_uah.toFixed(2) }} ₴</td>
                <td class="num col-num">
                  <template v-if="getLowestStorePrice(item.product_name)">
                    {{ getLowestStorePrice(item.product_name).price }} ₴
                  </template>
                  <span v-else class="dim">Н/Д</span>
                </td>
                <td>
                  <span v-if="getLowestStorePrice(item.product_name)" class="store-cell">
                    <span
                      :class="['store-dot', `store-${storeKeyFromName(getLowestStorePrice(item.product_name).store_name)}`]"
                    ></span>
                    {{ getLowestStorePrice(item.product_name).store_name }}
                  </span>
                  <span v-else class="dim">—</span>
                </td>
                <td :class="['num col-num', getDifferenceClass(item)]">{{ getPriceDifference(item) }}</td>
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
import { ref } from 'vue'
import { apiClient } from '@/api/config'
import { useToast } from '@/composables/useToast'
import AppButton from '@/components/AppButton.vue'
import AppLoader from '@/components/AppLoader.vue'
import AppIcon from '@/components/AppIcon.vue'
import StoreSelector from '@/components/StoreSelector.vue'

const STORE_KEY_BY_NAME = {
  'Rozetka': 'rozetka',
  'Сільпо': 'silpo',
  'Епіцентр': 'epicentr',
}

export default {
  name: 'ExcelUpload',
  components: { AppButton, AppLoader, AppIcon, StoreSelector },
  setup() {
    const toast = useToast()
    const fileName = ref('')
    const fileData = ref(null)
    const fileInput = ref(null)
    const comparisonData = ref(null)
    const storeData = ref(null)
    const isLoading = ref(false)
    const isDragging = ref(false)
    const availableStores = [
      { key: 'rozetka', name: 'Rozetka' },
      { key: 'silpo', name: 'Сільпо' },
      { key: 'epicentr', name: 'Епіцентр' },
    ]
    const selectedStores = ref(['rozetka'])

    const triggerFileInput = () => fileInput.value.click()

    const handleFileChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        fileName.value = file.name
        fileData.value = file
      }
    }

    const handleDrop = (event) => {
      isDragging.value = false
      const file = event.dataTransfer.files[0]
      if (file) {
        fileName.value = file.name
        fileData.value = file
      }
    }

    const clearFile = () => {
      fileName.value = ''
      fileData.value = null
      if (fileInput.value) fileInput.value.value = ''
    }

    const handleUpload = async () => {
      if (!fileData.value) return
      const formData = new FormData()
      formData.append('file', fileData.value)
      isLoading.value = true
      try {
        const storesParam = selectedStores.value.join(',')
        const response = await apiClient.post(`/excel-page?stores=${storesParam}`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        if (typeof response.data === 'string' || response.data.status === 'error') {
          toast.error(response.data.message || response.data)
          return
        }
        comparisonData.value = response.data.excel_data
        storeData.value = response.data.store_data
        fileName.value = ''
        fileData.value = null
      } catch (error) {
        toast.error(error.response?.data?.detail || 'Сталася помилка під час обробки файлу')
      } finally {
        isLoading.value = false
      }
    }

    const areNamesSimilar = (name1, name2) => {
      const clean = (s) => s.trim().toLowerCase().replace(/[^a-zа-яїієґ0-9\s]/g, '')
      const n1 = clean(name1)
      const n2 = clean(name2)
      if (n1.length < 3 || n2.length < 3) return n1.includes(n2) || n2.includes(n1)
      const words1 = n1.split(/\s+/).filter((w) => w.length > 1)
      const words2 = n2.split(/\s+/).filter((w) => w.length > 1)
      const common = words1.filter((w) => words2.some((w2) => w2.includes(w) || w.includes(w2)))
      return common.length / Math.max(words1.length, words2.length, 1) >= 0.15
    }

    const getLowestStorePrice = (productName) => {
      if (!storeData.value?.length) return null
      const matches = storeData.value.filter((item) => areNamesSimilar(productName, item.title))
      if (!matches.length) return null
      const best = matches.reduce((min, item) => {
        const price = item.price_on_sale || item.price
        const minPrice = min.price_on_sale || min.price
        return price < minPrice ? item : min
      })
      return {
        price: (best.price_on_sale || best.price)?.toFixed?.(2) ?? (best.price_on_sale || best.price),
        store_name: best.store_name || '—',
      }
    }

    const getPriceDifference = (item) => {
      const storeInfo = getLowestStorePrice(item.product_name)
      if (!storeInfo) return '—'
      const diff = parseFloat(item.original_price_uah) - parseFloat(storeInfo.price)
      return diff >= 0 ? `+${diff.toFixed(2)} ₴` : `−${Math.abs(diff).toFixed(2)} ₴`
    }

    const getDifferenceClass = (item) => {
      const storeInfo = getLowestStorePrice(item.product_name)
      if (!storeInfo) return ''
      const diff = parseFloat(item.original_price_uah) - parseFloat(storeInfo.price)
      return diff > 0 ? 'price-higher' : diff < 0 ? 'price-lower' : 'price-equal'
    }

    const storeKeyFromName = (name) => STORE_KEY_BY_NAME[name] || 'rozetka'

    return {
      fileName, fileInput, fileData, comparisonData, isLoading, isDragging,
      availableStores, selectedStores,
      triggerFileInput, handleFileChange, handleDrop, handleUpload, clearFile,
      getLowestStorePrice, getPriceDifference, getDifferenceClass, storeKeyFromName,
    }
  },
}
</script>

<style scoped>
.excel {
  padding: calc(var(--header-height) + var(--space-8)) var(--space-6) var(--space-12);
}

.excel__inner {
  max-width: var(--container-max-width);
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--space-6);
}

.page-header__title {
  font-size: clamp(1.75rem, 3vw, 2rem);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
}

.page-header__subtitle {
  margin-top: 4px;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.excel-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: var(--space-4);
}

/* Dropzone */
.dropzone-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-soft);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.dropzone {
  border: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-10) var(--space-5);
  text-align: center;
  cursor: pointer;
  transition: border-color var(--transition-fast), background var(--transition-fast);
  background-image:
    radial-gradient(circle at 1px 1px, rgb(148 163 184 / 0.5) 1px, transparent 0);
  background-size: 8px 8px;
}

[data-theme="dark"] .dropzone {
  background-image:
    radial-gradient(circle at 1px 1px, rgb(71 85 105 / 0.7) 1px, transparent 0);
}

.dropzone:hover, .dropzone.is-dragging {
  border-color: var(--color-primary);
}

.dropzone__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

.dropzone__title {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
}

.dropzone__hint {
  margin-top: 4px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.dropzone__btn {
  margin-top: var(--space-4);
  display: inline-flex;
  align-items: center;
  height: 36px;
  padding: 0 var(--space-4);
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-family: inherit;
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.dropzone__btn:hover { background: var(--color-bg-subtle); }

/* File preview */
.file-preview {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
}

.file-preview__chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--color-green-50);
  border: 1px solid var(--color-green-100);
  color: var(--color-primary);
}

.file-preview__body { flex: 1; min-width: 0; }

.file-preview__name {
  font-size: 13.5px;
  font-weight: var(--font-medium);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-preview__meta {
  margin-top: 2px;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.file-preview__clear {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
}

.file-preview__clear:hover { background: var(--color-bg-subtle); color: var(--color-text); }

.excel-actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.tmpl-link {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  text-decoration: none;
}

.tmpl-link:hover { color: var(--color-heading); }

/* Sidebar */
.sidebar { display: flex; flex-direction: column; gap: var(--space-4); }

.sidebar-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-soft);
  padding: var(--space-5);
}

.sidebar-card__title {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  margin-bottom: var(--space-3);
  letter-spacing: 0;
}

.format-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.format-list li {
  display: flex;
  gap: var(--space-2);
  align-items: flex-start;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.format-list__icon {
  color: var(--color-primary);
  margin-top: 2px;
  flex-shrink: 0;
}

/* Results */
.results {
  margin-top: var(--space-8);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}

.results__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.results__title {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
}

.results__sub {
  margin-top: 2px;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.results__actions { display: flex; gap: var(--space-2); }

.ghost-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 var(--space-3);
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  font-family: inherit;
  font-size: var(--text-sm);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
}

.ghost-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }

.ghost-btn--bordered {
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
}

/* Data table */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}

.data-table thead th {
  background: var(--color-bg-subtle);
  color: var(--color-text-secondary);
  padding: 10px 14px;
  text-align: left;
  font-size: 11px;
  font-weight: var(--font-medium);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  border-bottom: 1px solid var(--color-border);
}

.data-table thead th.col-num { text-align: right; }
.data-table thead th.col-store { width: 160px; }

.data-table tbody td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
}

.data-table tbody td.col-num { text-align: right; font-variant-numeric: tabular-nums; }

.data-table tr.row-hover:hover td { background: var(--color-bg-subtle); }

.store-cell {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: var(--font-medium);
}

.store-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-slate-400);
}

.store-dot.store-rozetka { background: var(--color-info); }
.store-dot.store-silpo { background: var(--color-primary); }
.store-dot.store-epicentr { background: var(--color-warning); }

.dim { color: var(--color-text-tertiary); }

.price-higher { color: var(--color-danger); font-weight: var(--font-medium); }
.price-lower { color: var(--color-primary); font-weight: var(--font-medium); }
.price-equal { color: var(--color-text-secondary); }

@media (max-width: 900px) {
  .excel-layout { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .excel { padding: calc(var(--header-height) + var(--space-6)) var(--space-4) var(--space-10); }
}
</style>
