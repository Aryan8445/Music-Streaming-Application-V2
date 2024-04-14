<template>
  <div>
    <h1>User Profile</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <p>Email: {{ userProfile.email }}</p>
      <p>Name: {{ userProfile.name }}</p>
      <p>User Type: {{ userProfile.user_type }}</p>
      <p>Registration Date: {{ userProfile.registration_date }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      loading: true,
      userProfile: {}
    };
  },
  mounted() {
    // Fetch user profile data
    this.fetchUserProfile();
  },
  methods: {
    fetchUserProfile() {
      // Assuming you have axios installed
      axios.get('/api/user')
        .then(response => {
          this.userProfile = response.data;
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching user profile:', error);
          this.loading = false;
        });
    }
  }
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
