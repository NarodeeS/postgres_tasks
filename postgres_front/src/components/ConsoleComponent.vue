<template>
    <div class="console-component">
        <div v-if="dbIsStarting === true">
            <div class="d-flex justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
        </div>

        <div class="container-fluid console" div v-else>
            <div
                class="modal fad"
                id="forceCloseModal"
                tabindex="-1"
                aria-labelledby="exampleModalLabel"
                aria-hidden="true"
            >
                <div class="modal-dialog custom-modal">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">Вы уверены ?</h1>
                        </div>
                        <div class="modal-body">
                            Вы хотите прервать задание ? Это действие нельзя будет отменить
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-warning" data-bs-dismiss="modal">
                                Отмена
                            </button>
                            <button
                                type="button"
                                class="btn btn-outline-danger"
                                data-bs-dismiss="modal"
                                @click="$emit('end_task')"
                            >
                                Закончить задание
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="terminal-container">
                <div class="terminal-header">
                    <div>PostgreSQL Terminal</div>
                </div>
                <div class="terminal-body" id="terminal">
                    <p v-if="responseFromPostgresList.length === 0">
                        Welcome to PostgreSQL Terminal!
                    </p>
                    <p v-if="responseFromPostgresList.length === 0">
                        <span class="terminal-prompt">$</span> <span class="user-input"></span>
                    </p>

                    <div
                        v-for="one_commnad in responseFromPostgresList"
                        v-bind:key="one_commnad.status"
                    >
                        <div class="console-line">
                            <strong
                                ><span class="console-prompt">postgres=#</span>
                                {{ one_commnad.command }}</strong
                            >
                        </div>
                        <TableComponent
                            v-if="one_commnad.columns !== null"
                            id="console-table"
                            :dataResults="one_commnad.result"
                            :dataColumns="one_commnad.columns"
                        ></TableComponent>
                        <blockquote class="blockquote">
                            <p>{{ one_commnad.status }}</p>
                        </blockquote>

                        <blockquote class="blockquote">
                            <p>{{ one_commnad.error_message }}</p>
                        </blockquote>
                    </div>
                </div>
                <div class="input-container">
                    <label for="input-field" class="input-label">Input:</label>
                    <textarea 
                        cols='20' rows='1'
                        class="input-field form-control"
                        v-model="command"
                        id="input-field"
                    />
                </div>
                <div class="row console-navigation">
                    <div class="col-5 single-line">
                        <p>
                            Turns: <strong>{{ turnNumber }}</strong>
                        </p>
                    </div>

                    <div class="col-7">
                        <button
                            type="button"
                            @click="sendCommand"
                            class="btn ml-2 btn-outline-custom-green"
                        >
                            Send Command
                        </button>
                        <button
                            type="button"
                            data-bs-toggle="modal"
                            data-bs-target="#forceCloseModal"
                            class="btn ml-2 btn-outline-custom-green"
                        >
                            Pass Task
                        </button>
                        <button
                            type="button"
                            @click="$emit('close_task_without_cheking')"
                            class="btn ml-2 btn-outline-custom-red"
                        >
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, nextTick, ref } from 'vue'
import type { PropType } from 'vue'
import type PostgersCommandResponse from '@/types/interfaces/PostgresCommandResponse'
import TableComponent from '@/components/TableComponent.vue'

export default defineComponent({
    components: {
        TableComponent
    },
    props: {
        dbIsStarting: {
            required: true,
            type: Boolean
        },
        responseFromPostgresList: {
            required: true,
            type: Object as PropType<PostgersCommandResponse[]>
        },
        turnNumber: {
            required: true,
            type: Number
        }
    },
    watch: {
        responseFromPostgresList: {
            handler: async function (val, oldVal) {
                var element = document.getElementById('terminal')!
                await nextTick()
                element.scrollTop = element.scrollHeight
            },
            deep: true
        }
    },

    emits: {
        close_task_without_cheking: () => true,
        end_task: () => true,
        send_command: (command: string) => true
    },

    setup(_, { emit }) {
        const command = ref('')

        function sendCommand() {
            emit('send_command', command.value)
            command.value = ''
        }
        return {
            command,
            sendCommand,
        }
    }
})
</script>

<style>
.terminal-container {
    padding: 15px;
    border: 1px solid var(--green-color);
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
    display: block;
    resize: vertical;
    overflow: auto;
}
.terminal-prompt {
    color: var(--green-color);
}
.console-navigation {
    margin-top: 20px;
}

.input-container {
    display: flex;
    align-items: center;
    margin-top: 10px;
}

.input-label {
    margin-right: 10px;
}

.input-field {
    background-color: #3e4460;
    flex-grow: 1;
    color: #fff;
}
.input-field:focus {
    outline: 1px solid var(--green-color);
    background-color: #3e4460;
    color: #fff;
}
.console-prompt {
    color: var(--green-color);
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

.single-line {
    color: #ffc107;
}
</style>
