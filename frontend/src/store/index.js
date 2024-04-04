import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    user: null,
    isLoggedIn: false,
    errorMessage: '',
    successMessage: ''
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setLoggedIn(state, isLoggedIn) {
      state.isLoggedIn = isLoggedIn;
    },
    setErrorMessage(state, message) {
      state.errorMessage = message;
    },
    setSuccessMessage(state, message) {
      state.successMessage = message;
    }
  },
  actions: {
    async logout({ commit }) {
      try {
        // Perform logout logic here
        localStorage.removeItem('access_token'); // Remove access token from local storage
        commit('setUser', null); // Set user to null
        commit('setLoggedIn', false); // Set isLoggedIn to false
      } catch (error) {
        console.error('Logout failed:', error);
        // Handle error
      }
    },
    async checkLoggedIn({ commit }) {
      const access_token = localStorage.getItem('access_token');
      if (access_token) {
        try {
          // Perform check logged in logic here
          // Assuming you fetch user data from an endpoint and set it to the state
          const response = await axios.get('http://127.0.0.1:5000/user');
          const user = response.data; // Assuming the response contains user data
          commit('setUser', user);
          commit('setLoggedIn', true);
        } catch (error) {
          console.error('User not authenticated:', error);
          // Handle error
        }
      } else {
        // If no access token found, set isLoggedIn to false
        commit('setLoggedIn', false);
      }
    },
    clearErrorMessage({ commit }) {
      commit('setErrorMessage', '');
    },
    clearSuccessMessage({ commit }) {
      commit('setSuccessMessage', '');
    }
  },
  getters: {
    user: state => state.user,
    isLoggedIn: state => state.isLoggedIn,
    errorMessage: state => state.errorMessage,
    successMessage: state => state.successMessage
  }
});
