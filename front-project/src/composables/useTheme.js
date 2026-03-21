import { ref, watchEffect } from 'vue'

const STORAGE_KEY = 'checkit-theme'
const isDark = ref(false)

// Ініціалізація: localStorage → system preference
const saved = localStorage.getItem(STORAGE_KEY)
if (saved) {
  isDark.value = saved === 'dark'
} else {
  isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
}

// Синхронізація з <html data-theme>
watchEffect(() => {
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
  localStorage.setItem(STORAGE_KEY, isDark.value ? 'dark' : 'light')
})

export function useTheme() {
  const toggleTheme = () => {
    isDark.value = !isDark.value
  }

  return { isDark, toggleTheme }
}
