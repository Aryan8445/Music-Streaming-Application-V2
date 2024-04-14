<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="playlist-container">
            <h2>{{ playlist.title }}</h2>

            <div class="mb-3">
              <input v-model="newPlaylistName" type="text" placeholder="New Playlist Name" class="form-control">
              <button @click="updatePlaylistName" class="btn btn-primary mt-2">Update Playlist Name</button>
            </div>

            <div>
              <h3>Songs in Playlist</h3>
              <ul class="list-group">
                <li v-for="song in playlist.songs" :key="song.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <p class="mb-0">{{ song.title }}</p>
                    <p class="mb-0 text-muted">{{ song.artist }}</p>
                  </div>
                  <div>
                    <router-link :to="'/play/' + song.id" class="btn btn-outline-success mx-2 btn-sm">Play Song</router-link>
                    <router-link :to="'/lyrics/' + song.id" class="btn btn-outline-info mx-2 btn-sm">Read Lyrics</router-link>
                    <button @click="removeSongFromPlaylist(song.id)" class="btn btn-outline-danger btn-sm mx-2">Remove</button>
                  </div>
                </li>
              </ul>
            </div>

            <div class="mt-4">
              <h3>Add Songs to Playlist</h3>
              <select v-model="selectedSong" class="form-select">
                <option v-for="song in allSongs" :key="song.id" :value="song.id">{{ song.title }} - {{ song.artist }}</option>
              </select>
              <button @click="addSongToPlaylist" class="btn btn-primary mt-2">Add Song to Playlist</button>
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
      playlist: {},
      newPlaylistName: '',
      allSongs: [],
      selectedSong: null
    };
  },
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage;
    },
    successMessage() {
      return this.$store.getters.successMessage;
    }
  },
  methods: {
    ...mapActions(['displaySuccessMessage', 'displayErrorMessage', 'clearMessages']),
    async fetchPlaylist() {
      try {
        const playlistId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://127.0.0.1:5000/api/playlists/${playlistId}/songs`, { headers: { Authorization: `Bearer ${token}` } });
        this.playlist = response.data;
      } catch (error) {
        this.displayErrorMessage('Error fetching playlist');
        console.error('Error fetching playlist:', error);
      }
    },
    async fetchAllSongs() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:5000/api/songs', { headers: { Authorization: `Bearer ${token}` } });
        this.allSongs = response.data;
      } catch (error) {
        this.displayErrorMessage('Error fetching all songs');
        console.error('Error fetching all songs:', error);
      }
    },
    async updatePlaylistName() {
      try {
        const playlistId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.put(`http://127.0.0.1:5000/api/playlists/${playlistId}`, { title: this.newPlaylistName }, { headers: { Authorization: `Bearer ${token}` } });
        this.playlist = response.data;
        this.newPlaylistName = '';
        this.displaySuccessMessage('Playlist name updated successfully');
      } catch (error) {
        this.displayErrorMessage('Error updating playlist name');
        console.error('Error updating playlist name:', error);
      }
    },
    async removeSongFromPlaylist(songId) {
      try {
        const playlistId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.delete(`http://127.0.0.1:5000/api/playlists/${playlistId}/delete-song/${songId}`, { headers: { Authorization: `Bearer ${token}` } });
        this.playlist = response.data;
        this.displaySuccessMessage('Song removed from playlist successfully');
      } catch (error) {
        this.displayErrorMessage('Error removing song from playlist');
        console.error('Error removing song from playlist:', error);
      }
    },
    async addSongToPlaylist() {
      try {
        const playlistId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.post(`http://127.0.0.1:5000/api/playlists/${playlistId}/add-song`, { song_id: this.selectedSong }, { headers: { Authorization: `Bearer ${token}` } });
        this.playlist = response.data;
        this.selectedSong = null;
        this.displaySuccessMessage('Song added to playlist successfully');
      } catch (error) {
        this.displayErrorMessage('Error adding song to playlist');
        console.error('Error adding song to playlist:', error);
      }
    }
  },
  mounted() {
    this.clearMessages();
    this.fetchPlaylist();
    this.fetchAllSongs();
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
.playlist-container {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
}

input[type="text"] {
  border-radius: 5px;
}

.list-group-item {
  border: none;
}

.btn-sm {
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .col-lg-8 {
    max-width: 100%;
  }
}
</style>
