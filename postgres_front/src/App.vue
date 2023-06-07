<template>
    <div class="layout">
        <NavBarComponent :isAuthenticated="isAuntificated" @logout="Logout"></NavBarComponent>
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

        let token = ref(cookie.getCookie('utoken'))
        let isAuntificated = ref(false)
        const errorInLogin = ref<null | string>(null)

        if (token.value == null) {
            isAuntificated.value = false
        } else {
            isAuntificated.value = true
        }

        async function Logout() {
            const token = cookie.getCookie('utoken')
            cookie.removeCookie('utoken')
            isAuntificated.value = false
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
                console.log(response)

                if (response.status == 200) {
                    cookie.removeCookie('utoken')
                    cookie.setCookie('utoken', response.data.auth_token)
                    isAuntificated.value = true
                    router.push({ name: 'account' })
                }
            } catch (error: any) {
                errorInLogin.value = error.response.data.non_field_errors[0]
                return
            }
        }
        return { Logout, Login, errorInLogin, isAuntificated }
    }
})
</script>

<style></style>
