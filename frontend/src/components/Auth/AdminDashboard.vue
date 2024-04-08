<template>
    <div>
      <NavBar />
      <ErrorSuccessMessage />
      <h2>Admin Dashboard</h2>
      <!-- Add admin dashboard content and features here -->
    </div>
  </template>
  
  <script>
  import NavBar from '@/components/Home/NavBar.vue';
import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';

  export default {
    name: 'AdminDashboard',
  };
  </script>
  
  <style>
  /* Add styles for the AdminDashboard component */
  </style>
  