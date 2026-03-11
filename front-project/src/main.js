import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { apiClient } from './api/config'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Make API client available globally
app.config.globalProperties.$api = apiClient

app.mount('#app')
