<template>

<div class="layout">
  <NavBarComponent :is_authenticated="is_auntificated" @logout="Logout" ></NavBarComponent>
      <main class="layout-content">
        <router-view :error="errorInLogin"  @login="Login"/>
      </main>
  </div>

</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useCookie } from  'vue-cookie-next';
import axios from 'axios';
import NavBarComponent from "./components/NavBarComponent.vue";
import router from "./router";

export default defineComponent({
  components: {
    NavBarComponent
    },

    mounted(){
        axios.defaults.baseURL = `http://localhost:8000/`
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.withCredentials = true;    
    }, 

    setup() {
        const cookie = useCookie()

        let token = ref(cookie.getCookie("token"))
        let is_auntificated = ref(false);
        const errorInLogin = ref<null | string>(null)


        if (token.value == null) {
            is_auntificated.value = false
        } else {
            is_auntificated.value = true
        }
        

        async function Logout(){
          const token = cookie.getCookie("token")
        
          try{
            const response = await axios.post('api/auth/token/logout/', {}, 
              { 
                headers: {
                   'Authorization': 'Token ' + token
                  }
              }
            )

            if (response.status == 204){
              cookie.removeCookie("token")
              router.push({name: 'mainPage'})
            }
          }
          catch (error) {
            console.log(error)
            return 
          }
            is_auntificated.value = false
        }
    
        async function Login(email: string, password: string){
          errorInLogin.value = null
          if (email == '' || password == ''){
            errorInLogin.value = "Login or password is empty"
            return
          }

          try{
            const response = await axios.post('api/auth/token/login/', {
              email: email,
              password: password 
            })

            if (response.status == 200){
              cookie.setCookie("token", response.data.auth_token)
              is_auntificated.value = true
              router.push({name: 'account'})
            }
          }
          catch (error : any) {
            console.log(error)
            errorInLogin.value =error.response.data.non_field_errors[0] 
            return 
          }
        }

        return {Logout, Login,  errorInLogin, is_auntificated}
    }
});
</script>

<style>

</style>
