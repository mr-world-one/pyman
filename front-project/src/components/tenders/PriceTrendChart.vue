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
      'Rozetka': '#2563eb',   // info
      'Сільпо': '#059669',    // brand
      'Епіцентр': '#b45309',  // warn
    }

    const getStoreColor = (store) => STORE_COLORS[store] || '#94a3b8'

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
          // Distinct, theme-agnostic warning color — must read on both light and dark
          datasets.push({
            label: 'Тендерна ціна',
            data: [
              { x: minDate, y: item.tender_price },
              { x: maxDate, y: item.tender_price },
            ],
            borderColor: '#dc2626',
            backgroundColor: 'rgba(220, 38, 38, 0.06)',
            borderDash: [8, 4],
            borderWidth: 2,
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 0,
            order: -1,  // draw on top of other lines
          })
        }

        // Theme-aware axis colors
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
        const axisColor = isDark ? '#94a3b8' : '#64748b'
        const gridColor = isDark ? 'rgba(148,163,184,0.12)' : 'rgba(15,23,42,0.06)'
        const titleColor = isDark ? '#f1f5f9' : '#0f172a'

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
                title: { display: true, text: 'Дата', color: titleColor },
                ticks: { color: axisColor },
                grid: { color: gridColor },
              },
              y: {
                title: { display: true, text: 'Ціна (грн)', color: titleColor },
                beginAtZero: false,
                ticks: { color: axisColor },
                grid: { color: gridColor },
              },
            },
            plugins: {
              tooltip: {
                callbacks: {
                  afterLabel: (ctx) => ctx.raw?.title || '',
                },
              },
              legend: {
                position: 'bottom',
                labels: { color: titleColor, usePointStyle: true, boxWidth: 12 },
              },
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
  margin-top: var(--space-2);
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
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg-subtle);
}

.chart-item {
  margin-bottom: var(--space-5);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}

.chart-item:last-child { margin-bottom: 0; }

.chart-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.chart-item-header h4 {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
  color: var(--color-heading);
  letter-spacing: 0;
  margin: 0;
}

.tender-price-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: var(--font-medium);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  font-variant-numeric: tabular-nums;
}

.chart-canvas-wrapper {
  position: relative;
  height: 280px;
}
</style>
