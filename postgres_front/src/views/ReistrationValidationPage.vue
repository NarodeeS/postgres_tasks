<template>
    <div class="container">
        <div class="form-container">
            <h2>Registration Form</h2>
            <form @submit.prevent>
                <div class="form-group">
                    <label for="name">Code</label>
                    <input type="text" id="name" name="name" v-model="code" required />
                </div>

                <div
                    v-if="errorInCodeValidation !== null"
                    class="alert alert-danger alert-dismissible fade show"
                    role="alert"
                >
                    <strong>Error:</strong> {{ errorInCodeValidation }}
                </div>

                <input type="submit" @click="registration" value="Register" />
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import router from '../router'
import { useStore } from 'vuex'
import { key } from '@/store'
import { AxiosResponse } from 'axios'

export default defineComponent({
    emits: {
        login: (email: string, password: string) => true
    },

    setup(_, { emit }) {
        const store = useStore(key)
        const code = ref<string>('')
        const errorInCodeValidation = ref<string | null>(null)

        function checkEmail() {
            if (store.state.email === null) {
                router.push({ name: 'registration' })
            }
        }

        async function registration() {
            if (code.value === '') {
                errorInCodeValidation.value = 'Code is required'
                return
            }

            try {
                const response = await axios.post('api/email/verification/', {
                    email: store.getters.email,
                    key: code.value
                })
                checkResponse(response)
            } catch (error: any) {
                return
            }
        }

        function checkResponse(response: AxiosResponse) {
            if (response.status === 200) {
                emit('login', store.getters.email, store.getters.password)
                router.push({ name: 'account' })
            } else {
                errorInCodeValidation.value = 'Code is not valid'
            }
        }

        return {
            code,
            errorInCodeValidation,
            registration,
            checkEmail
        }
    }
})
</script>

<style></style>
