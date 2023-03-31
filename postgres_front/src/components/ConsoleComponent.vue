<template>
    <div class="">
        <div v-if="db_is_starting === true">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
         <div class="container-fluid console bg-dark" div v-else>
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


      <div class="row">
        <div class="col-12 mb-3">
          <div class="console-header">
            <i class="fas fa-terminal"></i> PostgreSQL Console
          </div>
        </div>
        <div class="col-12">
        
          <div class="console-body">
            <div class="console-line" v-if="previous_command !== ''">
              <strong><span class="console-prompt">postgres=#</span> {{ previous_command}}</strong>
            </div>
            <TableComponent id="console-table"
                        :dataResults="response_from_postgres.result"
                        :dataColumns="response_from_postgres.columns"
                    ></TableComponent>
            <blockquote class="blockquote">
                <p>{{response_from_postgres.status}}</p>
            </blockquote>

            <blockquote class="blockquote">
                <p>{{response_from_postgres.error_message}}</p>
            </blockquote> 
  
          </div>


        </div>
        <div class="col-12 mt-3">
          <form>
            <div class="input-group">
              <span class="input-group-text"><i class="fas fa-angle-right"></i></span>
              <input type="text" v-model="command" class="form-control console-input" placeholder="Enter command...">
            </div>
          </form>
          <div class="terminal-input">
                <button type="button" @click="sendCommand" ><i class="fas fa-play"></i> Execute</button>
                <button type="button"  data-bs-toggle="modal" data-bs-target="#forceCloseModal" ><i class="fas fa-check"></i> Pass Task</button>
                <button type="button" @click="closeTask"><i class="fas fa-trash"></i> Delete Task</button>
              </div>
        </div>
      </div>
    </div>
</div>

    
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import type { PropType } from 'vue'
import type PostgersCommandResponse from '@/types/PostgresCommandResponse';
import TableComponent from '@/components/TableComponent.vue';

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

        const previous_command = ref("")
        const command = ref("")
        function closeTask() {
            emit('close_task')
        }
        function sendCommand() {
            emit('send_command', command.value)
            previous_command.value = command.value
            command.value = ""
        }

        function endTask() {
            emit('end_task')
        }

        return {
            command,
            previous_command,
            closeTask,
            sendCommand,
             endTask
        }
    },
})
</script>

<style>
#console-table {
  margin-top: 15px;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: #1a1a1a;
  border-radius: 5px;
  border: 1px solid #1abc9c;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  padding: 20px;
}
.blockquote {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  color: #fff; 
}
.console {
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  padding: 20px;
}

.console-header {
  color: #1abc9c;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.console-line {
  color: #fff;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 5px;
}

.console-prompt {
  color: #1abc9c;
}

.console-output {
  color: #fff;
}

.console-input {
  background-color: #1a1a1a;
  border: none;
  color: #fff;
  font-size: 14px;
  padding: 10px;
}

.console-input:focus {
  background-color: #333;
  border: none;
  box-shadow: none;
  color: #fff;
  outline: none;
}

.input-group-text {
  background-color: #1a1a1a;
  border: none;
  color: #fff;
}

.input-group-text i {
  color: #1abc9c;
}

.terminal {
  background-color: #232937;
  border-radius: 0.5rem;
  padding: 1rem;
  height: 400px;
  overflow: auto;
}
.terminal-input {
  display: flex;
  align-items: center;
  margin-top: 1rem;
}
.terminal-input input[type="text"] {
  flex-grow: 1;
  border: none;
  background-color: transparent;
  color: #fff;
  font-family: "Fira Code", monospace;
  font-size: 1rem;
  padding: 0.5rem;
  outline: none;
}
.terminal-input button {
  background-color: #1abc9c;
  color: #fff;
  border: none;
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  margin-left: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.terminal-input button:hover {
  background-color: #126958;
}
   
   
</style>