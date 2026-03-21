<script>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import AppToast from '@/components/AppToast.vue'

export default {
  name: 'App',
  components: { AppToast },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const menuOpen = ref(false)
    const { isDark, toggleTheme } = useTheme()

    const isAuthenticated = computed(() => authStore.isAuthenticated)

    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value
    }

    const closeMenu = () => {
      menuOpen.value = false
    }

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
    }
  },
}
</script>

<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="app-header__inner">
        <router-link to="/" class="app-header__logo">
          <span class="logo-green">check</span><span class="logo-red">IT</span>
        </router-link>

        <nav class="app-header__nav desktop-nav">
          <template v-if="isAuthenticated">
            <router-link to="/excel-page" class="nav-link" active-class="nav-link--active">Excel</router-link>
            <router-link to="/search-tender" class="nav-link" active-class="nav-link--active">Prozorro</router-link>
            <router-link to="/xpath" class="nav-link" active-class="nav-link--active">X-Path</router-link>
          </template>
        </nav>

        <div class="app-header__actions desktop-nav">
          <button class="theme-toggle" @click="toggleTheme" :aria-label="isDark ? 'Світла тема' : 'Темна тема'">
            <span v-if="isDark">☀️</span>
            <span v-else>🌙</span>
          </button>
          <template v-if="isAuthenticated">
            <button class="nav-link nav-link--logout" @click="handleLogout">Вийти</button>
          </template>
          <template v-else>
            <router-link to="/signin" class="nav-link" active-class="nav-link--active">Увійти</router-link>
            <router-link to="/register" class="nav-link nav-link--cta" active-class="nav-link--active">Реєстрація</router-link>
          </template>
        </div>

        <button class="hamburger" @click="toggleMenu" :aria-expanded="menuOpen" aria-label="Меню">
          <span class="hamburger__line" :class="{ open: menuOpen }"></span>
          <span class="hamburger__line" :class="{ open: menuOpen }"></span>
          <span class="hamburger__line" :class="{ open: menuOpen }"></span>
        </button>
        <button class="theme-toggle theme-toggle--mobile" @click="toggleTheme" :aria-label="isDark ? 'Світла тема' : 'Темна тема'">
          <span v-if="isDark">☀️</span>
          <span v-else>🌙</span>
        </button>
      </div>
    </header>

    <transition name="slide">
      <div v-if="menuOpen" class="side-menu-overlay" @click="closeMenu">
        <nav class="side-menu" @click.stop>
          <ul>
            <li><router-link to="/" @click="closeMenu">Головна</router-link></li>
            <li><router-link to="/about" @click="closeMenu">Про нас</router-link></li>
            <template v-if="isAuthenticated">
              <li><router-link to="/excel-page" @click="closeMenu">Excel</router-link></li>
              <li><router-link to="/search-tender" @click="closeMenu">Prozorro</router-link></li>
              <li><router-link to="/xpath" @click="closeMenu">X-Path</router-link></li>
              <li><a href="#" @click.prevent="handleLogout">Вийти</a></li>
            </template>
            <template v-else>
              <li><router-link to="/signin" @click="closeMenu">Увійти</router-link></li>
              <li><router-link to="/register" @click="closeMenu">Реєстрація</router-link></li>
            </template>
          </ul>
        </nav>
      </div>
    </transition>

    <main class="app-main">
      <router-view />
    </main>

    <footer class="app-footer">
      <p>&copy; {{ new Date().getFullYear() }} checkIT — Технологія чесності</p>
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

/* ===== Header ===== */
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--header-height);
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
  z-index: 600;
}

.app-header__inner {
  max-width: var(--container-max-width);
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 var(--space-4);
  gap: var(--space-4);
}

.app-header__logo {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  letter-spacing: 1px;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-green {
  color: var(--color-green-600);
}

.logo-red {
  color: var(--color-red-600);
}

.app-header__nav {
  flex: 1;
  display: flex;
  justify-content: center;
  gap: var(--space-1);
}

.app-header__actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.nav-link {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: background var(--transition-fast), color var(--transition-fast);
  background: none;
  border: none;
  font-family: inherit;
  cursor: pointer;
}

.nav-link:hover {
  background: var(--color-gray-100);
  color: var(--color-text);
}

.nav-link--active {
  background: var(--color-green-100);
  color: var(--color-green-700);
}

.nav-link--cta {
  background: linear-gradient(135deg, var(--color-green-500), var(--color-green-600));
  color: var(--color-white);
}

.nav-link--cta:hover {
  background: linear-gradient(135deg, var(--color-green-600), var(--color-green-700));
  color: var(--color-white);
}

.nav-link--logout {
  color: var(--color-red-600);
}

.nav-link--logout:hover {
  background: var(--color-red-100);
}

/* ===== Theme Toggle ===== */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--color-gray-100);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  cursor: pointer;
  font-size: 1rem;
  transition: background var(--transition-fast), border-color var(--transition-fast);
  flex-shrink: 0;
}

.theme-toggle:hover {
  background: var(--color-gray-200);
  border-color: var(--color-border-hover);
}

.theme-toggle--mobile {
  display: none;
}

/* ===== Hamburger ===== */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  padding: var(--space-2);
  cursor: pointer;
}

.hamburger__line {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--color-gray-700);
  border-radius: 2px;
  transition: transform var(--transition-base), opacity var(--transition-base);
}

.hamburger__line.open:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.hamburger__line.open:nth-child(2) {
  opacity: 0;
}

.hamburger__line.open:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* ===== Side Menu ===== */
.side-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 800;
  display: flex;
  justify-content: flex-end;
}

.side-menu {
  width: 260px;
  height: 100%;
  background: var(--color-red-600);
  padding: var(--space-16) var(--space-6) var(--space-6);
}

.side-menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.side-menu li {
  margin-bottom: var(--space-3);
}

.side-menu a {
  color: var(--color-white);
  text-decoration: none;
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  padding: var(--space-2) var(--space-3);
  display: block;
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
}

.side-menu a:hover {
  background: rgba(255, 255, 255, 0.2);
  color: var(--color-white);
}

.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.3s ease;
}

.slide-enter-active .side-menu,
.slide-leave-active .side-menu {
  transition: transform 0.3s ease;
}

.slide-enter-from {
  opacity: 0;
}

.slide-enter-from .side-menu {
  transform: translateX(100%);
}

.slide-leave-to {
  opacity: 0;
}

.slide-leave-to .side-menu {
  transform: translateX(100%);
}

/* ===== Main ===== */
.app-main {
  flex: 1;
}

/* ===== Footer ===== */
.app-footer {
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
  padding: var(--space-3) var(--space-4);
  text-align: center;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }

  .hamburger {
    display: flex;
  }

  .theme-toggle--mobile {
    display: flex;
  }

  .app-header__logo {
    flex: 1;
  }
}
</style>
