import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/LoginView.vue';
import Signup from '../views/SignupView.vue';
import UserProfile from '../views/UserProfile.vue';
import CreatorProfile from '../views/CreatorDashboard.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import LandingPage from '../views/LandingPage.vue';
import SignupView from '@/views/SignupView.vue';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/sign_up',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile,
  },
  {
    path: '/creator-profile',
    name: 'CreatorProfile',
    component: CreatorProfile,
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
