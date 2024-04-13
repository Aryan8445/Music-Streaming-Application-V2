<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8 ">
          <div class="p-4 border rounded bg-light shadow">
            <h3 class="text-center mb-4">Create Playlist</h3>

            <form @submit.prevent="createPlaylist">
              <div class="mb-3">
                <label for="playlistName" class="form-label h5">Playlist Name:</label>
                <input type="text" class="form-control" id="playlistName" v-model="playlistName" placeholder="Enter Playlist Name" required>
              </div>

              <table class="table table-striped">
                <thead>
                  <tr>
                    <th scope="col">S.No</th>
                    <th scope="col">Song Name</th>
                    <th scope="col">Artist</th>
                    <th scope="col">Add</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(song, index) in songs" :key="song.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ song.title }}</td>
                    <td>{{ song.artist }}</td>
                    <td>
                      <input type="checkbox" v-model="selectedSongs" :value="song.id">
                    </td>
                  </tr>
                </tbody>
              </table>

              <div class="text-center">
                <button type="submit" class="btn btn-success">Create Playlist</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/Home/NavBar.vue';
import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';
import axios from 'axios';
import { mapActions } from 'vuex';

export default {
  components: {
    NavBar,
    ErrorSuccessMessage,
  },
  data() {
    return {
      playlistName: '',
      songs: [],
      selectedSongs: [],
    };
  },
  methods: {
    ...mapActions(['displaySuccessMessage', 'displayErrorMessage']),
    async createPlaylist() {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.post('http://127.0.0.1:5000/api/playlists', {
          title: this.playlistName,
          song_ids: this.selectedSongs,
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.$router.push('/')
        this.displaySuccessMessage('Playlist created successfully');
        // Reset form fields
        this.playlistName = '';
        this.selectedSongs = [];
      } catch (error) {
        this.displayErrorMessage('Error creating playlist: ' + error.response.data.message);
      }
    },
    async fetchSongs() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/songs');
        this.songs = response.data;
      } catch (error) {
        console.error('Error fetching songs:', error);
      }
    },
  },
  mounted() {
    // Fetch songs when the component is mounted
    this.fetchSongs();
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
