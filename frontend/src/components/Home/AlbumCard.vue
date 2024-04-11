<template>
  <div class="col mb-4"> <!-- Adjust the column width -->
    <div class="card h-100 shadow-sm album-card">
      <img :src="album.imageUrl || require('@/assets/img/album.jpg')" class="card-img-top album-image" alt="Album Image">
      <div class="card-body">
        <h5 class="card-title text-center text-dark">{{ album.title }}</h5>
        <p class="card-text text-center text-muted">Artist: {{ album.artist }}</p>
        <div class="d-flex justify-content-center">
          <router-link :to="'/album-songs/' + album.id" class="btn btn-outline-info btn-sm">View Album</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlbumCard',
  props: {
    album: {
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

.album-card {
  background-color: #f8f9fa; /* Light gray background */
  position: relative;
  width: 250px; /* Adjust the card width */
}

.album-image {
  height: 200px; /* Adjust the album image height */
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
  width: 120px; /* Adjust the button width */
}

.btn-outline-info {
  color: #17a2b8;
  border-color: #17a2b8;
}

.btn-outline-info:hover {
  background-color: #17a2b8;
  color: #fff;
}
</style>
