<template>
  <transition name="fade">
    <div v-if="errorMessage || successMessage" class="message-container">
      <div v-if="errorMessage" class="alert alert-danger" role="alert">
        <span>{{ errorMessage }}</span>
        <button @click="clearMessages" class="close-btn">×</button>
      </div>
      <div v-if="successMessage" class="alert alert-success" role="alert">
        <span>{{ successMessage }}</span>
        <button @click="clearMessages" class="close-btn">×</button>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  computed: {
    errorMessage() {
      return this.$store.getters.errorMessage;
    },
    successMessage() {
      return this.$store.getters.successMessage;
    }
  },
  methods: {
    clearMessages() {
      this.$store.dispatch('clearMessages');
    }
  }
};
</script>

<style scoped>
.message-container {
  position: fixed;
  top: 60px; /* Adjust as needed to clear the navbar */
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
}

.alert {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 300px;
  padding: 10px 20px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.close-btn {
  cursor: pointer;
  border: none;
  background: none;
  font-size: 20px;
  color: #000;
}

.close-btn:hover {
  color: #f00;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
