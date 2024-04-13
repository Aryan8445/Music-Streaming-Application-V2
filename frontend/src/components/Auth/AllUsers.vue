<template>
    <div>
      <NavBar/>
      <ErrorSuccessMessage/>
    </div>
    <div class="container mt-4">
      <h2 class="text-center text-warning">All Users</h2>
      <div v-if="users">
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
            <!-- Loop through all users and display each user -->
            <tr v-for="(user, index) in users" :key="user.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ user.firstname }}</td>
              <td>{{ user.lastname }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.is_blacklisted ? 'Yes' : 'No' }}</td>
              <!-- Buttons for actions -->
              <td class="text-end">
                <!-- Blacklist button -->
                <button v-if="!user.is_blacklisted" class="btn btn-outline-danger btn-sm mx-2" @click="blacklistUser(user.id)">Blacklist</button>
                <!-- Whitelist button -->
                <button v-else class="btn btn-outline-success btn-sm mx-2" @click="whitelistUser(user.id)">Whitelist</button>
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
        users: null,
      };
    },
    mounted() {
      this.fetchUsers();
    },
    methods: {
      fetchUsers() {
        const accessToken = localStorage.getItem('access_token');
        axios.get(`http://127.0.0.1:5000/api/users`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then(response => {
          this.users = response.data.users;
        })
        .catch(error => {
          console.error('Error fetching users:', error);
          this.$store.dispatch('displayErrorMessage', 'Error fetching users');
        });
      },
      blacklistUser(userId) {
        const accessToken = localStorage.getItem('access_token');
        axios.post(`http://127.0.0.1:5000/api/users/${userId}/blacklist`, {}, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then(response => {
          this.users = this.users.map(user => {
            if (user.id === userId) {
              user.is_blacklisted = true;
            }
            return user;
          });
          console.log('User blacklisted successfully:', response.data);
          this.$store.dispatch('displaySuccessMessage', 'User blacklisted successfully');
        })
        .catch(error => {
          console.error('Error blacklisting user:', error);
          this.$store.dispatch('displayErrorMessage', 'Error blacklisting user');
        });
      },
      whitelistUser(userId) {
        const accessToken = localStorage.getItem('access_token');
        axios.delete(`http://127.0.0.1:5000/api/users/${userId}/blacklist`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then(response => {
          this.users = this.users.map(user => {
            if (user.id === userId) {
              user.is_blacklisted = false;
            }
            return user;
          });
          console.log('User whitelisted successfully:', response.data);
          this.$store.dispatch('displaySuccessMessage', 'User whitelisted successfully');
        })
        .catch(error => {
          console.error('Error whitelisting user:', error);
          this.$store.dispatch('displayErrorMessage', 'Error whitelisting user');
        });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add custom styles if needed */
  </style>
  