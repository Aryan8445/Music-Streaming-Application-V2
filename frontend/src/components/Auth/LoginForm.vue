<!-- loginform.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <form @submit.prevent="login" class="p-4 border rounded bg-light shadow">
          <h3 class="text-center mb-4">User Login</h3>

          <!-- Email Input -->
          <div class="mb-3">
            <label for="email" class="form-label">Email Address</label>
            <input type="email" class="form-control" v-model="email" id="email" placeholder="Enter email" required>
          </div>

          <!-- Password Input -->
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" v-model="password" id="password" placeholder="Enter Password" required>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="alert alert-danger text-center" role="alert">
            {{ errorMessage }}
          </div>

          <!-- Success Message -->
          <div v-if="successMessage" class="alert alert-success text-center" role="alert">
            {{ successMessage }}
          </div>

          <!-- Login Button -->
          <div class="d-grid gap-2 col-6 mx-auto">
            <button type="submit" class="btn btn-primary">Login</button>
          </div>

          <!-- Signup Link -->
          <div class="mt-3 text-center">
            Don't have an account? <router-link to="/sign_up">Sign up</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        // Reset error and success messages
        this.$store.commit('setErrorMessage', '');
        this.$store.commit('setSuccessMessage', '');

        // Validate email and password fields
        if (!this.email || !this.password) {
          throw new Error('Please enter both email and password');
        }
        
        const response = await axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password
        });

        const { access_token, user_type } = response.data;

        // Store access token and user type in localStorage or Vuex store
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('user_type', user_type);

        // Redirect based on user type
        if (user_type === 'admin') {
          this.$router.push('/admin_dashboard');
        } else {
          this.$router.push('/home');
        }

        // Set success message
        this.$store.commit('setSuccessMessage', 'Login successful!');
      } catch (error) {
        console.error('Login failed:', error.message);
        // Set error message
        this.$store.commit('setErrorMessage', error.response.data.message || 'Login failed');
      }
    }
  }
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
