<template>
  <PageContainer max-width="sm" centered>
    <div class="auth-card">
      <div class="auth-card__brand wordmark">
        <span class="logo-green">check</span><span class="logo-red">IT</span>
      </div>
      <h1 class="auth-card__title">Вхід у акаунт</h1>
      <p class="auth-card__subtitle">Введіть свої дані для продовження роботи.</p>

      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <form @submit.prevent="handleLogin" class="auth-form">
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
        <FormGroup html-for="password" required>
          <template #default>
            <div class="auth-form__password-label">
              <label for="password" class="auth-form__label">Пароль</label>
              <a href="#" class="auth-form__forgot">Забули пароль?</a>
            </div>
            <div class="input-icon">
              <AppIcon name="lock" :size="14" class="input-icon__svg" />
              <input
                id="password"
                type="password"
                v-model="password"
                class="app-input app-input--with-icon"
                placeholder="Введіть пароль"
                required
              />
            </div>
          </template>
        </FormGroup>
        <AppButton type="submit" :loading="loading" :disabled="loading" size="lg" class="auth-form__submit">
          {{ loading ? 'Вхід...' : 'Увійти' }}
        </AppButton>
      </form>

      <p class="auth-card__footer">
        Ще немає акаунту?
        <router-link to="/register">Зареєструватись</router-link>
      </p>
    </div>
  </PageContainer>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import PageContainer from '@/components/PageContainer.vue'
import FormGroup from '@/components/FormGroup.vue'
import AppButton from '@/components/AppButton.vue'
import AppIcon from '@/components/AppIcon.vue'

export default {
  name: 'SignIn',
  components: { PageContainer, FormGroup, AppButton, AppIcon },
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
.auth-card {
  width: 100%;
  max-width: 420px;
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

.auth-form__password-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.auth-form__label {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--color-text);
}

.auth-form__forgot {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}
.auth-form__forgot:hover { color: var(--color-heading); }

.auth-form__submit {
  width: 100%;
  margin-top: var(--space-2);
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
