<template>
  <PageContainer max-width="sm" centered>
    <CardPanel>
      <h1 class="form-title">Увійдіть у свій акаунт</h1>
      <div v-if="error" class="alert alert-error">{{ error }}</div>
      <form @submit.prevent="handleLogin">
        <FormGroup label="Електронна пошта" html-for="email" required>
          <input
            type="email"
            id="email"
            v-model="email"
            class="app-input"
            placeholder="Введіть вашу електронну пошту"
            required
          />
        </FormGroup>
        <FormGroup label="Пароль" html-for="password" required>
          <input
            type="password"
            id="password"
            v-model="password"
            class="app-input"
            placeholder="Введіть ваш пароль"
            required
          />
        </FormGroup>
        <AppButton type="submit" :loading="loading" :disabled="loading" size="lg" style="width: 100%">
          {{ loading ? 'Вхід...' : 'Увійти' }}
        </AppButton>
      </form>
      <p class="form-footer">
        Ще не зареєстровані? <router-link to="/register">Зареєструйтеся!</router-link>
      </p>
    </CardPanel>
  </PageContainer>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import PageContainer from '@/components/PageContainer.vue'
import CardPanel from '@/components/CardPanel.vue'
import FormGroup from '@/components/FormGroup.vue'
import AppButton from '@/components/AppButton.vue'

export default {
  name: 'SignIn',
  components: { PageContainer, CardPanel, FormGroup, AppButton },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const loading = ref(false)

    const handleLogin = async () => {
      if (loading.value) return
      loading.value = true

      try {
        error.value = ''
        await authStore.login(email.value, password.value)
        router.push('/')
      } catch (err) {
        error.value =
          err.response?.data?.detail || err.message || 'Помилка входу. Перевірте email або пароль'
      } finally {
        loading.value = false
      }
    }

    return { email, password, error, loading, handleLogin }
  },
}
</script>

<style scoped>
.form-title {
  text-align: center;
  font-size: var(--text-2xl);
  margin-bottom: var(--space-6);
}

.form-footer {
  margin-top: var(--space-6);
  text-align: center;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.form-footer a {
  color: var(--color-primary);
  font-weight: var(--font-semibold);
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>
