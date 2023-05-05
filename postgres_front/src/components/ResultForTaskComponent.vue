<template>
    <div v-if="result != 'none'">
        <div v-if="result === 'success_passed'">
            <SucessAlertComponent></SucessAlertComponent>
        </div>
        <div v-else-if="result === 'error_while_passing'">
            <ErrorAlertComponent></ErrorAlertComponent>
        </div>
        <div v-else-if="result  === 'move_over'">
            <TurnOutWithErrorAlertComponent></TurnOutWithErrorAlertComponent>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

import type ResponseType from '@/types/ResponesType'

import SucessAlertComponent from '@/components/results/SucessAlertComponent.vue'
import ErrorAlertComponent from '@/components/results/ErrorAlertComponent.vue'
import TurnOutWithErrorAlertComponent from '@/components/results/TurnOutWithError.vue'

export default defineComponent({
    props: {
        result: {
            // type: Object as PropType<ResponseType>,
            type: String,
            required: true
        }
    },

    components: {
        SucessAlertComponent,
        ErrorAlertComponent,
        TurnOutWithErrorAlertComponent
    }
})
</script>
