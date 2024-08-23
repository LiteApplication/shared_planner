import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/reservations',
      name: 'reservations',
      component: () => import('../views/ReservationsView.vue')
    },
    {
      path: "/shops",
      name: "shops",
      component: () => import('../views/ShopsView.vue')
    },
    {
      path: '/shops/:id',
      name: 'shop',
      component: () => import('../views/ShopView.vue')
    }
  ]
})

export default router
