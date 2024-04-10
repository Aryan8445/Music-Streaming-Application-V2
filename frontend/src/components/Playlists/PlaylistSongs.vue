<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
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
                  {{ song.title }} - {{ song.artist }}
                  <div>
                    <!-- <router-link  class="btn btn-dark mx-2">Read Lyrics</router-link> -->
                    <!-- <router-link  class="btn btn-success mx-2">Play Song</router-link> -->
                    <button @click="removeSongFromPlaylist(song.id)" class="btn btn-danger mx-2">Remove</button>
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
  methods: {
    ...mapActions(['displaySuccessMessage', 'displayErrorMessage']),
    async fetchPlaylist() {
      try {
        const playlistId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://127.0.0.1:5000/api/playlists/${playlistId}/songs`, { headers: { Authorization: `Bearer ${token}` } });
        this.playlist = response.data;
      } catch (error) {
        console.error('Error fetching playlist:', error);
      }
    },
    async fetchAllSongs() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:5000/api/songs', { headers: { Authorization: `Bearer ${token}` } });
        this.allSongs = response.data;
      } catch (error) {
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
      } catch (error) {
        console.error('Error updating playlist name:', error);
      }
    },
    async removeSongFromPlaylist(songId) {
      try {
        const playlistId = this.$route.params.id;
        const token = localStorage.getItem('access_token');
        const response = await axios.delete(`http://127.0.0.1:5000/api/playlists/${playlistId}/delete-song/${songId}`, { headers: { Authorization: `Bearer ${token}` } });
        this.playlist = response.data;
      } catch (error) {
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
      } catch (error) {
        console.error('Error adding song to playlist:', error);
      }
    }
  },
  mounted() {
    this.fetchPlaylist();
    this.fetchAllSongs();
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
