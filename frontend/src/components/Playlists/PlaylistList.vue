<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <h2 class="mb-4">All Playlists</h2>

          <div v-if="playlists.length === 0">
            <p>No playlists found.</p>
          </div>

          <div v-else>
            <div class="list-group">
              <router-link v-for="playlist in playlists" :key="playlist.id" :to="'/playlist-songs/' + playlist.id" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                <span>{{ playlist.title }}</span>
                <span class="badge bg-info rounded-pill">View Playlist</span>
              </router-link>
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

export default {
  components: {
    NavBar,
    ErrorSuccessMessage,
  },
  data() {
    return {
      playlists: [],
    };
  },
  methods: {
    async fetchPlaylists() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/playlists');
        this.playlists = response.data;
      } catch (error) {
        console.error('Error fetching playlists:', error);
      }
    },
  },
  mounted() {
    this.fetchPlaylists();
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
.list-group-item {
  cursor: pointer;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}
</style>
