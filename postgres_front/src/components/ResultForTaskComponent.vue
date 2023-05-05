<template>
    <div v-if="result != ResponseType.None">
        <div v-if="result === ResponseType.Success_passed">
            <SucessAlertComponent></SucessAlertComponent>
        </div>
        <div v-else-if="result === ResponseType.Error_while_passing">
            <ErrorAlertComponent></ErrorAlertComponent>
        </div>
        <div v-else-if="result  === ResponseType.Moves_over">
            <TurnOutWithErrorAlertComponent></TurnOutWithErrorAlertComponent>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

import ResponseType from '@/types/enums/ResponesType'

import SucessAlertComponent from '@/components/results/SucessAlertComponent.vue'
import ErrorAlertComponent from '@/components/results/ErrorAlertComponent.vue'
import TurnOutWithErrorAlertComponent from '@/components/results/TurnOutWithError.vue'

export default defineComponent({
    props: {
        result: {
            type: Number as PropType<ResponseType>,
            required: true
        }
    },

    components: {
        SucessAlertComponent,
        ErrorAlertComponent,
        TurnOutWithErrorAlertComponent
    },
    setup() {
        return {
          ResponseType
        }
    }
})
</script>
