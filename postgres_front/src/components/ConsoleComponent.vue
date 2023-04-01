<template>
<div class="console-component">
    <div v-if="db_is_starting === true">
      <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </div>

    <div class="container-fluid console" div v-else>

        <div class="modal fad " id="forceCloseModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog custom-modal">
                  <div class="modal-content">
                      <div class="modal-header">
                          <h1 class="modal-title fs-5" id="exampleModalLabel">Вы уверены ?</h1>
                      
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

        <div class="terminal-container">
          <div class="terminal-header">
            <div>PostgreSQL Terminal</div>
            <div><i class="fas fa-power-off"></i></div>
          </div>
          <div class="terminal-body">
            <p>Welcome to PostgreSQL Terminal!</p>
            <p><span class="terminal-prompt">$</span> <span class="user-input"></span></p>

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

          </div >
            <div class="input-container">
              <label for="input-field" class="input-label">Input:</label>
              <input type="text" class="input-field form-control" v-model="command" id="input-field">
            </div>

            <div class="input-container container-buttons">
              <button type="button" @click="sendCommand" class="btn ml-2 btn-custom-green">Submit</button>
              <button type="button" data-bs-toggle="modal" data-bs-target="#forceCloseModal"  class="btn ml-2 btn-custom-green">Pass</button>
              <button type="button" @click="closeTask" class="btn ml-2 btn-custom-red">Delete</button>
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

.terminal-container {
  padding: 15px;
  border: 1px solid #1abc9c;
  margin: auto;
  width: 90%;
  max-width: 700px;
  border-radius: 10px;
  background-color: #1c1e26;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
  overflow: hidden;

}
.terminal-header {
  background-color: #2c3e50;
  color: #fff;
  padding: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.2rem;
}
.terminal-body {
  padding: 10px;
  overflow-y: scroll;
  height: 300px;
  resize: vertical;
  overflow: auto;
}
.terminal-prompt {
  color: #1abc9c;
}
.input-container {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.container-buttons {
  display: flex;
  justify-content: flex-end;
}
.input-label {
  margin-right: 10px;
}
.input-field {
  background-color: #3e4460;
  flex-grow: 1;
}
.input-field:focus {
  outline: 1px solid #1abc9c;
  background-color: #3e4460;
  color: #fff;
}
.console-prompt{
  color: #1abc9c; 
}

.btn-custom-red {
    color: #fff;
    background-color: #dc3545;
    border: none;
    border-radius: 3px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}

.btn-custom-red:hover {
  background-color: #c82333;
}

.modal-content {
  background-color: #3f4457;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

</style>