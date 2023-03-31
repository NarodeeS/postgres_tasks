<template>
    <div class="container">
        <div class="form-container">
            <h2>Registration Form</h2>
            <form>
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="surname">Surname</label>
                    <input type="text" id="surname" name="surname" required>
                </div>
                <div class="form-group">
                    <label for="group">Group</label>
                    <input type="text" id="group" name="group" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-group">
                    <label for="repeat_password">Repeat Password</label>
                    <input type="password" id="repeat_password" name="repeat_password" required>
                </div>
                <input type="submit" value="Register">
            </form>
        </div>
    </div>

</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    
})

</script>

<style>
 </style>