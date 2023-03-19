<template>
            <div class="card" id="one-task-control">
            <h5 class="card-header">{{task.task_name}}</h5>
            <div class="card-body">
                <h5 class="card-title">{{task.complexity}}</h5>
                <p class="card-text">{{task.description}}</p>
                <a @click="deployTask" class="btn btn-outline-primary"
                >Start task</a>
            </div>
        </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import Task from '@/types/Task'

export default defineComponent({
    props: {
        task:{
            required: true,
            type: Object as PropType<Task>
        }
    },
    emits:{
        deploy_task: (id:number) => true
    },

    setup(props, { emit }) {
        
        function deployTask() {
            emit('deploy_task', props.task.id)
        }
        return {deployTask}
    }
})
</script>

<style>
#one-task-control{
    margin: 7px;
}
</style>
