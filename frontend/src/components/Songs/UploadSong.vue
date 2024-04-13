<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />

    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="p-4 upload-song-form border rounded bg-light shadow">
            <h3 class="text-center mb-4">Upload a New Song</h3>

            <div class="mb-3">
              <label for="title" class="form-label h5">Title:</label>
              <input type="text" class="form-control" v-model="title" placeholder="Enter Song Title" required>
            </div>
            <div class="mb-3">
              <label for="release_date" class="form-label h5">Release Date:</label>
              <input type="date" class="form-control" v-model="releaseDate" placeholder="Enter Release Date" required>
            </div>
            <div class="mb-3">
              <label for="genre" class="form-label h5">Genre:</label>
              <input type="text" class="form-control" v-model="genre" placeholder="Enter Genre" required>
            </div>
            <div class="mb-3">
              <label for="lyrics" class="form-label h5">Lyrics:</label>
              <input type="text" class="form-control" v-model="lyrics" placeholder="Enter Lyrics">
            </div>
            <div class="mb-3">
              <label for="song_file" class="form-label h5">Upload Song File (MP3, WAV, etc.):</label>
              <input type="file" class="form-control" id="song_file" @change="handleFileUpload" accept=".mp3, .wav"
                required>
            </div>

            <div class="d-grid gap-2 col-6 mx-auto">
              <button type="button" class="btn btn-success" @click="uploadSong">Upload Song</button>
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
      title: '',
      releaseDate: '',
      genre: '',
      lyrics: '',
      songFile: null,
    };
  },
  methods: {
    ...mapActions(['displaySuccessMessage', 'displayErrorMessage', 'clearMessages']),
    async uploadSong() {
      try {
        const formData = new FormData();
        formData.append('title', this.title);
        formData.append('release_date', this.releaseDate);
        formData.append('genre', this.genre);
        formData.append('lyrics', this.lyrics);
        formData.append('song_file', this.songFile);

        const response = await axios.post('http://127.0.0.1:5000/api/songs/upload', formData, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        await this.fetchUserDetails();



        this.$router.push('/');

        this.displaySuccessMessage('Song uploaded successfully');
      } catch (error) {

        this.displayErrorMessage('Error uploading song: ' + error.response.data.message);
      }
    },
    async fetchUserDetails() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/user', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        const userDetails = response.data;
        localStorage.setItem('user_type', userDetails.user_type);
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    },
    handleFileUpload(event) {
      this.songFile = event.target.files[0];
    },
  },
  created() {

    this.fetchUserDetails();
  },
};
</script>

<style scoped>
.upload-song-form {
  max-width: 400px;
  margin: 0 auto;
}
</style>
