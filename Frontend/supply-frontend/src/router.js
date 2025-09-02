import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from './components/UserLogin.vue';
import UserSignup from './components/UserSignup.vue';
import UserDashboard from './views/UserDashboard.vue';
import UserWarehouse from './views/UserWarehouse.vue';
import UserVendors from './views/UserVendors.vue'; // <-- Add this import

const routes = [
  {
    path: '/login',
    name: 'login',
    component: UserLogin,
    meta: { layout: 'auth' }
  },
  {
    path: '/signup',
    name: 'signup',
    component: UserSignup,
    meta: { layout: 'auth' }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, layout: 'default' }
  },
  {
    path: '/warehouses',
    name: 'warehouses',
    component: UserWarehouse,
    meta: { requiresAuth: true, layout: 'default' }
  },
  {
    path: '/vendors', // <-- Add this route
    name: 'vendors',
    component: UserVendors,
    meta: { requiresAuth: true, layout: 'default' }
  },
  {
    path: '/',
    redirect: '/login'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Auth guard: checks for 'access' token in localStorage
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem('access')) {
    next({ path: '/login' });
  } else {
    next();
  }
});

export default router;


