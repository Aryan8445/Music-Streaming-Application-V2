<template>

    <Navbar />
    <router-view />
    <Footer />

</template>

<script>
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';

export default {
  /* eslint-disable */ 
  name: 'App',
  components: {
    Navbar,
    Footer
  }
};
</script>

<style>
/* Add global styles here */
</style>
