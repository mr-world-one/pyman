import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { apiClient } from './api/config'
const app = createApp(App)

// Make API client available globally
app.config.globalProperties.$api = apiClient

app.use(router)

app.mount('#app')
