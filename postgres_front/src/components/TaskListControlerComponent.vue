<template>
    <div id="task-list">
        <TaskComponent
                v-for="task in task_list"
                :key="task.id"
                :task="task"
                @deploy_task="deployTask">
        </TaskComponent>
        </div> 
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import Task from '@/types/Task'
import TaskComponent from "@/components/OneTaskControler.vue"

export default defineComponent({
    components: {
        TaskComponent
    },
    props: {
        task_list: {
            required: true,
            type: Array as PropType<Task[]>
        }
    },
    emits:{
        deploy_task: (id:number) => true
    },

    setup(_, { emit }) {
        
        function deployTask(id: number)  {
            emit('deploy_task', id)
        }
        return {deployTask}
    },
})
</script>

<style>

</style>