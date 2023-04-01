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
            <a class="nav-link" href="#">About</a>
          </li>
          <li class="nav-item" v-if="is_authenticated == false" >
            <a class="nav-link" href="#" @click="$router.push({name: 'registration'})">Registration</a>
          </li>
          <li v-if="is_authenticated == true" class="nav-item">
            <a class="nav-link" @click="Logout">Logout</a>
          </li>
          <li v-if="is_authenticated == true" class="nav-item">
            <a class="nav-link" @click="$router.push({name: 'account'})">Account</a>
          </li>
          <li v-else class="nav-item">
            <a class="nav-link" @click="$router.push({name: 'login'})">Login</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
import router from '../router'

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
    return { Logout }
  },
})
</script>

<style >

</style>