<template>
    <div class="container">
        <div class="form-container">
            <h2>Registration Form</h2>
            <form @submit.prevent>
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" v-model="accountForm.first_name" required>
                </div>
                <div class="form-group">
                    <label for="surname">Surname</label>
                    <input type="text" id="surname" name="surname" v-model="accountForm.last_name" required>
                </div>
                <div class="form-group">
                    <label for="group">Group</label>
                    <input type="text" id="group" name="group" v-model="accountForm.student_group" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" v-model="accountForm.email" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" v-model="accountForm.password" required>
                </div>
                <div class="form-group">
                    <label for="repeat_password">Repeat Password</label>
                    <input type="password" id="repeat_password" name="repeat_password" v-model="accountForm.repeat_password" required>
                </div>

                <div v-if="errorInRegistrartion !== null" class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Error:</strong> {{errorInRegistrartion}}
                </div>

                <input type="submit" @click="Registration" value="Register">
            </form>
        </div>
    </div>

</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios from 'axios';
import type AccountForm from '@/types/AccoutForm'
import router from '../router';

export default defineComponent({
    emits:{
      login: (email: string, password: string) => true
  },

    setup(_, { emit }) {
        const errorInRegistrartion = ref<null | string>(null)
        const accountForm = ref<AccountForm>({
            first_name: '',
            last_name: '',
            student_group: '',
            email: '',
            password: '',
            repeat_password: ''
        })
        
        function CheckFields(): boolean {
            if (accountForm.value.first_name === '' || accountForm.value.last_name === '' || accountForm.value.group === '' || accountForm.value.email === '' || accountForm.value.password === '' || accountForm.value.repeat_password === '') {
               return false
            }
            if (accountForm.value.password !== accountForm.value.repeat_password) {
                errorInRegistrartion.value = 'Passwords are not equal !'
                return false
            }
            else {
                return true
            }
        }

                
        async function Registration() {
            errorInRegistrartion.value = null
            
            if (!CheckFields()) {
                return
            }
            console.log(accountForm.value)
            try{
                const response = await axios.post('api/auth/users/', accountForm.value)
                emit('login', accountForm.value.email, accountForm.value.password)
                router.push({name: 'account'})
            }
            catch (error : any) {
                console.log(error)
                if (error.response.data.password !== undefined) {
                    errorInRegistrartion.value =error.response.data.password[0]
                    return
                }
                if (error.response.data.email !== undefined) {
                    errorInRegistrartion.value =error.response.data.email[0]
                    return
                }
                return 
          }
        }

        return {
            accountForm,
            Registration,
            errorInRegistrartion 
        }
    }
    
})

</script>

<style>
 </style>