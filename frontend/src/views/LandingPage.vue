<template>
  <div>
    <br>
    <div class="landing-container">
      <div class="container text-center">
        <h1 class="display-3" style="color: black;">Welcome to the Music Streaming App</h1>
      </div>

      <div class="container mt-4">
        <div class="row justify-content-center">
          <div class="col-md-6">
            <div class="p-4 border rounded bg-light shadow">
              <h3 class="text-center mb-4">Get Started</h3>
              <hr>
              <div class="row justify-content-center text-center">
                <div class="col-md-4 mb-3">
                  <router-link to="/login" class="btn btn-primary btn-lg" role="button">Login</router-link>
                </div>
                <div class="col-md-4 mb-3">
                  <router-link to="/sign_up" class="btn btn-success btn-lg" role="button">Sign Up</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->

  </div>
</template>

<script>
export default {
  name: 'LandingPage',
};
</script>

<style scoped>
/* Landing page container */
.landing-container {
  height: 100vh;
  font-family: Arial, sans-serif;
}

/* Button styling */
.btn {
  width: 100%;
  margin-top: 10px;
}
</style>