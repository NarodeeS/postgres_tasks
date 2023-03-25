<template>
      <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand" href="#">PostgreSQL</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link"  @click="$router.push({name: 'mainPage'})" href="#">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Documentation</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Tutorials</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Community</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">About</a>
          </li>
          <li v-if="is_authenticated == true" class="nav-item">
            <a class="nav-link" @click="Logout">Logout</a>
          </li>
          <li v-else class="nav-item">
            <a class="nav-link" @click="Login">Login</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    is_authenticated: {
      required: true,
      type: Boolean
    }
  },
  emits:{
    login: () => true,
    logout: () => true
  },
  setup(_, { emit }) {

    function Logout() {
      emit('logout')
    }
    function Login() {
      emit('login')
    }
    return {Login, Logout }
  },
})
</script>

<style >

</style>