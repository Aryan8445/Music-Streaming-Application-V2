<template>
  <div>
    <NavBar/>
    <ErrorSuccessMessage/>

    <br>

    <!-- Welcome message and stats -->
    <div class="rounded-div" style="background-color: aliceblue;">
      <!-- User information -->
      <div class="container">
        <h3>Welcome, {{ user.artist_firstname }} {{ user.artist_lastname }}</h3>
      </div>

      <!-- Stats -->
      <div class="container text-center">
        <!-- Statistics cards -->
        <div class="row">
          <!-- Total songs uploaded -->
          <div class="col-md rounded-div">
            <h5>Total songs uploaded</h5>
            <h3>{{ user.total_songs_uploaded }}</h3>
          </div>
          <!-- Average rating -->
          <div class="col-md rounded-div">
            <h5>Average rating</h5>
            <h3>{{ user.average_rating }}</h3>
          </div>
          <!-- Total albums -->
          <div class="col-md rounded-div">
            <h5>Total albums</h5>
            <h3>{{ user.total_albums }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Your Uploads section -->
    <div class="container mt-4">
      <div class="row">
        <div class="col">
          <h3>Your Uploads</h3>
        </div>
        <div class="col text-end">
          <!-- Buttons for actions -->
          <router-link to="/upload-song" class="btn btn-outline-success mx-2"><strong>Upload Song</strong></router-link>
          <router-link to="/flagged_songs" class="btn btn-outline-warning mx-2"><strong>Flagged Songs</strong></router-link>
        </div>
      </div>
      <!-- Table for listing songs -->
      <table class="table table-striped table-hover">
        <!-- Table header -->
        <thead class="table-dark">
          <tr>
            <th scope="col">S.No</th>
            <th scope="col">Song Name</th>
            <th scope="col">Actions</th> <!-- Added new column for actions -->
          </tr>
        </thead>
        <!-- Table body -->
        <tbody>
          <!-- Loop through songs and display each song -->
          <tr v-for="(song, index) in user.songs" :key="song.id">
            <th scope="row">{{ index + 1 }}</th>
            <td>
              <!-- Song title and artist name -->
              <h5>{{ song.title }}</h5><em>{{ song.artist }}</em>
            </td>
            <!-- Buttons for actions -->
            <td class="text-end">
              <router-link :to="'/update-song/' + song.id" class="btn btn-info btn-sm mx-2">Update Song</router-link>
              <button class="btn btn-danger btn-sm mx-2" @click="deleteSong(song.id)">Delete Song</button> <!-- Added delete button -->
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Your Albums section -->
    <div class="container mt-4">
      <div class="row">
        <div class="col">
          <h3>Your Albums</h3>
        </div>
        <div class="col text-end">
          <router-link to="/create-album" style="border-radius: 20px;"
              class="btn btn-outline-primary "><strong>Create Album</strong></router-link>
        </div>
      </div>
      <!-- Table for listing albums -->
      <table class="table table-striped table-hover">
        <!-- Table header -->
        <thead class="table-dark">
          <tr>
            <th scope="col">S.No</th>
            <th scope="col">Album Title</th>
            <th scope="col">Actions</th> <!-- Added new column for actions -->
          </tr>
        </thead>
        <!-- Table body -->
        <tbody>
          <!-- Loop through albums and display each album -->
          <tr v-for="(album, index) in user.albums" :key="album.id">
            <th scope="row">{{ index + 1 }}</th>
            <td>
              <!-- Album title -->
              <h5>{{ album.title }}</h5>
            </td>
            <!-- Buttons for actions -->
            <td class="text-end">
              <router-link :to="'/album-songs/' + album.id" class="btn btn-info btn-sm mx-2">View Album</router-link>
              <button class="btn btn-danger btn-sm mx-2" @click="deleteAlbum(album.id)">Delete Album</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/Home/NavBar.vue';
import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';
import axios from 'axios'; // Import Axios library for making HTTP requests

export default {
  components: {
    NavBar,
    ErrorSuccessMessage,
  },

  data() {
    return {
      // Data properties to hold user information, statistics, flash messages, and song data
      user: {}, // User information
    };
  },

  methods: {
    // Method to fetch user information, statistics, and songs data
    fetchData() {
      // Perform API requests to fetch data and update the corresponding data properties
      axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
      axios.get(`http://127.0.0.1:5000/api/creator-dashboard`)
        .then(response => {
          this.user = response.data;
        })
        .catch(error => {
          console.error('Error fetching creator dashboard data:', error);
        });
    },

    // Method to delete a song
    deleteSong(songId) {
      axios.delete(`http://127.0.0.1:5000/api/songs/${songId}`)
        .then(response => {
          // Refresh songs after deletion
          this.fetchData();
          console.log('Song deleted successfully:', response.data);
          this.$store.dispatch('displaySuccessMessage', 'Song deleted successfully');
        })
        .catch(error => {
          console.error('Error deleting song:', error);
          this.$store.dispatch('displayErrorMessage', 'Error deleting song');
        });
    },

    // Method to update a song
    updateSong(song) {
      // Implement navigation or modal for updating the song
      console.log('Update song:', song);
    },



    // Method to delete an album
    deleteAlbum(albumId) {
      axios.delete(`http://127.0.0.1:5000/api/albums/${albumId}`)
        .then(response => {
          // Refresh albums after deletion
          this.fetchData();
          console.log('Album deleted successfully:', response.data);
          this.$store.dispatch('displaySuccessMessage', 'Album deleted successfully');
        })
        .catch(error => {
          console.error('Error deleting album:', error);
          this.$store.dispatch('displayErrorMessage', 'Error deleting album!');
        });
    },

    // Method to edit an album
  },

  mounted() {
    // Call the fetchData method when the component is mounted
    this.fetchData();
  }
};
</script>

<style>
  .rounded-div {
    border-radius: 15px;
    padding: 20px;
    background-color: #f0f0f0;
    margin: 20px;
  }
  .btn {
  border-radius: 20px;
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
