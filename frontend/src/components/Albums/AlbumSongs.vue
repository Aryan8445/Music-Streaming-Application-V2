<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="playlist-container">
            <h2 class="mb-4">{{ album.title }}</h2>

            <!-- Update Album Title Section -->
            <div v-if="isCurrentUserArtist" class="mb-4">
              <h3 class="mb-3">Update Album Title</h3>
              <div class="input-group">
                <input v-model="newAlbumTitle" type="text" placeholder="Enter New Album Title" class="form-control">
                <button @click="updateAlbumTitle" class="btn btn-primary">Update</button>
              </div>
            </div>

            <!-- Songs in Album -->
            <div>
              <h3 class="mb-3">Songs in Album</h3>
              <ul class="list-group">
                <li v-for="song in album.songs" :key="song.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <h5 class="mb-0">{{ song.title }}</h5>
                    <p class="mb-0 text-muted">{{ song.artist }}</p>
                  </div>
                  <div>
                    <button @click="playSong(song.id)" class="btn btn-primary">Play Song</button>
                    <button @click="readLyrics(song.id)" class="btn btn-info">Read Lyrics</button>
                    <div v-if="isCurrentUserArtist">
                      <button @click="removeSongFromAlbum(song.id)" class="btn btn-danger ml-2">Remove</button>
                    </div>
                  </div>
                </li>
              </ul>
            </div>

            <!-- Add Songs to Album -->
            <div v-if="isCurrentUserArtist" class="mt-4">
              <h3 class="mb-3">Add Songs to Album</h3>
              <div class="input-group">
                <select v-model="selectedSong" class="form-select">
                  <option disabled value="">Select Song to Add</option>
                  <option v-for="song in allSongs" :key="song.id" :value="song.id">{{ song.title }} - {{ song.artist }}</option>
                </select>
                <button @click="addSongToAlbum" class="btn btn-primary">Add</button>
              </div>
            </div>
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
      album: {},
      newAlbumTitle: '',
      allSongs: [],
      selectedSong: null
    };
  },
  computed: {
    isCurrentUserArtist() {
      const currentUserEmail = localStorage.getItem('email');
      return this.album.artist_email === currentUserEmail;
    },
    errorMessage() {
      return this.$store.getters.errorMessage;
    },
  },
  methods: {
    ...mapActions(['displaySuccessMessage', 'displayErrorMessage', 'clearMessages']),
    async fetchAlbum() {
      try {
        const albumId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://127.0.0.1:5000/api/albums/${albumId}`, { headers: { Authorization: `Bearer ${token}` } });
        this.album = response.data;
      } catch (error) {
        this.displayErrorMessage('Error fetching album');
        console.error('Error fetching album:', error);
      }
    },
    async fetchAllSongs() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:5000/api/songs', { headers: { Authorization: `Bearer ${token}` } });
        this.allSongs = response.data;
      } catch (error) {
        this.displayErrorMessage('Error fetching songs');
        console.error('Error fetching all songs:', error);
      }
    },
    async updateAlbumTitle() {
      try {
        const albumId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.put(`http://127.0.0.1:5000/api/albums/${albumId}`, { title: this.newAlbumTitle }, { headers: { Authorization: `Bearer ${token}` } });
        this.album = response.data;
        this.newAlbumTitle = '';
        this.displaySuccessMessage('Album title updated successfully');
      } catch (error) {
        this.displayErrorMessage('Error updating album title');
        console.error('Error updating album title:', error);
      }
    },
    async removeSongFromAlbum(songId) {
      try {
        const albumId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.delete(`http://127.0.0.1:5000/api/albums/${albumId}/delete-song/${songId}`, { headers: { Authorization: `Bearer ${token}` } });
        this.album = response.data;
        this.displaySuccessMessage('Song removed from album successfully');
      } catch (error) {
        this.displayErrorMessage('Error removing song from album');
        console.error('Error removing song from album:', error);
      }
    },
    async addSongToAlbum() {
      try {
        const albumId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.post(`http://127.0.0.1:5000/api/albums/${albumId}/add-song`, { song_id: this.selectedSong }, { headers: { Authorization: `Bearer ${token}` } });
        this.album = response.data;
        this.selectedSong = null;
        this.displaySuccessMessage('Song added to album successfully');
      } catch (error) {
        this.displayErrorMessage('Error adding song to album');
        console.error('Error adding song to album:', error);
      }
    },
    playSong(songId) {
      // Implement play song functionality
    },
    readLyrics(songId) {
      // Implement read lyrics functionality
    }
  },
  mounted() {
    this.clearMessages();
    this.fetchAlbum();
    this.fetchAllSongs();
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
