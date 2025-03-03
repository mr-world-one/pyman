import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Prozorro from '../views/ProzorroView.vue'


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
      component: () => import('@/views/XPathView.vue')
    },

    {
      path: '/signin',
      name: 'SignIn',
      component: () => import('@/views/SignInView.vue') 
    },

    {
      path: '/excel-page',
      name: 'ExcelUpload',
      component: () => import('@/views/PrivateView.vue')
    },

    {
      path: '/search-tender',
      name: 'Prozorro',
      component: () => import('@/views/ProzorroView.vue')
    }
  ], 
    
})


// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const publicPages = ['/signin', '/register', '/', '/about']
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !token) {
    return next('/signin')
  }
  next()
})
export default router
