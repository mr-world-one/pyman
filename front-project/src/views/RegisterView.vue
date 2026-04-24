<template>
  <PageContainer max-width="sm" centered>
    <div class="auth-card">
      <div class="auth-card__brand wordmark">
        <span class="logo-green">check</span><span class="logo-red">IT</span>
      </div>
      <h1 class="auth-card__title">Реєстрація</h1>
      <p class="auth-card__subtitle">Створіть акаунт за хвилину.</p>

      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <FormGroup label="Імʼя та прізвище" html-for="name" required>
          <div class="input-icon">
            <AppIcon name="user" :size="14" class="input-icon__svg" />
            <input
              id="name"
              type="text"
              v-model="name"
              class="app-input app-input--with-icon"
              placeholder="Олена Ковальчук"
              required
            />
          </div>
        </FormGroup>
        <FormGroup label="Електронна пошта" html-for="email" required>
          <div class="input-icon">
            <AppIcon name="mail" :size="14" class="input-icon__svg" />
            <input
              id="email"
              type="email"
              v-model="email"
              class="app-input app-input--with-icon"
              placeholder="you@org.ua"
              required
            />
          </div>
        </FormGroup>
        <FormGroup label="Пароль" html-for="password" required hint="Не менше 8 символів">
          <div class="input-icon">
            <AppIcon name="lock" :size="14" class="input-icon__svg" />
            <input
              id="password"
              type="password"
              v-model="password"
              class="app-input app-input--with-icon"
              placeholder="••••••••"
              required
            />
          </div>
        </FormGroup>
        <label class="auth-form__terms">
          <input type="checkbox" v-model="terms" />
          <span>
            Я погоджуюсь з <a href="#">умовами використання</a> та
            <a href="#">політикою конфіденційності</a>.
          </span>
        </label>
        <AppButton type="submit" :loading="loading" :disabled="loading || !terms" size="lg" class="auth-form__submit">
          {{ loading ? 'Реєстрація...' : 'Створити акаунт' }}
        </AppButton>
      </form>

      <p class="auth-card__footer">
        Вже маєте акаунт?
        <router-link to="/signin">Увійдіть</router-link>
      </p>
    </div>
  </PageContainer>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'
import PageContainer from '@/components/PageContainer.vue'
import FormGroup from '@/components/FormGroup.vue'
import AppButton from '@/components/AppButton.vue'
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'RegisterView',
  components: { PageContainer, FormGroup, AppButton, AppIcon },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const toast = useToast()
    const name = ref('')
    const email = ref('')
    const password = ref('')
    const terms = ref(false)
    const error = ref('')
    const loading = ref(false)

    const handleRegister = async () => {
      if (loading.value || !terms.value) return
      loading.value = true
      try {
        error.value = ''
        await authStore.register({ name: name.value, email: email.value, password: password.value })
        toast.success('Реєстрація успішна!')
        router.push('/')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Помилка реєстрації'
        toast.error(error.value)
      } finally {
        loading.value = false
      }
    }

    return { name, email, password, terms, error, loading, handleRegister }
  },
}
</script>

<style scoped>
.auth-card {
  width: 100%;
  max-width: 440px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-soft);
  padding: var(--space-8);
}

.auth-card__brand {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
}

.logo-green { color: var(--color-primary); }
.logo-red { color: var(--color-danger); }

.auth-card__title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  margin-top: var(--space-5);
  letter-spacing: var(--tracking-display);
}

.auth-card__subtitle {
  margin-top: 4px;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.auth-form {
  margin-top: var(--space-6);
}

.auth-form__terms {
  display: flex;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin-bottom: var(--space-4);
  cursor: pointer;
}

.auth-form__terms input {
  margin-top: 2px;
  accent-color: var(--color-primary);
}

.auth-form__terms a {
  color: var(--color-heading);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.auth-form__submit {
  width: 100%;
}

.alert {
  margin-bottom: var(--space-4);
}

.input-icon {
  position: relative;
}

.input-icon__svg {
  position: absolute;
  left: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-tertiary);
  pointer-events: none;
}

.app-input--with-icon {
  padding-left: 34px;
}

.auth-card__footer {
  margin-top: var(--space-6);
  text-align: center;
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.auth-card__footer a {
  color: var(--color-heading);
  font-weight: var(--font-medium);
}
.auth-card__footer a:hover { text-decoration: underline; }
</style>
