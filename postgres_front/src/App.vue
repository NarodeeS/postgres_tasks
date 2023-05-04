<template>
    <div class="layout">
        <NavBarComponent :is_authenticated="is_auntificated" @logout="Logout"></NavBarComponent>
        <main class="layout-content">
            <router-view :error="errorInLogin" @login="Login" />
        </main>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useCookie } from 'vue-cookie-next'
import axios from 'axios'
import NavBarComponent from './components/NavBarComponent.vue'
import router from './router'

export default defineComponent({
    components: {
        NavBarComponent
    },

    mounted() {
        if (typeof process.env.VUE_APP_ROOT_DNS === 'undefined') {
            axios.defaults.baseURL = `http://${process.env.VUE_APP_ROOT_API}:${process.env.VUE_APP_ROOT_API_PORT}/`
        } else {
            axios.defaults.baseURL = `http://${process.env.VUE_APP_ROOT_DNS}/`
        }
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.withCredentials = true
    },

    setup() {
        const cookie = useCookie()

        let token = ref(cookie.getCookie('token'))
        let is_auntificated = ref(false)
        const errorInLogin = ref<null | string>(null)

        if (token.value == null) {
            is_auntificated.value = false
        } else {
            is_auntificated.value = true
        }

        async function Logout() {
            const token = cookie.getCookie('token')
            cookie.removeCookie('token')
            is_auntificated.value = false
            router.push({ name: 'mainPage' })
            try {
                await axios.post(
                    'api/auth/token/logout/',
                    {},
                    {
                        headers: {
                            Authorization: 'Token ' + token
                        }
                    }
                )
            } catch (error) {
                return
            }
        }

        async function Login(email: string, password: string) {
            errorInLogin.value = null
            try {
                const response = await axios.post('api/auth/token/login/', {
                    email: email,
                    password: password
                })

                if (response.status == 200) {
                    cookie.setCookie('token', response.data.auth_token)
                    is_auntificated.value = true
                    router.push({ name: 'account' })
                }
            } catch (error: any) {
                errorInLogin.value = error.response.data.non_field_errors[0]
                return
            }
        }
        return { Logout, Login, errorInLogin, is_auntificated }
    }
})
</script>

<style></style>
