import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    user: null,
    userType: null,
    isLoggedIn: false,
    errorMessage: '',
    successMessage: ''
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setUserType(state, userType) {
      state.userType = userType;
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
    clearErrorMessage({ commit }) {
      commit('setErrorMessage', '');
    },
    clearSuccessMessage({ commit }) {
      commit('setSuccessMessage', '');
    }
  },
  getters: {
    user: state => state.user,
    userType: state => state.userType,
    isLoggedIn: state => state.isLoggedIn,
    errorMessage: state => state.errorMessage,
    successMessage: state => state.successMessage
  }
});
