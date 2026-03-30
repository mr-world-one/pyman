import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { apiClient } from '@/api/config'

export const useTendersStore = defineStore('tenders', () => {
  const tenders = ref([])
  const currentTender = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const filters = ref({
    tender_type: null,
    status: null,
    page: 1,
    limit: 20,
  })

  const filteredTenders = computed(() => tenders.value)

  const totalPages = computed(() => {
    // Approximate — backend doesn't return count yet
    return tenders.value.length < filters.value.limit ? filters.value.page : filters.value.page + 1
  })

  async function fetchTenders() {
    loading.value = true
    error.value = null
    try {
      const params = {
        page: filters.value.page,
        limit: filters.value.limit,
      }
      if (filters.value.tender_type) params.tender_type = filters.value.tender_type
      if (filters.value.status) params.status = filters.value.status

      const { data } = await apiClient.get('/tenders/', { params })
      tenders.value = data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Помилка завантаження'
    } finally {
      loading.value = false
    }
  }

  async function fetchTender(id) {
    loading.value = true
    error.value = null
    try {
      const { data } = await apiClient.get(`/tenders/${id}`)
      currentTender.value = data
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Тендер не знайдено'
      return null
    } finally {
      loading.value = false
    }
  }

  async function createTender(tenderData) {
    loading.value = true
    error.value = null
    try {
      const { data } = await apiClient.post('/tenders/', tenderData)
      tenders.value.unshift(data)
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Помилка створення'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function importFromProzorro(prozorroId) {
    loading.value = true
    error.value = null
    try {
      const { data } = await apiClient.post(`/tenders/import/${encodeURIComponent(prozorroId)}`)
      tenders.value.unshift(data)
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Помилка імпорту'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteTender(id) {
    try {
      await apiClient.delete(`/tenders/${id}`)
      tenders.value = tenders.value.filter((t) => t.id !== id)
      if (currentTender.value?.id === id) {
        currentTender.value = null
      }
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Помилка видалення'
      throw err
    }
  }

  async function analyzeTender(id, stores = ['rozetka']) {
    loading.value = true
    error.value = null
    try {
      const { data } = await apiClient.post(`/tenders/${id}/analyze`, null, {
        params: { stores: stores.join(',') },
      })
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Помилка аналізу'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchPriceHistory(id, days = 30) {
    try {
      const { data } = await apiClient.get(`/tenders/${id}/price-history`, {
        params: { days },
      })
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Помилка завантаження історії цін'
      return null
    }
  }

  async function analyzeRisks(tenderId, stores = ['rozetka', 'silpo', 'epicentr']) {
    loading.value = true
    error.value = null
    try {
      const { data } = await apiClient.post('/assistant/analyze-risks', null, {
        params: { tender_id: tenderId, stores: stores.join(',') },
      })
      return data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Помилка аналізу ризиків'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setFilter(key, value) {
    filters.value[key] = value
    filters.value.page = 1
  }

  function nextPage() {
    filters.value.page++
  }

  function prevPage() {
    if (filters.value.page > 1) filters.value.page--
  }

  return {
    tenders,
    currentTender,
    loading,
    error,
    filters,
    filteredTenders,
    totalPages,
    fetchTenders,
    fetchTender,
    createTender,
    importFromProzorro,
    deleteTender,
    analyzeTender,
    fetchPriceHistory,
    analyzeRisks,
    setFilter,
    nextPage,
    prevPage,
  }
})
