<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage /> 

    <div class="container mt-4">
      <h2 class="d-flex justify-content-between align-items-center">Trending Songs
        <div class="pagination">
          <button class="btn btn-icon mr-2" @click="previousPage" :disabled="currentPage === 1" v-if="currentPage !== 1">
            <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/left-squared.png" alt="left-squared"/>
          </button>
          <button class="btn btn-icon" @click="nextPage" :disabled="currentPage * pageSize >= totalSongs" v-if="currentPage * pageSize < totalSongs">
            <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/right-squared.png" alt="right-squared"/>
          </button>
        </div>
      </h2>
      <div class="row">
        <SongCard
          v-for="song in displayedSongs"
          :key="song.id"
          :song="song"
        />
      </div>
<hr>
      <h2 class="mt-4 d-flex justify-content-between align-items-center">Trending Albums
        <div class="pagination">
          <button class="btn btn-icon mr-2" @click="previousPageAlbums" :disabled="currentPageAlbums === 1" v-if="currentPageAlbums !== 1">
            <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/left-squared.png" alt="left-squared"/>
          </button>
          <button class="btn btn-icon" @click="nextPageAlbums" :disabled="currentPageAlbums * pageSizeAlbums >= totalAlbums" v-if="currentPageAlbums * pageSizeAlbums < totalAlbums">
            <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/right-squared.png" alt="right-squared"/>
          </button>
        </div>
      </h2>
      <div class="row">
        <AlbumCard
          v-for="album in displayedAlbums"
          :key="album.id"
          :album="album"
        />
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios';
import NavBar from '@/components/Home/NavBar.vue';
import ErrorSuccessMessage from '@/components/Auth/ErrorSuccessMessage.vue';
import SongCard from '@/components/Home/SongCard.vue';
import AlbumCard from '@/components/Home/AlbumCard.vue';

export default {
  name: 'Home',
  components: {
    NavBar,
    ErrorSuccessMessage,
    SongCard,
    AlbumCard
  },
  data() {
    return {
      songs: [],
      albums: [],
      currentPage: 1,
      currentPageAlbums: 1,
      pageSize: 8,
      pageSizeAlbums: 4
    };
  },
  computed: {
    totalSongs() {
      return this.songs.length;
    },
    totalAlbums() {
      return this.albums.length;
    },
    displayedSongs() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.songs.slice(startIndex, endIndex);
    },
    displayedAlbums() {
      const startIndex = (this.currentPageAlbums - 1) * this.pageSizeAlbums;
      const endIndex = startIndex + this.pageSizeAlbums;
      return this.albums.slice(startIndex, endIndex);
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const [songsResponse, albumsResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/songs'),
          axios.get('http://127.0.0.1:5000/api/albums')
        ]);
        this.songs = songsResponse.data;
        this.albums = albumsResponse.data;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    nextPage() {
      if (this.currentPage * this.pageSize < this.totalSongs) {
        this.currentPage++;
      }
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPageAlbums() {
      if (this.currentPageAlbums * this.pageSizeAlbums < this.totalAlbums) {
        this.currentPageAlbums++;
      }
    },
    previousPageAlbums() {
      if (this.currentPageAlbums > 1) {
        this.currentPageAlbums--;
      }
    }
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
}

.btn-icon {
  background: transparent;
  border: none;
  padding: 0;
}

.btn-icon img {
  width: 30px;
  height: 30px;
}

.btn-icon:hover img {
  filter: brightness(120%);
}

.fa-chevron-left,
.fa-chevron-right {
  font-size: 1.5rem;
}

.fa-chevron-left {
  margin-right: 10px;
}

.fa-chevron-right {
  margin-left: 10px;
}
</style>
