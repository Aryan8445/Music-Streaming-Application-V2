<template>
    <div class="lyrics-container">
      <NavBar />
      <ErrorSuccessMessage />
      <div class="container">
        <div class="song-details">
          <h1>{{ song.title }}</h1>
          <h2>By {{ song.artist }}</h2>
          <p>Release Date: {{ song.release_date }}</p>
          <p>Genre: {{ song.genre }}</p>
        </div>
  
        <div class="lyrics-section">
          <h2>Lyrics</h2>
          <pre v-if="song.lyrics">{{ song.lyrics }}</pre>
          <p v-else>No lyrics available</p>
        </div>
  
        <div class="rating-section" v-if="isAuthenticated">
          <div class="rating-input">
            <label for="rating" class="form-label">Rate this song:</label>
            <select id="rating" class="form-select" v-model="userRating" @change="rateSong">
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
            <span v-if="message" class="message">{{ message }}</span>
          </div>
  
          <div class="rating-info" v-if="averageRating !== null">
            <p>Average Rating: {{ averageRating }}/5.00</p>
          </div>
        </div>
  
        <div v-else>
          <div class="rating-info" v-if="averageRating !== null">
            <p>Average Rating: {{ averageRating }}/5.00</p>
          </div>
          <p>Please log in to rate this song. <router-link to="/login" class="btn btn-primary">Login</router-link></p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import NavBar from '@/components/Home/NavBar.vue';
  import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';
  
  export default {
    name: "ReadLyrics",
    components: {
      NavBar,
      ErrorSuccessMessage,
    },
    data() {
      return {
        song: {},
        userRating: null,
        averageRating: null,
        totalRatings: null,
        message: '',
      };
    },
    computed: {
      isAuthenticated() {
        return localStorage.getItem('access_token') !== null;
      },
    },
    methods: {
      fetchSong() {
        const songId = this.$route.params.id;
        axios.get(`http://127.0.0.1:5000/api/songs/${songId}`)
          .then((response) => {
            this.song = response.data;
            this.fetchRating();
          })
          .catch((error) => {
            console.error("Error fetching song:", error);
          });
      },
      fetchRating() {
        const songId = this.$route.params.id;
        axios.get(`http://127.0.0.1:5000/api/songs/${songId}/ratings`)
          .then((response) => {
            this.averageRating = response.data.average_rating.toFixed(2);
            this.totalRatings = response.data.total_ratings;
          })
          .catch((error) => {
            console.error("Error fetching rating:", error);
          });
      },
      rateSong() {
        const songId = this.$route.params.id;
        const accessToken = localStorage.getItem('access_token');
        const config = {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        };
        axios.post(`http://127.0.0.1:5000/api/songs/${songId}/ratings`, { value: this.userRating }, config)
          .then((response) => {
            this.message = response.data.message;
            this.fetchRating();
          })
          .catch((error) => {
            console.error("Error rating song:", error);
          });
      },
    },
    mounted() {
      this.fetchSong();
    },
  };
  </script>
  
  <style scoped>
  .container {
    margin: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .song-details {
    text-align: center;
  }
  
  .lyrics-section {
    margin-top: 30px;
    text-align: center;
  }
  
  .rating-section {
    margin-top: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .rating-input {
    margin-bottom: 10px;
  }
  
  .message {
    color: red;
  }
  </style>
  