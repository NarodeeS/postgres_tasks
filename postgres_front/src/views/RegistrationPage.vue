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
                        v-model="accountForm.firstName"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="surname">Surname</label>
                    <input
                        type="text"
                        id="surname"
                        name="surname"
                        v-model="accountForm.lastName"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="group">Group</label>
                    <input
                        type="text"
                        id="group"
                        name="group"
                        v-model="accountForm.studentGroup"
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
                        v-model="accountForm.repeatPassword"
                        required
                    />
                </div>

                <div
                    v-if="errorInRegistration !== null"
                    class="alert alert-danger alert-dismissible fade show"
                    role="alert"
                >
                    <strong>Error:</strong> {{ errorInRegistration }}
                </div>

                <button class="btn btn-outline-custom-green" @click="registration">Register</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import type AccountForm from '@/types/interfaces/AccoutForm'
import router from '../router'
import { useStore } from 'vuex'
import { key } from '@/store'

export default defineComponent({
    emits: {
        login: (email: string, password: string) => true
    },

    setup(_, { emit }) {
        const errorInRegistration = ref<null | string>(null)
        const store = useStore(key)
        const accountForm = ref<AccountForm>({
            firstName: '',
            lastName: '',
            studentGroup: '',
            email: '',
            password: '',
            repeatPassword: ''
        })

        function CheckFields(): boolean {
            if (
                accountForm.value.firstName === '' ||
                accountForm.value.lastName === '' ||
                accountForm.value.studentGroup === '' ||
                accountForm.value.email === '' ||
                accountForm.value.password === '' ||
                accountForm.value.repeatPassword === ''
            ) {
                return false
            }
            if (accountForm.value.password !== accountForm.value.repeatPassword) {
                errorInRegistration.value = 'Passwords are not equal!'
                return false
            }
            return true
        }

        async function registration() {
            errorInRegistration.value = null

            if (!CheckFields()) {
                return
            }
            try {
                await axios.post('api/auth/users/',
                                {     
                                    "first_name": accountForm.value.firstName,
                                    "last_name": accountForm.value.lastName,
                                    "student_group": accountForm.value.studentGroup,
                                    "email": accountForm.value.email,
                                    "password": accountForm.value.password
                                }
                )
                // accountForm.value)
                if (accountForm.value.email == '' || accountForm.value.password == '') {
                    errorInRegistration.value = 'Login or password is empty'
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
                router.push({ name: 'accountValidation' })
            } else {
                emit('login', accountForm.value.email, accountForm.value.password)
            }
        }

        function parseError(error: any) {
            try {
                if (error.response.data.password !== undefined) {
                    errorInRegistration.value = error.response.data.password[0]
                    return
                }
                if (error.response.data.email !== undefined) {
                    errorInRegistration.value = error.response.data.email[0]
                    return
                }
            } catch (error: any) {
                errorInRegistration.value =
                    'Something went wrong, try again or contact with support'
                return
            }
        }

        return {
            accountForm,
            errorInRegistration: errorInRegistration,
            registration
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
