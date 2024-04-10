<template>
  <div>
    <h2>Song List</h2>
    <ul>
      <li v-for="song in songs" :key="song.id">
        <div>{{ song.title }}</div>
        <div>Artist: {{ song.artist }}</div>
        <div>Release Date: {{ song.release_date }}</div>
        <div>Genre: {{ song.genre }}</div>
        <div>Lyrices: {{ song.lyrics }}</div>
        <div>
          <audio controls :src="song.file_path"></audio>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      songs: [],
    };
  },
  mounted() {
    // Fetch songs from the API when the component is mounted
    this.fetchSongs();
  },
  methods: {
    async fetchSongs() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/songs');
        this.songs = response.data; // Assuming the response contains an array of songs
      } catch (error) {
        console.error('Error fetching songs:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
