<template>
    <div id="task-list">
        <OneTaskComponent
            v-for="task in task_list"
            :key="task.id"
            :task="task"
            @deploy_task="$emit('deploy_task', task.id)"
        >
        </OneTaskComponent>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import type Task from '@/types/interfaces/Task'
import OneTaskComponent from '@/components/OneTaskControler.vue'

export default defineComponent({
    components: {
        OneTaskComponent
    },
    props: {
        task_list: {
            required: true,
            type: Array as PropType<Task[]>
        }
    },
    emits: {
        deploy_task: (id: number) => true
    },
})
</script>

<style></style>
