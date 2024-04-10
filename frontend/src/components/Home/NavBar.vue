<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">Music Streaming App</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" v-if="userType !== 'admin'" to="/">Home</router-link>
          </li>
          <li class="nav-item" >
            <router-link class="nav-link" to="/all_songs">Songs</router-link>
          </li>
          <li class="nav-item" >
            <router-link class="nav-link" to="/all_songs">Albums</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="isLoggedIn" to="/profile">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-if="isLoggedIn && userType === 'user'" to="/upload-song">Creator Account</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn && userType === 'creator'">
            <router-link class="nav-link" to="/creator-dashboard">Creators Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/sign_up">Sign Up</router-link>
          </li>
        </ul>
        <form class="d-flex">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
        <button class="btn btn-outline-danger" @click="logout" v-if="isLoggedIn">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
    };
  },
  computed: {
    isLoggedIn() {
      return localStorage.getItem('access_token') !== null;
    },
    userType() {
      return localStorage.getItem('user_type')
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('clearMessages');
      localStorage.removeItem('access_token', null)
      localStorage.removeItem('user_type', null)
      localStorage.removeItem('expires_at', null)
      window.location.reload();
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
