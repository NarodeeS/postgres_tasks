<template>
    <div>
        <header class="bg-dark text-white py-5">
            <div class="container">
                <div class="row">
                    <div class="col-md-8">
                        <h1 class="ml9">
                            <span class="text-wrapper">
                                <span class="letters"
                                    >Решайте задачи в PostgreSQL так легко, что это кажется игрой
                                    @ChatGPT
                                </span>
                            </span>
                        </h1>

                        <a
                            href="#"
                            @click="$router.push({ name: 'account' })"
                            class="btn btn-custom-green btn-success btn-lg mt-4"
                            >Get Started</a
                        >
                    </div>
                </div>
            </div>
        </header>

        <!-- Features -->
        <section class="py-5">
            <div class="container">
                <div class="row">
                    <div class="col-md-4 mb-4"></div>
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
import anime from 'animejs'

export default defineComponent({
    mounted() {
        const textWrapper = document.querySelector('.ml9 .letters')
        textWrapper!.innerHTML = textWrapper!.textContent!.replace(
            /\S/g,
            "<span class='letter'>$&</span>"
        )

        anime
            .timeline({ loop: true })
            .add({
                targets: '.ml9 .letter',
                scale: [0, 1],
                duration: 1500,
                elasticity: 600,
                delay: (el, i) => 45 * (i + 1)
            })
            .add({
                targets: '.ml9',
                opacity: 0,
                duration: 1000,
                easing: 'easeOutExpo',
                delay: 1000
            })
    }
})
</script>
<style>
.ml9 {
    position: relative;
    font-weight: 200;
    font-size: 35px;
}

.ml9 .text-wrapper {
    position: relative;
    display: inline-block;
    padding-top: 0.2em;
    padding-right: 0.05em;
    padding-bottom: 0.1em;
    overflow: hidden;
}

.ml9 .letter {
    transform-origin: 50% 100%;
    display: inline-block;
    line-height: 1em;
}
</style>
