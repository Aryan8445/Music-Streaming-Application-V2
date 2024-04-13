<template>
    <div>
        <NavBar />
        <ErrorSuccessMessage />
        <div class="container-fluid mt-5 text-center">
            <div class="mb-4 d-flex " style="width: 400px; margin-left: 550px;">
                <input type="text" v-model="query" class="form-control search-input" placeholder="Search..."
                    @keyup.enter="search">
                <button class="btn btn-primary search-btn" @click="search">Search</button>
            </div>
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <!-- Search bar -->


                    <!-- Songs -->
                    <div v-if="songs.length > 0">
                        <h2 class="section-title">Songs</h2>
                        <div class="song-list">
                            <div v-for="song in songs" :key="song.id" class="card mb-3">
                                <div class="card-body">
                                    <h5 class="card-title">{{ song.title }}</h5>
                                    <p class="card-text">{{ song.artist }}</p>
                                    <div class="btn-group" role="group">
                                        <router-link :to="'/play/' + song.id" class="btn btn-outline-success  mx-2">Play
                                            Song</router-link>
                                        <router-link :to="'/lyrics/' + song.id" class="btn btn-outline-info  mx-2">Read
                                            Lyrics</router-link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else>
                        <p class="no-data-message">No songs found.</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <!-- Albums -->
                    <div v-if="albums.length > 0">
                        <h2 class="section-title">Albums</h2>
                        <div class="album-list">
                            <div v-for="album in albums" :key="album.id" class="card mb-3">
                                <div class="card-body">
                                    <h5 class="card-title">{{ album.title }}</h5>
                                    <p class="card-text">{{ album.artist }}</p>
                                    <router-link :to="'/album-songs/' + album.id" class="btn btn-outline-primary">View
                                        Album</router-link>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else>
                        <p class="no-data-message">No albums found.</p>
                    </div>
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
    components: {
        NavBar,
        ErrorSuccessMessage,
    },
    data() {
        return {
            query: '',
            songs: [],
            albums: []
        };
    },
    methods: {
        async search() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/api/search', {
                    query: this.query
                });
                // Update songs and albums based on search results
                this.songs = response.data.songs;
                this.albums = response.data.albums;
            } catch (error) {
                console.error('Error searching:', error.message);
            }
        }
    }
};
</script>

<style scoped>
.search-input {
    border-radius: 20px;
}

.search-btn {
    border-radius: 20px;
}

.section-title {
    color: #333;
}

.song-list .card,
.album-list .card {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.song-list .card:hover,
.album-list .card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.no-data-message {
    font-style: italic;
    color: #666;
}
</style>