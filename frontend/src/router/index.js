import { createRouter, createWebHistory } from 'vue-router';
import axios from 'axios';
import store from '../store'; // Import the Vuex store

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/Auth/LoginForm.vue'),
  },
  {
    path: '/sign_up',
    name: 'Signup',
    component: () => import('../components/Auth/SignupForm.vue'),
  },
  {
    path: '/play/:id',
    name: 'Play',
    component: () => import('../components/Songs/PlaySong.vue'),
  },
  {
    path: '/lyrics/:id',
    name: 'Lyrics',
    component: () => import('../components/Songs/ReadLyrics.vue'),
  },
  {
    path: '/search',
    name: 'SearchResults',
    component: () => import('../components/Home/SearchResults.vue'),
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: () => import('../components/Auth/UserProfile.vue'),
    meta: { requiresAuth: true } // Protected route, requires authentication
  },
  {
    path: '/upload-song',
    name: 'UploadSong',
    component: () => import('../components/Songs/UploadSong.vue'),
    meta: { requiresAuth: true} // Protected route, requires authentication
  },
  {
    path: '/update-song/:id',
    name: 'UpdateSong',
    component: () => import('../components/Songs/UpdateSong.vue'),
    meta: { requiresAuth: true} // Protected route, requires authentication
  },
  {
    path: '/create-playlist',
    name: 'CreatePlaylist',
    component: () => import('../components/Playlists/CreatePlaylist.vue'),
    meta: { requiresAuth: true} // Protected route, requires authentication
  },
  {
    path: '/create-Album',
    name: 'CreateAlbum',
    component: () => import('../components/Albums/CreateAlbum.vue'),
    meta: { requiresAuth: true, isCreator: true} // Protected route, requires authentication
  },
  {
    path: '/playlist-songs/:id',
    name: 'PlaylistSongs',
    component: () => import('../components/Playlists/PlaylistSongs.vue'),
    meta: { requiresAuth: true} // Protected route, requires authentication
  },
  {
    path: '/album-songs/:id',
    name: 'AlbumSongs',
    component: () => import('../components/Albums/AlbumSongs.vue'), 
  },
  {
    path: '/creator-dashboard',
    name: 'CreatorDashboard',
    component: () => import('../components/Auth/CreatorDashboard.vue'),
    meta: { requiresAuth: true, isCreator: true  } // Protected route, requires authentication
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: () => import('../components/Auth/AdminDashboard.vue'), 
    meta: { requiresAuth: true, isAdmin: true } // Protected route for admin only
  },
  {
    path: '/all-songs',
    name: 'AllSongs',
    component: () => import('../components/Songs/AllSongs.vue'), 
    meta: { requiresAuth: true, isAdmin: true } // Protected route for admin only
  },
  {
    path: '/all-albums',
    name: 'AllAlbums',
    component: () => import('../components/Albums/AllAlbums.vue'), 
    meta: { requiresAuth: true, isAdmin: true } // Protected route for admin only
  },
  {
    path: '/all-users',
    name: 'AllUsers',
    component: () => import('../components/Auth/AllUsers.vue'), 
    meta: { requiresAuth: true, isAdmin: true } // Protected route for admin only
  },
  {
    path: '/all-creators',
    name: 'AllCreators',
    component: () => import('../components/Auth/AllCreators.vue'), 
    meta: { requiresAuth: true, isAdmin: true } // Protected route for admin only
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Navigation guard to check authentication status before accessing protected routes
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        // Send the JWT token with the request to the backend for validation
        const response = await axios.get('http://127.0.0.1:5000/protected', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        // If the token is valid, allow access to the route
        if (response.status === 200) {
          if (to.meta.isAdmin && localStorage.getItem('user_type') !== 'admin') {
            // If the user is not an admin and tries to access the admin dashboard, redirect to home
            next('/');
          } 
          else if (to.meta.isCreator && localStorage.getItem('user_type') !== 'creator') {
            // If the user is not a creator and tries to access the creator dashboard, redirect to home
            next('/');
          } 
          else {
            next();
          }
        } else {
          // If the token is invalid, redirect to the login page
          store.dispatch('displayErrorMessage', 'Authentication failed. Please login again.');
          next('/login');
        }
      } catch (error) {
        console.error('Authentication failed:', error);
        store.dispatch('displayErrorMessage', 'Authentication failed. Please login again.');
        next('/login');
      }
    } else {
      // If the token is missing, redirect to the login page
      next('/login');
    }
  } else {
    // Allow access to non-protected routes
    next();
  }
});

export default router;
