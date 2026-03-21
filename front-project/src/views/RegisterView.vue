<template>
  <PageContainer max-width="sm" centered>
    <CardPanel>
      <h1 class="form-title">Реєстрація користувача</h1>
      <div v-if="error" class="alert alert-error">{{ error }}</div>
      <form @submit.prevent="handleRegister">
        <FormGroup label="Ім'я" html-for="name" required>
          <input
            type="text"
            id="name"
            v-model="name"
            class="app-input"
            placeholder="Введіть ім'я"
            required
          />
        </FormGroup>
        <FormGroup label="Електронна пошта" html-for="email" required>
          <input
            type="email"
            id="email"
            v-model="email"
            class="app-input"
            placeholder="Введіть електронну пошту"
            required
          />
        </FormGroup>
        <FormGroup label="Пароль" html-for="password" required>
          <input
            type="password"
            id="password"
            v-model="password"
            class="app-input"
            placeholder="Введіть пароль"
            required
          />
        </FormGroup>
        <AppButton type="submit" :loading="loading" :disabled="loading" size="lg" style="width: 100%">
          {{ loading ? 'Реєстрація...' : 'Зареєструватися' }}
        </AppButton>
      </form>
      <p class="form-footer">
        Вже маєте акаунт? <router-link to="/signin">Увійдіть!</router-link>
      </p>
    </CardPanel>
  </PageContainer>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'
import PageContainer from '@/components/PageContainer.vue'
import CardPanel from '@/components/CardPanel.vue'
import FormGroup from '@/components/FormGroup.vue'
import AppButton from '@/components/AppButton.vue'

export default {
  name: 'RegisterView',
  components: { PageContainer, CardPanel, FormGroup, AppButton },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const toast = useToast()
    const name = ref('')
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const loading = ref(false)

    const handleRegister = async () => {
      if (loading.value) return
      loading.value = true

      try {
        error.value = ''
        await authStore.register({
          name: name.value,
          email: email.value,
          password: password.value,
        })
        toast.success('Реєстрація успішна!')
        router.push('/')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Помилка реєстрації'
        toast.error(error.value)
      } finally {
        loading.value = false
      }
    }

    return { name, email, password, error, loading, handleRegister }
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
