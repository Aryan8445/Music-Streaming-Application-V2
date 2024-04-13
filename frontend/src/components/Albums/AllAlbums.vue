<template>
    <div>
      <NavBar/>
      <ErrorSuccessMessage/>
    </div>
    <div class="container mt-4 ">
      <h2 class="text-center text-warning ">All Albums</h2>
      <div v-if="albums">
        <table class="table table-striped table-hover shadow">
          <!-- Table header -->
          <thead class="table-dark">
            <tr>
              <th scope="col">S.No</th>
              <th scope="col">Album Title</th>
              <th scope="col">Artist</th>
              <th scope="col text-center">Actions</th>
            </tr>
          </thead>
          <!-- Table body -->
          <tbody>
            <!-- Loop through all albums and display each album -->
            <tr v-for="(album, index) in albums" :key="album.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ album.title }}</td>
              <td>{{ album.artist }}</td>
              <!-- Buttons for actions -->
              <td class="text-end">
                <!-- Delete button -->
                <button class="btn btn-outline-danger btn-sm mx-2" @click="deleteAlbum(album.id)">Delete Album</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import NavBar from '@/components/Home/NavBar.vue';
  import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';
  
  export default {
    components: {
      NavBar,
      ErrorSuccessMessage,
    },
    data() {
      return {
        albums: null,
      };
    },
    mounted() {
      this.fetchAlbums();
    },
    methods: {
      fetchAlbums() {
        const accessToken = localStorage.getItem('access_token');
        axios.get(`http://127.0.0.1:5000/api/albums`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then(response => {
          this.albums = response.data;
        })
        .catch(error => {
          console.error('Error fetching albums:', error);
            this.$store.dispatch('displayErrorMessage', 'Error fetching albums');
        });
      },
      deleteAlbum(albumId) {
        const accessToken = localStorage.getItem('access_token');
        axios.delete(`http://127.0.0.1:5000/api/albums/${albumId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then(response => {

          this.albums = this.albums.filter(album => album.id !== albumId);
          console.log('Album deleted successfully:', response.data);
          this.$store.dispatch('displaySuccessMessage', 'Album deleted successfully');
        })
        .catch(error => {
          console.error('Error deleting album:', error);
          this.$store.dispatch('displayErrorMessage', 'Error deleting album');
        });
      },
    },
  };
  </script>
  
  <style scoped>
  
  </style>
  