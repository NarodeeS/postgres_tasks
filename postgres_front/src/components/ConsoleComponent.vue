<template>
    <div>
        <div v-if="db_is_starting === true">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div v-else>

            <div class="modal fade" id="forceCloseModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">Вы уверены ?</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            Вы хотите прервать задание ? Это действие нельзя будет отменить
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-warning" data-bs-dismiss="modal">Отмена</button>
                            <button type="button" class="btn btn-outline-danger" data-bs-dismiss="modal" @click="endTask">
                                Закончить задание</button>
                        </div>
                    </div>
                </div>
            </div>


            <div class="mb-3" >
                <label  for="exampleFormControlTextarea1" class="form-label">SQL code</label>
                <textarea v-model="command" class="form-control" id="exampleFormControlTextarea1" rows="3">
                </textarea>
            </div>

            <div>
                <TableComponent
                    :dataResults="response_from_postgres.results"
                    :dataColumns="response_from_postgres.columns"
                ></TableComponent>

                <blockquote class="blockquote">
                    <p>{{response_from_postgres.status}}</p>
                </blockquote>

                <blockquote class="blockquote">
                    <p>{{response_from_postgres.error}}</p>
                </blockquote>
            </div>
            
            <button type="button" @click="sendCommand" class="btn btn-outline-success">Run</button>
            <button type="button" class="btn btn-outline-primary"
                    data-bs-toggle="modal" data-bs-target="#forceCloseModal">Сдать задание</button>
            <button type="button" @click="closeTask" id="btn_close_task" class="btn btn-outline-danger">Delete database</button>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from 'vue'
import PostgersCommandResponse from '@/types/PostgresCommandResponse';
import TableComponent from './TableComponent.vue';

export default defineComponent({
    components: {
        TableComponent,
    },
    props: {
        db_is_starting:{
            required: true,
            type: Boolean
        },
        response_from_postgres: {
            required: true,
            type : Object as PropType<PostgersCommandResponse> 
        },
    },
    emits:{
        close_task: () => true,
        end_task: () => true,
        send_command: (command: string) => true
    },
    
    setup(_, {emit}) {
        const command = ref("")
        function closeTask() {
            emit('close_task')
        }
        function sendCommand() {
            emit('send_command', command.value)
            command.value = ""
        }

        function endTask() {
            emit('end_task')
        }

        return {
            command,
            closeTask,
            sendCommand,
             endTask
        }
    },
})
</script>

<style>
#btn_close_task{
    position: absolute;
    right: 15px;
}


</style>