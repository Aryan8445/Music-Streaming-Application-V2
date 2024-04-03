<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <form @submit.prevent="signup" class="p-4 border rounded bg-light shadow">
          <h3 class="text-center mb-4">User Signup</h3>

          <div class="mb-3">
            <label for="email" class="form-label">Email Address</label>
            <input type="email" class="form-control" v-model="email" id="email" placeholder="Enter email" required>
          </div>

          <div class="mb-3">
            <label for="firstName" class="form-label">First Name</label>
            <input type="text" class="form-control" v-model="firstName" id="firstName" placeholder="Enter first name" required>
          </div>

          <div class="mb-3">
            <label for="lastName" class="form-label">Last Name</label>
            <input type="text" class="form-control" v-model="lastName" id="lastName" placeholder="Enter last name" required>
          </div>

          <div class="mb-3">
            <label for="password1" class="form-label">Password</label>
            <input type="password" class="form-control" v-model="password1" id="password1" placeholder="Enter password" required>
          </div>

          <div class="mb-3">
            <label for="password2" class="form-label">Confirm Password</label>
            <input type="password" class="form-control" v-model="password2" id="password2" placeholder="Confirm password" required>
          </div>

          <div class="d-grid gap-2 col-6 mx-auto">
            <button type="submit" class="btn btn-primary">Signup</button>
          </div>

          <div class="mt-3 text-center">
            Already have an account? <router-link to="/login">Login</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignupForm',
  data() {
    return {
      email: '',
      firstName: '',
      lastName: '',
      password1: '',
      password2: '',
    };
  },
  methods: {
    async signup() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/signup', {
          email: this.email,
          firstName: this.firstName,
          lastName: this.lastName,
          password1: this.password1,
          password2: this.password2,
        });
        // Handle successful signup
        console.log('Signup successful:', response.data);
        // Redirect to login page or perform any other action
        this.$router.push('/login');
      } catch (error) {
        console.error('Signup failed:', error.response.data.message);
        // Handle signup failure (show error message, clear input fields, etc.)
      }
    },
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
