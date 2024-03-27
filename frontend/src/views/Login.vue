<template>
  <div>
    <!-- Login Component -->
    <div class="login-page">
      <div class="login-container">
        <Login @login="login"></Login>
      </div>
    </div>

  </div>
</template>

<script>
/* eslint-disable */
import Login from '@/components/Auth/Login.vue';
// Import Navbar and Footer components if available
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';

export default {
  components: {
    Login, // Register the Login component
    Navbar,
    Footer
  },
  methods: {
    login() {
      // Perform login logic here
    }
  }
};
</script>

<style scoped>
/* Add any specific styles for the landing page */
</style>
