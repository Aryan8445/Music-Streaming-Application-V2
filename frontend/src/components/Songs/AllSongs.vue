<template>
  <div>
    <NavBar/>
    <ErrorSuccessMessage/>
  </div>
  <div class="container mt-4">
    <!-- Other content -->
    <div class="container mt-4">
      <h2 class="text-center text-warning">All Songs</h2>
      <div v-if="songs">
        <table class="table table-striped table-hover">
          <!-- Table header -->
          <thead class="table-dark">
            <tr>
              <th scope="col">S.No</th>
              <th scope="col">Song Name</th>
              <th scope="col">Genre</th>
              <th scope="col text-center">Actions</th>
            </tr>
          </thead>
          <!-- Table body -->
          <tbody>
            <!-- Loop through all songs and display each song -->
            <tr v-for="(song, index) in songs" :key="song.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>
                <!-- Song title and artist name -->
                <h5>{{ song.title }}</h5><em>{{ song.artist }}</em>
              </td>
              <!-- Genre -->
              <td>{{ song.genre }}</td>
              <!-- Buttons for actions -->
              <td class="text-end">
                <!-- Delete button -->
                <button class="btn btn-outline-danger btn-sm mx-2" @click="deleteSong(song.id)">Delete Song</button>
                <!-- Flag or Unflag button -->
                <button v-if="!song.is_flagged" class="btn btn-outline-info btn-sm mx-2" @click="flagSong(song.id)">Flag Song</button>
                <button v-if="song.is_flagged" class="btn btn-outline-secondary btn-sm mx-2" @click="unflagSong(song.id)">Unflag Song</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
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
      songs: null,
    };
  },
  mounted() {
    this.fetchSongs();
  },
  methods: {
    fetchSongs() {
      const accessToken = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/songs`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        this.songs = response.data;
      })
      .catch(error => {
        console.error('Error fetching songs:', error);
        // Handle error
      });
    },
    deleteSong(songId) {
      const accessToken = localStorage.getItem('access_token');
      axios.delete(`http://127.0.0.1:5000/api/songs/${songId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        // Remove the deleted song from the list
        this.songs = this.songs.filter(song => song.id !== songId);
        console.log('Song deleted successfully:', response.data);
        this.$store.dispatch('displaySuccessMessage', 'Song deleted successfully');
      })
      .catch(error => {
        console.error('Error deleting song:', error);
        this.$store.dispatch('displayErrorMessage', 'Error deleting song');
      });
    },
    flagSong(songId) {
      const accessToken = localStorage.getItem('access_token');
      axios.post(`http://127.0.0.1:5000/api/songs/${songId}/flag`, {}, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        // Update the song's flag status
        const updatedSong = this.songs.find(song => song.id === songId);
        if (updatedSong) {
          updatedSong.is_flagged = true;
        }
        console.log('Song flagged successfully:', response.data);
        this.$store.dispatch('displaySuccessMessage', 'Song flagged successfully');
      })
      .catch(error => {
        console.error('Error flagging song:', error);
        this.$store.dispatch('displayErrorMessage', 'Error flagging song');
      });
    },
    unflagSong(songId) {
      const accessToken = localStorage.getItem('access_token');
      axios.delete(`http://127.0.0.1:5000/api/songs/${songId}/flag`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        // Update the song's flag status
        const updatedSong = this.songs.find(song => song.id === songId);
        if (updatedSong) {
          updatedSong.is_flagged = false;
        }
        console.log('Song unflagged successfully:', response.data);
        this.$store.dispatch('displaySuccessMessage', 'Song unflagged successfully');
      })
      .catch(error => {
        console.error('Error unflagging song:', error);
        this.$store.dispatch('displayErrorMessage', 'Error unflagging song');
      });
    },
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
