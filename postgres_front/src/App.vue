<template>

<div class="layout">
  <NavBarComponent :is_authenticated="is_auntificated" @logout="Logout" @login="ToLoginPage"></NavBarComponent>
      <main class="layout-content">
        <router-view  @login="Login"/>
      </main>
  </div>

</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useCookie } from  'vue-cookie-next'
import NavBarComponent from "./components/NavBarComponent.vue";
import router from "./router";

export default defineComponent({
  components: {
    NavBarComponent
    },

    setup() {
        const cookie = useCookie()

        const token = ref(cookie.getCookie("token"))
        let is_auntificated = ref(false);
        if (token.value == null) {
            is_auntificated.value = false
        } else {
            is_auntificated.value = true
        }

        function Logout(){
            cookie.removeCookie("token")
            router.push({name: 'mainPage'})
            is_auntificated.value = false
        }
        function ToLoginPage(){
          router.push({name: 'login'})
        }

        function Login(){
          router.push({name: 'account'})
          cookie.setCookie("token", 'some_token')
          is_auntificated.value = true
        }

        return {Logout, Login, ToLoginPage, is_auntificated}
    }
});
</script>

<style>

</style>
