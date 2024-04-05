<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Music Streaming App</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item" v-for="(navItem, index) in dynamicNavbarItems" :key="index">
              <router-link :to="navItem.route" class="nav-link">{{ navItem.label }}</router-link>
            </li>
          </ul>
          <form class="d-flex" @submit.prevent="search" v-if="isLoggedIn">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
          <button v-if="isLoggedIn" @click="logout" class="btn btn-outline-danger">Logout</button>
        </div>
      </div>
    </nav>

    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show w-75 mx-auto" role="alert">
      {{ errorMessage }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="clearErrorMessage"></button>
    </div>
    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show  w-75 mx-auto" role="alert">
      {{ successMessage }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="clearSuccessMessage"></button>
    </div>
    <div class="container mt-4">
      <!-- Content goes here -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: '', // Store search query
      user: null,
      userType: null,
      errorMessage: '',
      successMessage: ''
    };
  },
  computed: {
    
    isLoggedIn() {

      return localStorage.getItem('access_token') !== null;
    },
    dynamicNavbarItems() {
      // Define dynamic navbar items based on user's login status and user type
      const userType = localStorage.getItem('user_type');
      const isLoggedIn = this.isLoggedIn;

      // Default navbar items for guests
      let navItems = [];

      if (isLoggedIn) {
        // Add logged-in user's navbar items
        if (userType === 'admin') {
          navItems = [
            { label: 'Songs', route: '/all_songs' },
            { label: 'Users', route: '/all_users' },
            { label: 'Creators', route: '/all_creators' },
          ];
        } else if (userType === 'creator') {
          navItems = [
            { label: 'Home', route: '/home' },
            { label: 'Profile', route: '/profile' },
            { label: 'Creator Account', route: '/upload_song' },
            { label: 'Creator Dashboard', route: '/creator_dashboard' },
          ];
        } else {
          navItems = [
            { label: 'Home', route: '/home' },
            { label: 'Profile', route: '/profile' },
            { label: 'Creator Account', route: '/upload_song' },
          ];
        }
      } else {
        // Default navbar items for guests
        navItems = [
          { label: 'Login', route: '/login' },
          { label: 'Sign Up', route: '/sign_up' }
        ];
      }

      return navItems;
    }
  },
  methods: {
    async search() {
      // Implement search functionality based on the searchQuery
      console.log('Search query:', this.searchQuery);
      // Example: Redirect to search results page with query parameter
      this.$router.push({ path: '/search', query: { q: this.searchQuery } });
      // Clear search query after search
      this.searchQuery = '';
    },
    async clearErrorMessage() {
      this.errorMessage = '';
    },
    async clearSuccessMessage() {
      this.successMessage = '';
    },
    async logout() {
      try {
        // const response = await axios.post('/logout');
        // Clear access token and user type from localStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_type');
        // Redirect to login page after logout
        this.$router.push('/login');
        // Set success message
        this.successMessage = 'Logout successful!';
      } catch (error) {
        console.error('Logout failed:', error.message);
        // Set error message
        this.errorMessage = error.response.data.message || 'Logout failed';
      }
    }
  },
  created() {
    // Check user's login status on component creation
    const access_token = localStorage.getItem('access_token');
    if (access_token) {
      this.userType = localStorage.getItem('user_type');
      this.user = localStorage.getItem('user');
    }
  }
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
