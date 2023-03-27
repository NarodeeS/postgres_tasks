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
                  class="btn btn-custom-green btn-block">Login</button>
            </form>
      
          </div>

          <div v-if="error !== null" class="alert alert-danger alert-dismissible fade show" role="alert">
              <strong>Error:</strong> {{error}}
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
import { defineComponent, ref, PropType} from 'vue'

export default defineComponent({
  emits:{
      login: (login: string, password: string) => true
  },
  props: {
    error: {
      type:  null as unknown as PropType<string | null>,
      required: true
    }
  },
  setup(_, { emit }) {
      const login  = ref('')
      const password  = ref('')
      
      function Login() {
       emit('login', login.value, password.value)

        password.value = ''
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
