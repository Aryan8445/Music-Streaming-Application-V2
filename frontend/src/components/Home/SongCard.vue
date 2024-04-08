<template>
  <div class="col mb-4"> <!-- Adjust the column width -->
    <div class="card h-100 shadow-sm song-card">
      <img :src="song.imageUrl || require('@/assets/img/music.jpg')" class="card-img-top song-image" alt="Song Image">
      <div class="card-body">
        <h5 class="card-title text-center text-dark">{{ song.title }}</h5>
        <p class="card-text text-center text-muted">Artist: {{ song.artist }}</p>
        <p class="card-text text-center text-muted">Genre: {{ song.genre }}</p>
        <div class="d-flex justify-content-between">
          <router-link :to="'/play/' + song.id" class="btn btn-outline-success btn-sm">Play Song</router-link>
          <router-link :to="'/lyrics/' + song.id" class="btn btn-outline-info btn-sm">Read Lyrics</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SongCard',
  props: {
    song: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.card {
  border: none;
  border-radius: 10px;
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}

.song-card {
  background-color: #f8f9fa; /* Light gray background */
  position: relative;
  width: 250px; /* Adjust the card width */
}

.song-image {
  height: 100px; /* Adjust the card image height */
  object-fit: cover;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
}

.card-text {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.btn {
  border-radius: 20px;
  width: 100px; /* Adjust the button width */
}

.btn-outline-success {
  color: #28a745; /* Green color */
  border-color: #28a745;
}

.btn-outline-success:hover {
  background-color: #28a745;
  color: #fff; /* White text on hover */
}

.btn-outline-info {
  color: #17a2b8; /* Blue color */
  border-color: #17a2b8;
}

.btn-outline-info:hover {
  background-color: #17a2b8;
  color: #fff; /* White text on hover */
}
</style>
