<template>
    <!-- Login Section -->
<section class="bg-dark text-white py-5">
  <div class="container">
    <div class="row">
      <div class="col-md-6 offset-md-3">
        <div class="card">
          <div class="card-header  text-white">
            <h4>Login to your account</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent>
              <div class="form-group">
                <label for="email">Email address</label>
                <input type="text" class="form-control" v-model="login" id="email" placeholder="Enter email">
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" v-model="password" id="password" placeholder="Password">
              </div>
              <button 
              type="submit"
                  @click="Login"
                  class="btn btn-custom-green btn-success btn-block">Login</button>
            </form>
          </div>
          <div class="card-footer bg-dark text-white">
            <p class="mb-0">Don't have an account? <a href="#" class="text-success-custom">Register here</a></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  emits:{
      login: (login: string, password: string) => true
  },
  setup(_, { emit }) {
      const login = ''
      const password = ''
      
      function Login() {
       emit('login', login, password)
      }
      return {Login, login, password}
  },
})
</script>

<style>

.card-header {
  background-color: #1abc9c;
}
.text-success-custom{
  color: #1abc9c;
}
</style>
