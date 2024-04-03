import { createStore } from 'vuex';

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
        commit('setUser', null);
        commit('setLoggedIn', false);
      } catch (error) {
        console.error('Logout failed:', error);
        // Handle error
      }
    },
    async checkLoggedIn({ commit }) {
      try {
        // Perform check logged in logic here
        commit('setUser', logged_in_as);
        commit('setLoggedIn', true);
      } catch (error) {
        console.error('User not authenticated:', error);
        // Handle error
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
