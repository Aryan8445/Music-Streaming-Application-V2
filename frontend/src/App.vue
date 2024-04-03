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

            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/home">Home</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/profile">Profile</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn && user === 'user'">
              <router-link class="nav-link" to="/upload_song">Creator Account</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn && user === 'creator'">
              <router-link class="nav-link" to="/creator_dashboard">Creator Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <a class="nav-link" href="/logout" @click="logout">Logout</a>
            </li>
          </ul>
          <div class="d-flex" v-if="isLoggedIn">
            <form class="d-flex" @submit.prevent="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="query" />
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
          </div>
          <ul class="navbar-nav ms-auto" v-else>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/sign_up">Sign Up</router-link>
            </li>
          </ul>
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
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['errorMessage', 'successMessage']),
    user() {
      return this.$store.state.user;
    },
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    }
  },
  created() {
    this.checkLoggedIn();
  },
  methods: {
    async logout() {
      try {
        await axios.post('/api/logout');
        localStorage.removeItem('access_token');
        this.$store.commit('setUser', null);
        this.$store.commit('setLoggedIn', false);
        this.$router.push('/login');
      } catch (error) {
        console.error('Logout failed:', error);
        // Handle error
      }
    },
    async checkLoggedIn() {
      const access_token = localStorage.getItem('access_token');
      if (access_token) {
        try {
          const response = await axios.get('/api/protected');
          const { logged_in_as } = response.data;
          this.$store.commit('setUser', logged_in_as);
          this.$store.commit('setLoggedIn', true);
        } catch (error) {
          console.error('User not authenticated:', error);
          // Handle error
        }
      }
    },
    clearErrorMessage() {
      this.$store.commit('setErrorMessage', '');
    },
    clearSuccessMessage() {
      this.$store.commit('setSuccessMessage', '');
    }
  },
};
</script>
