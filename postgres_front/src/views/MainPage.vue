<template>
    <div>
        <header class="bg-dark text-white py-5">
            <div class="container">
            <div class="row">
                <div class="col-md-8">
                <h1>Learn PostgreSQL from Scratch</h1>
                <p class="lead">A comprehensive guide to master PostgreSQL.</p>
                <a href="#" @click="$router.push({name: 'account'})" class="btn btn-custom-green btn-success btn-lg mt-4">Get Started</a>
                </div>
            </div>
            </div>
        </header>

        <!-- Features -->
        <section class="py-5">
            <div class="container">
            <div class="row">
                <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                    <i class="fa fa-database fa-4x mb-3" aria-hidden="true"></i>
                    <h3>Database Management</h3>
                    <p class="card-text">Learn how to manage databases and perform CRUD operations with PostgreSQL.</p>
                    <a href="#" @click="$router.push({name: 'account'})" class="btn btn-custom-green btn-success">Learn More</a>
                    </div>
                </div>
                </div>
                <div class="col-md-4 mb-4">
                <div class=""></div>
                </div>
            </div>
            </div>
        </section>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({

})
</script>
<style>

</style>