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
            <ModalComponent @end_task="$emit('end_task')"></ModalComponent>

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
                        v-for="oneCommnad in responseFromPostgresList"
                        v-bind:key="oneCommnad.status"
                    >
                        <div class="console-line">
                            <strong
                                ><span class="console-prompt">postgres=#</span>
                                {{ oneCommnad.command }}</strong
                            >
                        </div>
                        <TableComponent
                            v-if="oneCommnad.columns !== null"
                            id="console-table"
                            :dataResults="oneCommnad.result"
                            :dataColumns="oneCommnad.columns"
                        ></TableComponent>
                        <blockquote class="blockquote">
                            <p>{{ oneCommnad.status }}</p>
                        </blockquote>

                        <blockquote class="blockquote">
                            <p>{{ oneCommnad.errorMessage }}</p>
                        </blockquote>
                    </div>
                </div>
                <div class="input-container">
                    <label for="input-field" class="input-label">Input:</label>
                    <textarea
                        cols="20"
                        rows="1"
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
import ModalComponent from './ModalComponent.vue'

export default defineComponent({
    components: {
        TableComponent,
        ModalComponent
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
            sendCommand
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
    background-color: var(--gray-color);
    color: var(--white-color);
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
    background-color: var(--light-grey-color);
    flex-grow: 1;
    color: var(--white-color);
}
.input-field:focus {
    outline: 1px solid var(--green-color);
    background-color: var(--light-grey-color);
    color: var(--white-color);
}
.console-prompt {
    color: var(--green-color);
}

.single-line {
    color: var(--yellow-color);
}
</style>
