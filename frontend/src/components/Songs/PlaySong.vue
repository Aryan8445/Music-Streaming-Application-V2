<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />
    <div class="container mt-5">
      <div class="song-details p-4 rounded bg-light shadow">
        <div class="row">
          <div class="col">
            <h1 class="mb-3">{{ song.title }}</h1>
            <h2 class="text-muted mb-4">By {{ song.artist }}</h2>
            <p class="mb-3"><strong>Release Date:</strong> {{ song.release_date }}</p>
            <p class="mb-3"><strong>Genre:</strong> {{ song.genre }}</p>
          </div>
          <div class="col">
            <div v-if="isAuthenticated" class="rating-section">
              <div class="row">
                <div class="col">
                  <div class="rating-input p-2 rounded ">
                    <label for="rating" class="form-label"><strong>Rate this song:</strong></label>
                    <select id="rating" class="form-select" v-model="userRating" @change="rateSong">
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                    </select>
                    <span v-if="message" class="message text-danger">{{ message }}</span>
                  </div>
                </div>
                <div class="col">
                  <div class="rating-info p-2 rounded ">
                    <p class="mb-0"><strong>Average Rating: {{ averageRating }}/5.00</strong></p>
                    
                  </div>
                </div>
              </div>
            </div>
            <p v-else class="mb-0 mt-4"><strong>Please log in to rate this song. </strong><router-link to="/login"
                        class="btn btn-outline-primary btn-sm">Login</router-link></p>
          </div>
        </div>
        <div class="audio-player text-center mt-4">
          <audio controls ref="audioPlayer" class="w-50">
            Your browser does not support the audio element.
          </audio>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from '@/components/Home/NavBar.vue';
import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';

export default {
  name: "PlaySong",
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
          this.playSong(response.data.file_path);
          this.fetchRating();
        })
        .catch((error) => {
          console.error("Error fetching song:", error);
        });
    },
    playSong(filePath) {
      const audioPlayer = this.$refs.audioPlayer;
      audioPlayer.src = filePath;
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
.song-details {
  max-width: 800px;
  margin: 0 auto;
}

.rating-section {
  margin-top: 20px;
}

.message {
  font-size: 14px;
  margin-top: 5px;
}
</style>
