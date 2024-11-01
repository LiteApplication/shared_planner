import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      path: '/reset_password/:token/:first_setup',
      name: 'reset_password',
      component: () => import('../views/ResetPasswordView.vue')
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: () => import('../views/NotificationsView.vue')
    },
    {
      path: '/',
      name: 'reservations',
      component: () => import('../views/ReservationsView.vue')
    },
    {
      path: "/shops",
      name: "shops",
      component: () => import('../views/ShopsView.vue')
    },
    {
      path: '/shops/:id/:week',
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
      component: () => import('../views/admin/AdminReservationsView.vue')
    },
    {
      path: "/admin/settings",
      name: "admin-settings",
      component: () => import('../views/admin/AdminSettingsView.vue')
    }
  ]
})

router.onError((error, to) => {
  if (error.message.includes('Failed to fetch dynamically imported module') || error.message.includes("Importing a module script failed") || error.message.includes("Loading chunk") || error.message.includes("dynamically imported module")) {
    window.location.href = to.fullPath
  }
})

export default router
