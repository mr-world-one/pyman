<template>
  <div class="price-trend-chart">
    <div v-if="loading" class="chart-loading">
      <AppLoader />
      <span>Завантаження історії цін...</span>
    </div>

    <div v-else-if="!hasData" class="chart-empty">
      <p>Немає даних про історію цін. Запустіть аналіз цін для збору даних.</p>
    </div>

    <div v-else>
      <div v-for="item in chartData" :key="item.item_id" class="chart-item">
        <div class="chart-item-header">
          <h4>{{ item.item_name }}</h4>
          <span class="tender-price-tag" v-if="item.tender_price > 0">
            Тендерна ціна: {{ formatPrice(item.tender_price) }} грн
          </span>
        </div>
        <div class="chart-canvas-wrapper">
          <canvas :ref="el => setCanvasRef(el, item.item_id)"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted, nextTick } from 'vue'
import AppLoader from '@/components/AppLoader.vue'

export default {
  name: 'PriceTrendChart',
  components: { AppLoader },
  props: {
    tenderId: { type: Number, required: true },
    priceHistory: { type: Object, default: null },
    loading: { type: Boolean, default: false },
  },
  setup(props) {
    const canvasRefs = ref({})
    const chartInstances = ref({})

    const hasData = ref(false)
    const chartData = ref([])

    const setCanvasRef = (el, itemId) => {
      if (el) canvasRefs.value[itemId] = el
    }

    const formatPrice = (val) => {
      if (val == null) return '—'
      return Number(val).toLocaleString('uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }

    const STORE_COLORS = {
      'Rozetka': '#4caf50',
      'Сільпо': '#ff9800',
      'Епіцентр': '#2196f3',
      'Citadel': '#f44336',
    }

    const getStoreColor = (store) => STORE_COLORS[store] || '#9e9e9e'

    const renderCharts = async () => {
      if (!props.priceHistory?.items?.length) {
        hasData.value = false
        chartData.value = []
        return
      }

      hasData.value = true
      chartData.value = props.priceHistory.items

      await nextTick()

      // Dynamically import Chart.js
      let Chart, registerables
      try {
        const chartModule = await import('chart.js')
        Chart = chartModule.Chart
        registerables = chartModule.registerables
        Chart.register(...registerables)
        // Import date adapter for time scale
        await import('chartjs-adapter-date-fns')
      } catch {
        console.warn('chart.js not installed — showing data as table fallback')
        return
      }

      for (const item of chartData.value) {
        const canvas = canvasRefs.value[item.item_id]
        if (!canvas) continue

        // Destroy existing chart
        if (chartInstances.value[item.item_id]) {
          chartInstances.value[item.item_id].destroy()
        }

        // Group history entries by store
        const storeGroups = {}
        for (const entry of item.history || []) {
          const store = entry.source_store || 'Unknown'
          if (!storeGroups[store]) storeGroups[store] = []
          storeGroups[store].push({
            x: new Date(entry.date),
            y: entry.price,
            title: entry.product_title,
          })
        }

        // Build datasets
        const datasets = Object.entries(storeGroups).map(([store, points]) => ({
          label: store,
          data: points.sort((a, b) => a.x - b.x),
          borderColor: getStoreColor(store),
          backgroundColor: getStoreColor(store) + '33',
          fill: false,
          tension: 0.3,
          pointRadius: 4,
          pointHoverRadius: 6,
        }))

        // Add tender price reference line
        if (item.tender_price > 0) {
          const dates = (item.history || []).map(e => new Date(e.date))
          const minDate = dates.length ? new Date(Math.min(...dates)) : new Date()
          const maxDate = dates.length ? new Date(Math.max(...dates)) : new Date()
          datasets.push({
            label: 'Тендерна ціна',
            data: [
              { x: minDate, y: item.tender_price },
              { x: maxDate, y: item.tender_price },
            ],
            borderColor: '#e91e63',
            borderDash: [8, 4],
            borderWidth: 2,
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 0,
          })
        }

        chartInstances.value[item.item_id] = new Chart(canvas, {
          type: 'line',
          data: { datasets },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                type: 'time',
                time: { unit: 'day', displayFormats: { day: 'dd.MM' } },
                title: { display: true, text: 'Дата' },
              },
              y: {
                title: { display: true, text: 'Ціна (грн)' },
                beginAtZero: false,
              },
            },
            plugins: {
              tooltip: {
                callbacks: {
                  afterLabel: (ctx) => ctx.raw?.title || '',
                },
              },
              legend: { position: 'bottom' },
            },
          },
        })
      }
    }

    watch(() => props.priceHistory, renderCharts, { deep: true })

    onMounted(() => {
      if (props.priceHistory) renderCharts()
    })

    return { hasData, chartData, canvasRefs, setCanvasRef, formatPrice }
  },
}
</script>

<style scoped>
.price-trend-chart {
  margin-top: var(--space-4);
}

.chart-loading {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-6);
  justify-content: center;
  color: var(--color-text-secondary);
}

.chart-empty {
  padding: var(--space-6);
  text-align: center;
  color: var(--color-text-secondary);
  font-style: italic;
}

.chart-item {
  margin-bottom: var(--space-6);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
}

.chart-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.chart-item-header h4 {
  font-size: var(--text-base);
  font-weight: var(--font-bold);
  color: var(--color-heading);
  margin: 0;
}

.tender-price-tag {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.chart-canvas-wrapper {
  position: relative;
  height: 280px;
}
</style>
