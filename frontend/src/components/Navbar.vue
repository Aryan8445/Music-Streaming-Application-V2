<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link to="/" class="navbar-brand">Music Streaming App</router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/playlists" class="nav-link">Playlists</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/albums" class="nav-link">Albums</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/profile" class="nav-link">Profile</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    /* eslint-disable */ 
    name: 'Navbar'
  };
  </script>
  
  <style scoped>
  /* Add your custom styles for Navbar.vue here */
  .navbar-brand {
    font-weight: bold;
  }
  .navbar-nav .nav-item {
    margin-right: 10px;
  }
  </style>
  

