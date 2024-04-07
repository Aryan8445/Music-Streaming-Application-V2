import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import LoginForm from '../components/Auth/LoginForm';
import SignupForm from '../components/Auth/SignupForm';
import UserProfile from '../components/Auth/UserProfile.vue';
import CreatorDashboard from '../components/Auth/CreatorDashboard.vue';
import AdminDashboard from '../components/Auth/AdminDashboard.vue';
import AuthService from '../services/AuthService';

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm,
  },
  {
    path: '/sign_up',
    name: 'Signup',
    component: SignupForm,
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true } // Protected route, requires authentication
  },
  {
    path: '/creator-dashboard',
    name: 'CreatorDashboard',
    component: CreatorDashboard,
    meta: { requiresAuth: true } // Protected route, requires authentication
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true } // Protected route, requires authentication
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Navigation guard to check authentication status before accessing protected routes
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    // Check if the user is authenticated
    const isAuthenticated = AuthService.isAuthenticated(); // Implement this method in AuthService.js
    if (isAuthenticated) {
      // Proceed to the route
      next();
    } else {
      // Redirect to the login page if not authenticated
      next('/login');
    }
  } else {
    // Allow access to non-protected routes
    next();
  }
});

export default router;
