<script>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import AppToast from '@/components/AppToast.vue'
import AppIcon from '@/components/AppIcon.vue'
import AppIconSprite from '@/components/AppIconSprite.vue'

export default {
  name: 'App',
  components: { AppToast, AppIcon, AppIconSprite },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const menuOpen = ref(false)
    const { isDark, toggleTheme } = useTheme()

    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const currentYear = new Date().getFullYear()

    const toggleMenu = () => { menuOpen.value = !menuOpen.value }
    const closeMenu = () => { menuOpen.value = false }

    const handleLogout = async () => {
      authStore.logout()
      closeMenu()
      await router.push('/signin')
    }

    return {
      menuOpen,
      toggleMenu,
      closeMenu,
      isAuthenticated,
      handleLogout,
      isDark,
      toggleTheme,
      currentYear,
    }
  },
}
</script>

<template>
  <div class="app-layout">
    <AppIconSprite />

    <header class="app-header">
      <div class="app-header__inner">
        <router-link to="/" class="app-header__logo wordmark" @click="closeMenu">
          <span class="logo-green">check</span><span class="logo-red">IT</span>
        </router-link>

        <nav class="app-header__nav desktop-nav" v-if="isAuthenticated">
          <router-link to="/tenders" class="nav-link" active-class="nav-link--active">Тендери</router-link>
          <router-link to="/search-tender" class="nav-link" active-class="nav-link--active">Prozorro</router-link>
          <router-link to="/excel-page" class="nav-link" active-class="nav-link--active">Excel</router-link>
          <router-link to="/xpath" class="nav-link" active-class="nav-link--active">X-Path</router-link>
        </nav>
        <nav class="app-header__nav desktop-nav" v-else>
          <router-link to="/about" class="nav-link" active-class="nav-link--active">Про нас</router-link>
        </nav>

        <div class="app-header__actions desktop-nav">
          <button
            class="icon-btn"
            type="button"
            :aria-label="isDark ? 'Світла тема' : 'Темна тема'"
            @click="toggleTheme"
          >
            <AppIcon :name="isDark ? 'sun' : 'moon'" :size="16" />
          </button>
          <template v-if="isAuthenticated">
            <button class="nav-link nav-link--logout" type="button" @click="handleLogout">Вийти</button>
          </template>
          <template v-else>
            <router-link to="/signin" class="nav-link">Увійти</router-link>
            <router-link to="/register" class="nav-link nav-link--cta" active-class="nav-link--active">Реєстрація</router-link>
          </template>
        </div>

        <div class="app-header__mobile">
          <button
            class="icon-btn"
            type="button"
            :aria-label="isDark ? 'Світла тема' : 'Темна тема'"
            @click="toggleTheme"
          >
            <AppIcon :name="isDark ? 'sun' : 'moon'" :size="16" />
          </button>
          <button
            class="icon-btn"
            type="button"
            aria-label="Меню"
            :aria-expanded="menuOpen"
            @click="toggleMenu"
          >
            <AppIcon :name="menuOpen ? 'x' : 'menu'" :size="18" />
          </button>
        </div>
      </div>
    </header>

    <transition name="drawer">
      <div v-if="menuOpen" class="drawer-overlay" @click="closeMenu">
        <aside class="drawer" @click.stop>
          <div class="drawer__head">
            <span class="wordmark">
              <span class="logo-green">check</span><span class="logo-red">IT</span>
            </span>
            <button class="icon-btn" type="button" aria-label="Закрити меню" @click="closeMenu">
              <AppIcon name="x" :size="18" />
            </button>
          </div>
          <nav class="drawer__nav">
            <router-link to="/" @click="closeMenu">Головна</router-link>
            <router-link to="/about" @click="closeMenu">Про нас</router-link>
            <template v-if="isAuthenticated">
              <router-link to="/tenders" @click="closeMenu">Тендери</router-link>
              <router-link to="/search-tender" @click="closeMenu">Prozorro</router-link>
              <router-link to="/excel-page" @click="closeMenu">Excel</router-link>
              <router-link to="/xpath" @click="closeMenu">X-Path</router-link>
              <button type="button" class="drawer__logout" @click="handleLogout">Вийти</button>
            </template>
            <template v-else>
              <router-link to="/signin" @click="closeMenu">Увійти</router-link>
              <router-link to="/register" @click="closeMenu">Реєстрація</router-link>
            </template>
          </nav>
        </aside>
      </div>
    </transition>

    <main class="app-main">
      <router-view />
    </main>

    <footer class="app-footer">
      <div class="app-footer__inner">
        <div class="app-footer__brand">
          <span class="wordmark"><span class="logo-green">check</span><span class="logo-red">IT</span></span>
          <span class="app-footer__dot">·</span>
          <span>Технологія чесності</span>
        </div>
        <div class="app-footer__links">
          <a href="#">Документація</a>
          <a href="#">API</a>
          <a href="#">Контакти</a>
          <span class="num">© {{ currentYear }}</span>
        </div>
      </div>
    </footer>

    <AppToast />
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ===== Wordmark ===== */
.wordmark {
  font-family: var(--font-display);
  font-size: 19px;
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-display);
  text-decoration: none;
  white-space: nowrap;
}

