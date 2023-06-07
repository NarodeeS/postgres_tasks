<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">

            <div class="col-4">
                <a class="navbar-brand" href="#">PostgreSQL</a>
            </div>

            <div class="col-8 collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" @click="$router.push({ name: 'mainPage' })" href="#"
                            >Home</a
                        >
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
                    <li class="nav-item" v-if="isAuthenticated == false">
                        <a class="nav-link" href="#" @click="$router.push({ name: 'registration' })"
                            >Registration</a
                        >
                    </li>
                    <li v-if="isAuthenticated == true" class="nav-item">
                        <a class="nav-link" @click="$emit('logout')">Logout</a>
                    </li>
                    <li v-if="isAuthenticated == true" class="nav-item">
                        <a class="nav-link" @click="$router.push({ name: 'account' })">{{ userEmail }}</a>
                    </li>
                    <li v-else class="nav-item">
                        <a class="nav-link" @click="$router.push({ name: 'login' })">Login</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
    props: {
        isAuthenticated: {
            required: true,
            type: Boolean
        },
        userEmail: {
            required: false,
            type: String as PropType<string | null> 
        }
    },
    emits: {
        login: () => true,
        logout: () => true
    }
})
</script>

<style></style>
