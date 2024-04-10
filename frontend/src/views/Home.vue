<template>
  <div>
    <NavBar />
    <ErrorSuccessMessage />

    <div class="container mt-4">
      <h2 class="d-flex justify-content-between align-items-center">Trending Songs
        <div class="pagination">
          <button class="btn btn-icon mr-2" @click="previousPage" :disabled="currentPage === 1"
            v-if="currentPage !== 1">
            <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/left-squared.png"
              alt="left-squared" />
          </button>
          <button class="btn btn-icon" @click="nextPage" :disabled="currentPage * pageSize >= totalSongs"
            v-if="currentPage * pageSize < totalSongs">
            <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/right-squared.png"
              alt="right-squared" />
          </button>
        </div>
      </h2>
      <div class="row">
        <SongCard v-for="song in displayedSongs" :key="song.id" :song="song" />
      </div>
      <hr>
      <h2 class="mt-4 d-flex justify-content-between align-items-center">Trending Albums
        <div class="pagination">
          <button class="btn btn-icon mr-2" @click="previousPageAlbums" :disabled="currentPageAlbums === 1"
            v-if="currentPageAlbums !== 1">
            <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/left-squared.png"
              alt="left-squared" />
          </button>
          <button class="btn btn-icon" @click="nextPageAlbums"
            :disabled="currentPageAlbums * pageSizeAlbums >= totalAlbums"
            v-if="currentPageAlbums * pageSizeAlbums < totalAlbums">
            <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/right-squared.png"
              alt="right-squared" />
          </button>
        </div>
      </h2>
      <div class="row">
        <AlbumCard v-for="album in displayedAlbums" :key="album.id" :album="album" />
      </div>
      <hr>
      <!-- Playlist section -->
      <div v-if="isLoggedIn() && playlists.length > 0">

        <h2 class="mt-4 d-flex justify-content-between align-items-center">Your Playlists
          <span><router-link to="/create-playlist" style="border-radius: 20px; width: 120px;"
              class="btn btn-outline-info btn-sm">Create Playlist</router-link></span>

          <div class="pagination">
            <button class="btn btn-icon mr-2" @click="previousPagePlaylists" :disabled="currentPagePlaylists === 1"
              v-if="currentPagePlaylists !== 1">
              <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/left-squared.png"
                alt="left-squared" />
            </button>
            <button class="btn btn-icon" @click="nextPagePlaylists"
              :disabled="currentPagePlaylists * pageSizePlaylists >= totalPlaylists"
              v-if="currentPagePlaylists * pageSizePlaylists < totalPlaylists">
              <img width="100" height="100" src="https://img.icons8.com/carbon-copy/100/000000/right-squared.png"
                alt="right-squared" />
            </button>
          </div>
        </h2>
        <div class="row">
          <PlaylistCard v-for="playlist in displayedPlaylists" :key="playlist.id" :playlist="playlist" />
        </div>
      </div>
      <div v-else-if="isLoggedIn()">
        <div class="container mt-4">
          <div class="alert alert-secondary rounded-lg shadow-sm text-center" role="alert">
            <div>
              <h3>No playlists available.</h3>
            </div><br>
            <router-link to="/create-playlist" style="border-radius: 20px; width: 120px;"
              class="btn btn-outline-info btn-sm">Create Playlist</router-link>
          </div>
        </div>
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
import PlaylistCard from '@/components/Home/PlaylistCard.vue';

export default {
  name: 'Home',
  components: {
    NavBar,
    ErrorSuccessMessage,
    SongCard,
    AlbumCard,
    PlaylistCard
  },
  data() {
    return {
      songs: [],
      albums: [],
      playlists: [],
      currentPage: 1,
      currentPageAlbums: 1,
      currentPagePlaylists: 1,
      pageSize: 8,
      pageSizeAlbums: 4,
      pageSizePlaylists: 4,
      totalSongs: 0,
      totalAlbums: 0,
      totalPlaylists: 0
    };
  },
  computed: {
    displayedSongs() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.songs.slice().reverse().slice(startIndex, endIndex);
    },
    displayedAlbums() {
      const startIndex = (this.currentPageAlbums - 1) * this.pageSizeAlbums;
      const endIndex = startIndex + this.pageSizeAlbums;
      return this.albums.slice().reverse().slice(startIndex, endIndex);
    },
    displayedPlaylists() {
      const startIndex = (this.currentPagePlaylists - 1) * this.pageSizePlaylists;
      const endIndex = startIndex + this.pageSizePlaylists;
      return this.playlists.slice().reverse().slice(startIndex, endIndex);
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    isLoggedIn() {
      const accessToken = localStorage.getItem('access_token');
      return !!accessToken;
    },
    async fetchData() {
      try {
        const [songsResponse, albumsResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/songs'),
          axios.get('http://127.0.0.1:5000/api/albums')
        ]);
        this.songs = songsResponse.data;
        this.albums = albumsResponse.data;
        this.totalSongs = this.songs.length;
        this.totalAlbums = this.albums.length;

        const accessToken = localStorage.getItem('access_token');
        if (accessToken) {
          const playlistsResponse = await axios.get('http://127.0.0.1:5000/api/playlists', {
            headers: {
              Authorization: `Bearer ${accessToken}`
            }
          });
          this.playlists = playlistsResponse.data;
          this.totalPlaylists = this.playlists.length;
        } else {
          console.log('Access token not found.');
        }
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
    },
    nextPagePlaylists() {
      if (this.currentPagePlaylists * this.pageSizePlaylists < this.totalPlaylists) {
        this.currentPagePlaylists++;
      }
    },
    previousPagePlaylists() {
      if (this.currentPagePlaylists > 1) {
        this.currentPagePlaylists--;
      }
    },
    createPlaylist() {
      // Logic to create a new playlist
    }
  }
};
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

/* Styles for the no playlists available section */
.text-center {
  margin-top: 20px;
}

.btn-lg {
  padding: 10px 20px;
  font-size: 1.25rem;
}


.btn-outline-info {
  color: #a817b8;
  border-color: #a817b8;
}

.btn-outline-info:hover {
  background-color: #a817b8;
  color: #fff;
}
</style>
