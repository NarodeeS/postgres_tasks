<template>
    <div class="alert custom-alert" role="alert">
      <h4 class="alert-heading">Well done!</h4>
      <p>A yeah, you successfully pass the task.</p>
      <hr>
      <p class="mb-0">You can try to pass it again.</p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
})
</script>

<style>
.custom-alert{
  color: #ffc107;
  background-color: #3f4457;
}

</style>