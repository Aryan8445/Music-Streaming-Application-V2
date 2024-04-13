<template>
  <div>
    <NavBar/>
    <ErrorSuccessMessage/>
  </div>
  <div class="container mt-4">
    <div class="row">
      <div class="col">
        <h2 class="text-primary">Welcome, Admin!</h2>
      </div>
      <div class="col text-end">
        <router-link to="/all-songs" class="btn btn-info mx-2">All Songs</router-link>
        <router-link to="/all-users" class="btn btn-success mx-2">All Users</router-link>
        <router-link to="/all-creators" class="btn btn-warning mx-2">All Creators</router-link>
      </div>
    </div>

    <br>

    <div class="row justify-content-center">
      <div class="col-md-4 mb-4" v-if="adminDashboardData">
        <div class="card bg-light rounded shadow">
          <div class="card-body text-center">
            <h5 class="card-title text-primary">Normal Users</h5>
            <h3 class="card-text">{{ adminDashboardData.total_normal_user }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-4" v-if="adminDashboardData">
        <div class="card bg-light rounded shadow">
          <div class="card-body text-center">
            <h5 class="card-title text-warning">Creators</h5>
            <h3 class="card-text">{{ adminDashboardData.total_creators }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-4" v-if="adminDashboardData">
        <div class="card bg-light rounded shadow">
          <div class="card-body text-center">
            <h5 class="card-title text-danger">Total Songs</h5>
            <h3 class="card-text">{{ adminDashboardData.total_songs }}</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="row justify-content-center">
      <div class="col-md-4 mb-4" v-if="adminDashboardData">
        <div class="card bg-light rounded shadow">
          <div class="card-body text-center">
            <h5 class="card-title text-success">Total Albums</h5>
            <h3 class="card-text">{{ adminDashboardData.total_albums }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-4" v-if="adminDashboardData">
        <div class="card bg-light rounded shadow">
          <div class="card-body text-center">
            <h5 class="card-title text-info">Total Genres</h5>
            <h3 class="card-text">{{ adminDashboardData.total_genres }}</h3>
          </div>
        </div>
      </div>
    </div>

    <br>

    <div class="container mt-4">
    <h2 class="text-center text-warning">Top Rated Songs</h2>
    <br>
    <div v-if="adminDashboardData">
        <table class="table table-striped table-hover">
            <!-- Table header -->
            <thead class="table-dark">
                <tr>
                    <th scope="col">S.No</th>
                    <th scope="col">Song Name</th>
                    <th scope="col">Genre</th>
                    <th scope="col text-center">Actions</th> <!-- Added new column for actions -->
                </tr>
            </thead>
            <!-- Table body -->
            <tbody>
                <!-- Loop through top rated songs and display each song -->
                <tr v-for="(song, index) in adminDashboardData.top_rated_songs" :key="song.id">
                    <th scope="row">{{ index + 1 }}</th>
                    <td>
                        <!-- Song title -->
                        <h5>{{ song.title }}</h5>
                        By <i>{{ song.artist }}</i>
                    </td>
                    <td>
                        <!-- Genre -->
                        <em>{{ song.genre }}</em>
                    </td>
                    <!-- Buttons for actions -->
                    <td class="text-end">
                      <button class="btn btn-outline-danger btn-sm mx-2" @click="deleteSong(song.id)">Delete Song</button> <!-- Added delete button -->
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div v-else>
        <p>Loading...</p>
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
      adminDashboardData: null
    };
  },
  mounted() {
    this.fetchAdminDashboardData();
  },
  methods: {
    fetchAdminDashboardData() {
      // Fetch access token from localStorage or your preferred storage method
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        console.error('Access token not found');
        return;
      }

      axios.get(`http://127.0.0.1:5000/api/admin-dashboard`, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      })
        .then(response => {
          this.adminDashboardData = response.data;
        })
        .catch(error => console.error('Error fetching admin dashboard data:', error));
    },
    deleteSong(songId) {
      const accessToken = localStorage.getItem('access_token');
      axios.delete(`http://127.0.0.1:5000/api/songs/${songId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      })
        .then(response => {
          // Refresh songs after deletion
          this.fetchAdminDashboardData();
          console.log('Song deleted successfully:', response.data);
          this.$store.dispatch('displaySuccessMessage', 'Song deleted successfully');
        })
        .catch(error => {
          console.error('Error deleting song:', error);
          this.$store.dispatch('displayErrorMessage', 'Error deleting song');
        });
    },
  }
};
</script>

<style scoped>
.rounded-div {
    border-radius: 15px;
    padding: 20px;
    background-color: #f0f0f0;
    margin: 20px;
  }
  .btn {
  border-radius: 20px;
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
