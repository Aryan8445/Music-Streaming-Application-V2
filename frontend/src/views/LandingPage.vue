<template>
  <div>
    <div class="landing-container">
      <div class="container text-center">
        <h1 class="display-3">Welcome to the Music Streaming App</h1>
      </div>
      
      <div class="container mt-4">
        <div class="row justify-content-center">
          <div class="col-md-6">
            <div class="p-4 border rounded bg-light shadow">
              <h3 class="text-center mb-4">Get Started</h3>
              <hr>
              <div class="row justify-content-center text-center">
                <div class="col-md-4">
                  <router-link to="/login" class="btn btn-primary btn-lg" role="button">Login</router-link>
                </div>
                <div class="col-md-4">
                  <router-link to="/sign_up" class="btn btn-success btn-lg" role="button">Sign Up</router-link>
                </div>
                <div class="col-md-4">
                  <router-link to="/admin_login" class="btn btn-secondary btn-lg" role="button">Admin</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    /* eslint-disable */
  // Component logic goes here
  name: 'LandingPage'
};
</script>

<style>
/* Landing page container */
.landing-container {
  background-color: #f8f9fa;
  padding-top: 100px;
  padding-bottom: 100px;
}

/* Button styling */
.btn {
  width: 100%;
  margin-top: 10px;
}

/* Add your custom styles here */
</style>
