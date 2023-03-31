<template>
    <div class="card-task mb-3 bg-dark border-success">
        <div class="card-body">
            <h5 class="card-title custom-text">{{task.title}}</h5>
            <p class="card-text text-white">{{task.completed}}</p>
            <p class="card-text text-white">{{task.difficulty}}</p>
            <p class="card-text text-white">{{task.description}}</p>
            <div class="row justify-content-between align-items-center">
                <div class="col-6">
                    <p class="card-text text-muted">Due Date: 12/31/2023</p>
                </div>
                <div class="col-6 text-end">
                    <button class="btn btn-custom-green " @click="deployTask">Start task</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import type Task from '@/types/Task'

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
.card-task {
  border-radius: 15px;
  box-shadow: 0px 3px 15px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.card-text {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.custom-text{
  color: #1abc9c;
}


</style>
