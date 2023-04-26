<template>
    <div class="container">
        <div class="form-container">
            <h2>Registration Form</h2>
            <form @submit.prevent>
                <div class="form-group">
                    <label for="name">Code</label>
                    <input type="text" id="name" name="name" v-model="code" required>
                </div>

                <div v-if="errorInCodeValidation !== null" class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Error:</strong> {{errorInCodeValidation}}
                </div>

                <input type="submit" @click="Registration" value="Register">
            </form>
        </div>
    </div>

</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue'
import axios from 'axios';
import router from '../router';
import { useStore } from 'vuex'
import { key } from '@/store'


export default defineComponent({
    emits:{
      login: (email: string, password: string) => true
      },

    // mounted() {
    //     axios.defaults.baseURL = `http://${process.env.VUE_APP_BASE_URL}/`
    //     axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    //     axios.defaults.xsrfCookieName = "csrftoken";
    //     axios.defaults.withCredentials = true;   
    //     this.checkEmail()
    // },
    setup(_, { emit }) {
        const store = useStore(key)

        const code = ref<string>('')
        const errorInCodeValidation = ref <string | null>(null)

        function checkEmail() {
            if ( store.state.email === null) {

                router.push({name: 'registration'})
            }
        }

        async function Registration() {
            if (code.value === '') {
                errorInCodeValidation.value = 'Code is required'
                return
            }

            try{     
                const response = await axios.post('api/email/verification/', {
                    email: store.getters.email,
                    key: code.value
                })
                if (response.status === 200) {

                    emit('login', store.getters.email, store.getters.password)
                    router.push({name: 'account'})
                }
                else{
                    errorInCodeValidation.value = 'Code is not valid'
                }
            }
            catch (error : any) {
                console.log(error)
                return 
          }
        }

        return {
            code,
            errorInCodeValidation,
            Registration,
            checkEmail
        }
    }
    
})

</script>

<style>
 </style>