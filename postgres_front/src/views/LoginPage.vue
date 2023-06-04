<template>
    <div class="container">
        <div class="form-container">
            <h2>Login to Your Account</h2>
            <form>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="text" id="email" name="email" v-model="email" required />
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        v-model="password"
                        required
                    />
                </div>

                <div
                    v-if="error !== null"
                    class="alert alert-danger alert-dismissible fade show"
                    role="alert"
                >
                    <strong>Error:</strong> {{ error }}
                </div>
                <button class="btn btn-outline-custom-green login-button" @click="Login">
                    Login
                </button>

                <div class="forgot-password">
                    <a href="#" @click="$router.push({ name: 'registration' })">Have no account?</a>
                </div>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue'

export default defineComponent({
    emits: {
        login: (email: string, password: string) => true
    },
    props: {
        error: {
            type: null as unknown as PropType<string | null>,
            required: true
        }
    },
    setup(_, { emit }) {
        const email = ref('')
        const password = ref('')

        function Login() {
            if (email.value === '' || password.value === '') {
                return
            }
            emit('login', email.value, password.value)

            password.value = ''
        }
        return { Login, email, password }
    }
})
</script>

<style>
.forgot-password {
    text-align: right;
    font-size: 14px;
    margin-top: 10px;
}

.forgot-password a {
    color: var(--green-color);
    font-weight: bold;
}

.login-button {
    width: 100%;
    min-height: 50px;
}
</style>