.logo-green { color: var(--color-green-600); }
.logo-red { color: var(--color-red-700); }

[data-theme="dark"] .logo-green { color: var(--color-green-500); }
[data-theme="dark"] .logo-red { color: var(--color-red-500); }

/* ===== Header ===== */
.app-header {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  height: var(--header-height);
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
  z-index: 600;
}

[data-theme="dark"] .app-header {
  background: rgba(2, 6, 23, 0.78);
}

.app-header__inner {
  max-width: var(--container-max-width);
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 var(--space-6);
  gap: var(--space-4);
}

.app-header__logo {
  flex-shrink: 0;
}

.app-header__nav {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 4px;
}

.app-header__actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.app-header__mobile {
  display: none;
  align-items: center;
  gap: var(--space-1);
  margin-left: auto;
}

/* ===== Nav links ===== */
.nav-link {
  padding: 6px var(--space-3);
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-md);
  background: none;
  border: none;
  font-family: inherit;
  cursor: pointer;
  transition: background var(--transition-fast), color var(--transition-fast);
  line-height: 1.5;
}

.nav-link:hover {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

.nav-link--active {
  color: var(--color-heading);
  font-weight: var(--font-medium);
}

.nav-link--cta {
  background: var(--color-primary);
  color: var(--color-white);
  font-weight: var(--font-medium);
}

.nav-link--cta:hover {
  background: var(--color-primary-hover);
  color: var(--color-white);
}

[data-theme="dark"] .nav-link--cta {
  color: #052e1b;
}

.nav-link--logout {
  color: var(--color-text-secondary);
}

.nav-link--logout:hover {
  color: var(--color-danger);
  background: var(--color-danger-light);
}

/* ===== Icon button ===== */
.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.icon-btn:hover {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

/* ===== Drawer ===== */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  backdrop-filter: blur(4px);
  z-index: 800;
  display: flex;
  justify-content: flex-end;
}

.drawer {
  width: 78%;
  max-width: 320px;
  height: 100%;
  background: var(--color-surface);
  border-left: 1px solid var(--color-border);
  padding: var(--space-5);
  overflow-y: auto;
}

.drawer__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
}

.drawer__nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.drawer__nav a,
.drawer__logout {
  display: block;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-md);
  font-weight: var(--font-normal);
  color: var(--color-text);
  text-decoration: none;
  background: transparent;
  border: none;
  text-align: left;
  font-family: inherit;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.drawer__nav a:hover,
.drawer__logout:hover {
  background: var(--color-bg-subtle);
}

.drawer__nav a.router-link-active {
  color: var(--color-heading);
  font-weight: var(--font-medium);
  background: var(--color-bg-subtle);
}

.drawer__logout {
  margin-top: var(--space-2);
  color: var(--color-danger);
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-3);
  border-radius: 0;
}

.drawer-enter-active, .drawer-leave-active {
  transition: opacity 200ms ease;
}
.drawer-enter-active .drawer,
.drawer-leave-active .drawer {
  transition: transform 200ms ease;
}
.drawer-enter-from, .drawer-leave-to { opacity: 0; }
.drawer-enter-from .drawer,
.drawer-leave-to .drawer { transform: translateX(100%); }

/* ===== Main ===== */
.app-main {
  flex: 1;
  background: var(--color-bg);
}

/* ===== Footer ===== */
.app-footer {
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
  height: var(--footer-height);
  display: flex;
  align-items: center;
}

.app-footer__inner {
  max-width: var(--container-max-width);
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  font-size: 12.5px;
  color: var(--color-text-secondary);
}

.app-footer__brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.app-footer__brand .wordmark {
  font-size: var(--text-base);
}

.app-footer__dot { opacity: 0.6; }

.app-footer__links {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.app-footer__links a {
  color: var(--color-text-secondary);
}

.app-footer__links a:hover {
  color: var(--color-heading);
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }
  .app-header__mobile {
    display: flex;
  }
  .app-header__inner {
    padding: 0 var(--space-4);
  }
  .app-footer__links a:nth-child(n+3) { display: none; }
  .app-footer__links {
    gap: var(--space-3);
  }
}
</style>
