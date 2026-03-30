import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior() {
    return { top: 0 }
  },
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
      meta: { guestOnly: true },
    },
    {
      path: '/signin',
      name: 'SignIn',
      component: () => import('@/views/SignInView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/xpath',
      name: 'Xpath',
      component: () => import('@/views/XPathView.vue'),
      meta: { requiresAuth: true },
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
    },
    {
      path: '/tenders',
      name: 'TenderList',
      component: () => import('@/views/tenders/TenderListView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/tenders/create',
      name: 'TenderCreate',
      component: () => import('@/views/tenders/TenderCreateView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/tenders/:id',
      name: 'TenderDetail',
      component: () => import('@/views/tenders/TenderDetailView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/signin')
  }

  if (to.meta.guestOnly && isAuthenticated) {
    return next('/')
  }

  next()
})

export default router
