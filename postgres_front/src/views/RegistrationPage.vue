<template>
    <div class="container">
        <div class="form-container">
            <h2>Registration Form</h2>
            <form @submit.prevent>
                <div class="form-group">
                    <label for="name">Name</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        v-model="accountForm.first_name"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="surname">Surname</label>
                    <input
                        type="text"
                        id="surname"
                        name="surname"
                        v-model="accountForm.last_name"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="group">Group</label>
                    <input
                        type="text"
                        id="group"
                        name="group"
                        v-model="accountForm.student_group"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        v-model="accountForm.email"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        v-model="accountForm.password"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="repeat_password">Repeat Password</label>
                    <input
                        type="password"
                        id="repeat_password"
                        name="repeat_password"
                        v-model="accountForm.repeat_password"
                        required
                    />
                </div>

                <div
                    v-if="errorInRegistrartion !== null"
                    class="alert alert-danger alert-dismissible fade show"
                    role="alert"
                >
                    <strong>Error:</strong> {{ errorInRegistrartion }}
                </div>

                <button class="btn btn-outline-custom-green register-button" @click="Registration">
                    Register
                </button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import type AccountForm from '@/types/AccoutForm'
import router from '../router'
import { useStore } from 'vuex'
import { key } from '@/store'

export default defineComponent({
    emits: {
        login: (email: string, password: string) => true
    },

    setup(_, { emit }) {
        const errorInRegistrartion = ref<null | string>(null)
        const store = useStore(key)
        const accountForm = ref<AccountForm>({
            first_name: '',
            last_name: '',
            student_group: '',
            email: '',
            password: '',
            repeat_password: ''
        })

        function CheckFields(): boolean {
            if (
                accountForm.value.first_name === '' ||
                accountForm.value.last_name === '' ||
                accountForm.value.student_group === '' ||
                accountForm.value.email === '' ||
                accountForm.value.password === '' ||
                accountForm.value.repeat_password === ''
            ) {
                return false
            }
            if (accountForm.value.password !== accountForm.value.repeat_password) {
                errorInRegistrartion.value = 'Passwords are not equal !'
                return false
            } else {
                return true
            }
        }

        async function Registration() {
            errorInRegistrartion.value = null

            if (!CheckFields()) {
                return
            }
            try {
                await axios.post('api/auth/users/', accountForm.value)
                if (accountForm.value.email == '' || accountForm.value.password == '') {
                    errorInRegistrartion.value = 'Login or password is empty'
                    return
                }
                redirectToAccountOrToVerification()
            } catch (error: any) {
                parseError(error)
            }
        }

        function redirectToAccountOrToVerification() {
            if (process.env.VUE_APP_VERIFICATE_EMAIL === 'yes') {
                store.state.email = accountForm.value.email
                store.state.password = accountForm.value.password
                router.push({ name: 'accountValdidation' })
            } else {
                emit('login', accountForm.value.email, accountForm.value.password)
                router.push({ name: 'account' })
            }
        }

        function parseError(error: any) {
            try {
                if (error.response.data.password !== undefined) {
                    errorInRegistrartion.value = error.response.data.password[0]
                    return
                }
                if (error.response.data.email !== undefined) {
                    errorInRegistrartion.value = error.response.data.email[0]
                    return
                }
            } catch (error: any) {
                errorInRegistrartion.value =
                    'Something went wrong, try again or contact with support'
                return
            }
        }

        return {
            accountForm,
            errorInRegistrartion,
            Registration
        }
    }
})
</script>

<style>
.register-button {
    width: 100%;
    min-height: 50px;
}
</style>
