<template>
    <div class="col mb-4"> <!-- Adjust the column width -->
      <div class="card h-100 shadow-sm playlist-card">
        <img :src="playlist.imageUrl || require('@/assets/img/playlist.jpg')" class="card-img-top playlist-image" alt="Playlist Image"> <!-- Use different image -->
        <div class="card-body">
          <h5 class="card-title text-center text-dark">{{ playlist.title }}</h5>
          <div class="d-flex justify-content-center">
            <router-link :to="'/playlist-songs/' + playlist.id" class="btn btn-outline-info btn-sm">View Playlist</router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PlaylistCard',
    props: {
      playlist: {
        type: Object,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  .card {
    border: none;
    border-radius: 10px;
    transition: transform 0.3s ease-in-out;
  }
  
  .card:hover {
    transform: translateY(-5px);
  }
  
  .playlist-card {
    background-color: #f8f9fa; /* Light gray background */
    position: relative;
    width: 250px; /* Adjust the card width */
  }
  
  .playlist-image {
    height: 200px; /* Adjust the playlist image height */
    object-fit: cover;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }
  
  .card-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.3rem;
  }
  
  .card-text {
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }
  
  .btn {
    border-radius: 20px;
    width: 120px; /* Adjust the button width */
  }
  
  .btn-outline-info {
    color: #17a2b8;
    border-color: #17a2b8;
  }
  
  .btn-outline-info:hover {
    background-color: #17a2b8;
    color: #fff;
  }
  </style>
  