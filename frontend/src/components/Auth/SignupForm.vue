<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <form @submit.prevent="signup" class="signup-form p-4 border rounded bg-light shadow">
            <h3 class="text-center mb-4">User Signup</h3>

            <div class="mb-3">
              <label for="email" class="form-label">Email Address</label>
              <input type="email" class="form-control" v-model="email" id="email" placeholder="Enter email" required>
              <div v-if="!isEmail(email)" class="invalid-feedback">Please enter a valid email address.</div>
            </div>

            <div class="mb-3">
              <label for="firstName" class="form-label">First Name</label>
              <input type="text" class="form-control" v-model="firstName" id="firstName" placeholder="Enter first name" required>
              <div v-if="!isUsername(firstName)" class="invalid-feedback">Please enter your first name.</div>
            </div>

            <div class="mb-3">
              <label for="lastName" class="form-label">Last Name</label>
              <input type="text" class="form-control" v-model="lastName" id="lastName" placeholder="Enter last name" required>
              <div v-if="!isUsername(lastName)" class="invalid-feedback">Please enter your last name.</div>
            </div>

            <div class="mb-3">
              <label for="password1" class="form-label">Password</label>
              <input type="password" class="form-control" v-model="password1" id="password1" placeholder="Enter password" required>
              <div v-if="!isPassword(password1)" class="invalid-feedback">Password must be at least 4 characters long.</div>
            </div>

            <div class="mb-3">
              <label for="password2" class="form-label">Confirm Password</label>
              <input type="password" class="form-control" v-model="password2" id="password2" placeholder="Confirm password" required>
              <div v-if="password1 !== password2" class="invalid-feedback">Passwords do not match.</div>
            </div>

            <!-- User Role Dropdown -->
            <div class="mb-3">
              <label for="userRole" class="form-label">User Role</label>
              <select v-model="userRole" class="form-select" id="userRole">
                <option value="user">User</option>
                <option value="creator">Creator</option>
              </select>
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
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from '@/components/Home/NavBar.vue';
import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';
import store from '@/store'; // Import Vuex store

export default {
  name: 'SignupForm',
  data() {
    return {
      email: '',
      firstName: '',
      lastName: '',
      password1: '',
      password2: '',
      userRole: 'user' // Default user role
    };
  },
  components:{
    NavBar,
    ErrorSuccessMessage
  },
  methods: {
    isEmail(str) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(str);
    },
    isUsername(str) {
      return str.length > 0;
    },
    isPassword(str) {
      return str.length >= 4;
    },
    async signup() {
      if (
        !this.isEmail(this.email) ||
        !this.isUsername(this.firstName) ||
        !this.isUsername(this.lastName) ||
        !this.isPassword(this.password1) ||
        this.password1 !== this.password2
      ) {
        // If any validation fails, set error message using Vuex
        store.dispatch('displayErrorMessage', 'Invalid input. Please check your inputs and try again.');
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:5000/signup', {
          email: this.email,
          firstName: this.firstName,
          lastName: this.lastName,
          password1: this.password1,
          password2: this.password2,
          userRole: this.userRole // Include the selected user role in the request
        });
        // Handle successful signup
        console.log('Signup successful:', response.data);
        // Redirect to login page or perform any other action
        this.$router.push('/login');
        // Dispatch success message to Vuex store
        store.dispatch('displaySuccessMessage', 'Signup successful');
      } catch (error) {
        console.error('Signup failed:', error.response.data.message);
        // Set error message using Vuex
        store.dispatch('displayErrorMessage', error.response.data.message || 'Signup failed');
      }
    },
  },
};
</script>

<style scoped>
.signup-form {
  max-width: 400px;
  margin: 0 auto;
}

.signup-form .form-label {
  font-weight: bold;
}

.signup-form .btn-primary {
  width: 100%;
}
</style>
