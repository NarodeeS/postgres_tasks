<template>
    <!-- Login Section -->
    <div class="container">
        <div class="form-container">
            <h2>  Login to Your Account</h2>
              <form>
                <div class="form-group">
                  <label for="email">Email</label>
                  <input
                   type="text"
                    id="email" name="email" v-model="email" required>
                </div>
                <div class="form-group">
                  <label for="password">Password</label>
                  <input type="password" id="password" name="password" v-model="password" required>
                </div>
                  <div class="form-group">
                      <div class="custom-control custom-checkbox">
                          <input type="checkbox" class="custom-control-input" id="remember">
                          <!-- <label class="custom-control-label" for="remember">Remember me</label> -->
                      </div>
                  </div>
                  <div v-if="error !== null" class="alert alert-danger alert-dismissible fade show" role="alert">
              <strong>Error:</strong> {{error}}
          </div>
                  <input type="submit" @click="Login" value="Login">

                  <div class="forgot-password">
                                <a href="#" @click="ToLoginPage">Have no accout?</a>
                            </div>  
              </form>
          </div>
      </div>

</template>

<script lang="ts">
import { defineComponent, ref, PropType} from 'vue'
import router from '../router'

export default defineComponent({
  emits:{
      login: (email: string, password: string) => true
  },
  props: {
    error: {
      type:  null as unknown as PropType<string | null>,
      required: true
    }
  },
  setup(_, { emit }) {
      const email = ref('')
      const password  = ref('')

      function ToLoginPage() {
        router.push({name: 'registration'})
    }      
      
      function Login() {
        if (email.value === '' || password.value === '') {
          return
        }
       emit('login', email.value, password.value)

        password.value = ''
      }
      return {Login, ToLoginPage,  email, password}
  },
})
</script>

<style>

.forgot-password {
            text-align: right;
            font-size: 14px;
            margin-top: 10px;
        }

.forgot-password a {
    color: #1abc9c;
    font-weight: bold;
}

.forgot-password a:hover {
        text-decoration: none;
        color: #148f77;
    }
 
</style>
