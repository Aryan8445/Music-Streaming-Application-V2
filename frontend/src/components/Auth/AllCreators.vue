<template>
  <div>
    <NavBar/>
    <ErrorSuccessMessage/>
  </div>
  <div class="container mt-4">
    <h2 class="text-center text-warning">All Creators</h2>
    <div v-if="creators">
      <table class="table table-striped table-hover shadow">
        <!-- Table header -->
        <thead class="table-dark">
          <tr>
            <th scope="col">S.No</th>
            <th scope="col">First Name</th>
            <th scope="col">Last Name</th>
            <th scope="col">Email</th>
            <th scope="col">Blacklisted</th>
            <th scope="col" class="text-center">Actions</th>
          </tr>
        </thead>
        <!-- Table body -->
        <tbody>
          <!-- Loop through all creators and display each creator -->
          <tr v-for="(creator, index) in creators" :key="creator.id">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ creator.firstname }}</td>
            <td>{{ creator.lastname }}</td>
            <td>{{ creator.email }}</td>
            <td>{{ creator.is_blacklisted ? 'Yes' : 'No' }}</td>
            <!-- Buttons for actions -->
            <td class="text-end">
              <!-- Blacklist button -->
              <button v-if="!creator.is_blacklisted" class="btn btn-outline-danger btn-sm mx-2" @click="blacklistCreator(creator.id)">Blacklist</button>
              <!-- Whitelist button -->
              <button v-else class="btn btn-outline-success btn-sm mx-2" @click="whitelistCreator(creator.id)">Whitelist</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>Loading...</p>
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
      creators: null,
    };
  },
  mounted() {
    this.fetchCreators();
  },
  methods: {
    fetchCreators() {
      const accessToken = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/creators`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        this.creators = response.data.creators;
      })
      .catch(error => {
        console.error('Error fetching creators:', error);
        this.$store.dispatch('displayErrorMessage', 'Error fetching creators');
      });
    },
    blacklistCreator(creatorId) {
      const accessToken = localStorage.getItem('access_token');
      axios.post(`http://127.0.0.1:5000/api/users/${creatorId}/blacklist`, {}, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        this.creators = this.creators.map(creator => {
          if (creator.id === creatorId) {
            creator.is_blacklisted = true;
          }
          return creator;
        });
        console.log('Creator blacklisted successfully:', response.data);
        this.$store.dispatch('displaySuccessMessage', 'Creator blacklisted successfully');
      })
      .catch(error => {
        console.error('Error blacklisting creator:', error);
        this.$store.dispatch('displayErrorMessage', 'Error blacklisting creator');
      });
    },
    whitelistCreator(creatorId) {
      const accessToken = localStorage.getItem('access_token');
      axios.delete(`http://127.0.0.1:5000/api/users/${creatorId}/blacklist`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then(response => {
        this.creators = this.creators.map(creator => {
          if (creator.id === creatorId) {
            creator.is_blacklisted = false;
          }
          return creator;
        });
        console.log('Creator whitelisted successfully:', response.data);
        this.$store.dispatch('displaySuccessMessage', 'Creator whitelisted successfully');
      })
      .catch(error => {
        console.error('Error whitelisting creator:', error);
        this.$store.dispatch('displayErrorMessage', 'Error whitelisting creator');
      });
    },
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>
