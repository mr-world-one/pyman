import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/xpath',
      name: 'Xpath',
      component: () => import('@/views/XPathView.vue'),
      meta: { requiresAuth: true },
    },

    {
      path: '/signin',
      name: 'SignIn',
      component: () => import('@/views/SignInView.vue') 
    },

    {
      path: '/excel-page',
      name: 'ExcelUpload',
      component: () => import('@/views/PrivateView.vue'),
      meta: { requiresAuth: true },
    },

    {
      path: '/search-tender',
      name: 'Prozorro',
      component: () => import('@/views/ProzorroView.vue'),
      meta: { requiresAuth: true },
    }
  ], 
    
})


// Navigation guard — uses localStorage directly to avoid circular pinia import
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/signin')
  }
  next()
})
export default router
