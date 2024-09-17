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
      path: '/notifications',
      name: 'notifications',
      component: () => import('../views/NotificationsView.vue')
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
    },
    {
      path: "/admin/users",
      name: "admin-users",
      component: () => import('../views/admin/AdminUsersView.vue')
    },
    {
      path: "/admin/shops",
      name: "admin-shops",
      component: () => import('../views/admin/AdminShopsView.vue')
    },
    {
      path: "/admin/reservations",
      name: "admin-reservations",
      component: () => import('../views/admin/AdminShopsView.vue')
    },
    {
      path: "/admin/settings",
      name: "admin-settings",
      component: () => import('../views/admin/AdminSettingsView.vue')
    }
  ]
})

export default router
