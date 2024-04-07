import { createStore } from 'vuex';

export default createStore({
  state: {
    errorMessage: '',
    successMessage: ''
  },
  mutations: {
    setErrorMessage(state, message) {
      state.errorMessage = message;
    },
    setSuccessMessage(state, message) {
      state.successMessage = message;
    },
    clearMessages(state) {
      state.errorMessage = '';
      state.successMessage = '';
    }
  },
  actions: {
    displayErrorMessage({ commit }, message) {
      commit('setErrorMessage', message);
    },
    displaySuccessMessage({ commit }, message) {
      commit('setSuccessMessage', message);
    },
    clearMessages({ commit }) {
      commit('clearMessages');
    }
  },
  getters: {
    errorMessage: state => state.errorMessage,
    successMessage: state => state.successMessage
  }
});
