<template>
  <div>
      <NavBar />
      <ErrorSuccessMessage /> 
    <div class="container mt-4">
      <h1>Welcome from Home</h1>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import NavBar from '@/components/Home/NavBar.vue';
import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';

export default {
  name: 'Home',
  components: {
    NavBar,
    ErrorSuccessMessage
  },
}
</script>

<style scoped>
/* Add your component styles here */
</style>
