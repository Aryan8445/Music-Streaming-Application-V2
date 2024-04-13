<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <form @submit.prevent="updateSong" class="update-song-form p-4 border rounded bg-light shadow">
            <h3 class="text-center mb-4">Update Song Details</h3>

            <!-- Title Input -->
            <div class="mb-3">
              <label for="title" class="form-label">Title</label>
              <input type="text" class="form-control" v-model="title" id="title" :placeholder="currentSong.title" required>
            </div>

            <!-- Release Date Input -->
            <div class="mb-3">
              <label for="release_date" class="form-label">Release Date</label>
              <input type="date" class="form-control" v-model="releaseDate" id="release_date" :placeholder="currentSong.release_date" required>
            </div>

            <!-- Genre Input -->
            <div class="mb-3">
              <label for="genre" class="form-label">Genre</label>
              <input type="text" class="form-control" v-model="genre" id="genre" :placeholder="currentSong.genre" required>
            </div>

            <!-- Lyrics Input -->
            <div class="mb-3">
              <label for="lyrics" class="form-label">Lyrics</label>
              <textarea class="form-control" v-model="lyrics" id="lyrics" rows="4" :placeholder="currentSong.lyrics"></textarea>
            </div>

            <!-- Update Button -->
            <div class="d-grid gap-2 col-6 mx-auto">
              <button type="submit" class="btn btn-primary">Update</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from '@/components/Home/NavBar.vue';
import ErrorSuccessMessage from '../Auth/ErrorSuccessMessage.vue';

export default {
  name: 'UpdateSong',
  data() {
    return {
      title: '',
      releaseDate: '',
      genre: '',
      lyrics: '',
      currentSong: {}, // Holds the details of the current song
    };
  },
  components:{
    NavBar
  },
  mounted() {
    // Fetch the current song details when the component is mounted
    this.fetchCurrentSong();
  },
  methods: {
    async fetchCurrentSong() {
      try {
        const songId = this.$route.params.id;
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.get(`http://127.0.0.1:5000/api/songs/${songId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });
        this.currentSong = response.data;
        // Set default values for form fields
        this.title = this.currentSong.title;
        this.releaseDate = this.currentSong.release_date;
        this.genre = this.currentSong.genre;
        this.lyrics = this.currentSong.lyrics;

      } catch (error) {
        console.error('Failed to fetch song details:', error.message);

      }
    },
    async updateSong() {
      try {
        const songId = this.$route.params.id;
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.put(`http://127.0.0.1:5000/api/songs/${songId}`, {
          title: this.title,
          release_date: this.releaseDate,
          genre: this.genre,
          lyrics: this.lyrics
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });

        // Handle success response
        console.log('Song updated successfully:', response.data);
        this.$router.push('/creator-dashboard')
        this.$store.dispatch('displaySuccessMessage', 'Song updated successfully');
        // Redirect or display success message as needed
      } catch (error) {
        console.error('Failed to update song:', error.message);
        this.$store.dispatch('displayErrorMessage', 'Error updating song');
      }
    }
  }
};
</script>

<style scoped>
.update-song-form {
  max-width: 400px;
  margin: 0 auto;
}

.update-song-form .form-label {
  font-weight: bold;
}

.update-song-form .btn-primary {
  width: 100%;
}
</style>
