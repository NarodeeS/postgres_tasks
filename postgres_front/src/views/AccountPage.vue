<template>
    <div>
        <div id="main-part" class="container-fluid" v-if="isAuthenticated === true">
            <div class="row">
                <div class="col-4 tasks-control">
                    <h3>Задания:</h3>
                    <TaskListControlerComponent
                        :taskList="tasksList"
                        @deploy_task="deployTask"
                    ></TaskListControlerComponent>
                </div>
                <div class="col-8 console-control">
                    <ResultForTaskComponent :result="resultForTask"></ResultForTaskComponent>
                    <div v-if="taskId != null">
                        <ConsoleComponent
                            @send_command="sendCommand"
                            @end_task="sendTaskForChecking"
                            @close_task_without_cheking="endTaskWithoutChecking"
                            :dbIsStarting="dbIsStarting"
                            :turnNumber="movesLeft"
                            :responseFromPostgresList="postgresResponseHistory"
                        ></ConsoleComponent>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import axios, { AxiosResponse } from 'axios'
import { useCookie } from 'vue-cookie-next'

import type Task from '@/types/interfaces/Task'
import ResponseType from '@/types/enums/ResponesType'
import type PostgresCommandResponse from '@/types/interfaces/PostgresCommandResponse'

import TaskListControlerComponent from '@/components/TaskListControlerComponent.vue'
import ConsoleComponent from '@/components/ConsoleComponent.vue'
import ResultForTaskComponent from '@/components/ResultForTaskComponent.vue'

import router from '@/router'

export default defineComponent({
    name: 'App',
    components: {
        ResultForTaskComponent,
        TaskListControlerComponent,
        ConsoleComponent
    },
    mounted() {
        const cookie = useCookie()
        let token = cookie.getCookie('utoken')

        if (token) {
            this.isAuthenticated = true
            this.getTasksOrPushToLoginPage()
        } else {
            this.isAuthenticated = false
            router.push({ name: 'login' })
        }
    },
    emits: {
        get_email: () => true,
    },

    setup(_, { emit }) {
        // shitty code
       
         const cookie = useCookie()
        const headers = {
            Authorization: 'Token ' + cookie.getCookie('utoken')
        }

        const resultForTask = ref<ResponseType>(ResponseType.Moves_over)
        const movesLeft = ref<number>(0)
        const dbName = ref<null | string>(null)
        const isAuthenticated = ref(false)
        const dbIsStarting = ref(false)
        const taskId = ref<number | null>(null)

        const postgresResponseHistory = ref<PostgresCommandResponse[]>([])
        const tasksList = ref<Task[]>([])

        function delay(milliseconds: number) {
            return new Promise((resolve) => {
                setTimeout(resolve, milliseconds)
            })
        }

        async function getTasksOrPushToLoginPage() {
            resultForTask.value = ResponseType.None
            try {
                const response = await axios.get('api/tasks/', { headers: headers })
                response.data.forEach((element: Task) => {
                    tasksList.value.push(element)
                })
                emit('get_email')
            } catch (err) {
                router.push({ name: 'login' })
            }
        }

        function endTaskWithoutChecking() {
            makeRequestForDelitingdb()
            resultForTask.value = ResponseType.None
            taskId.value = null
        }

        async function makeRequestForDelitingdb() {
            try {
                await axios.delete(`api/databases/${dbName.value}/`, { headers: headers })
                postgresResponseHistory.value = []
            } catch (err) {
                console.log(err)
            }
        }

        async function deployTask(id: number) {
            if (taskId.value != null) {
                alert('Вы не еще завешили начатое задание')
                return
            }

            prepareFieldsBeforeDeployingTask(id)
            let selectedTask = tasksList.value.find((x) => x.id === taskId.value)
            if (typeof selectedTask === 'undefined') {
                return
            }

            await makeRequestIsDbStarted(selectedTask.id)
            checkIsDbStarted()
        }

        async function makeRequestIsDbStarted(taskId: number) {
            try {
                const response = await axios.post(
                    `/api/tasks/`,
                    { task_id: taskId },
                    { headers: headers }
                )
                dbName.value = response.data.db_name
                console.log(dbName.value)
            } catch (err) {
                console.log(err)
                alert('Ошибка при создании базы данных')
                return
            }
        }

        function prepareFieldsBeforeDeployingTask(id: number) {
            resultForTask.value = ResponseType.None
            taskId.value = id
            dbIsStarting.value = true
        }

        async function checkIsDbStarted() {
            await delay(1000)

            let max_retries = 5
            let try_number = 0
            while (max_retries !== try_number || dbIsStarting.value === false) {
                try_number += 1
                await isDbStartedRequest()

                if (dbIsStarting.value === false) {
                    return
                }
                await delay(1000)

            }
        }

        async function isDbStartedRequest() {
            try {
                const response = await axios.get(`api/databases/${dbName.value}/`, {
                    headers: headers
                })
                console.log(response)
                if (response.data.status === 'up') {
                    dbIsStarting.value = false
                    movesLeft.value = response.data.moves_left
                }
            } catch (err) {
                taskId.value = null
            }
        }

        async function sendCommand(command: string) {
            resultForTask.value = ResponseType.None
            if (command === '') {
                emptyComandWasSended()
                return
            } else {
                try {
                    const response = await axios.post(
                        `/api/databases/${dbName.value}/command/`,
                        { command: command },
                        { headers: headers }
                    )
                    updatePostgresResponseFields(response, command)

                    if (movesLeft.value === 0) {
                        let result = await makeRequestForTaskChecking()
                        if (result === true) {
                            resultForTask.value = ResponseType.Success_passed
                        }
                        else {
                            resultForTask.value = ResponseType.Moves_over
                        }
                        await makeRequestForDelitingdb()
                        taskId.value = null
                    }
                } catch (err: any) {
                    alert('Ошибка при выполнении команды')
                    return
                }
            }
        }

        function emptyComandWasSended() {
            let newPostgresResponseHistory: PostgresCommandResponse = {
                status: '',
                result: [],
                errorMessage: '',
                columns: null,
                command: ''
            }
            postgresResponseHistory.value.push(newPostgresResponseHistory)
        }

        function updatePostgresResponseFields(response: AxiosResponse, command: string) {
            movesLeft.value = response.data.moves_left
            let index = 1
            let newPostgresResponseHistory: PostgresCommandResponse = {
                status: response.data.status,
                result: [],
                errorMessage: response.data.error_message,
                columns: response.data.columns,
                command: command
            }

            if (response.data.result !== null) {
                response.data.result.forEach(function (el: any) {
                    let raw = {
                        id: index,
                        data: el
                    }
                    newPostgresResponseHistory.result.push(raw)
                    index += 1
                })
            }

            postgresResponseHistory.value.push(newPostgresResponseHistory)
        }

        async function sendTaskForChecking() {
                // deleteTaskIfTurnOut(response)
                let result = await makeRequestForTaskChecking()
                if (result === true) {
                    cleanFieldsAfterSuccess()
                    await makeRequestForDelitingdb()
                    return
                }
 
                resultForTask.value = ResponseType.Error_while_passing
        }

        async function makeRequestForTaskChecking(): Promise<boolean>{
            try {
                const response = await axios.post(
                    `/api/databases/${dbName.value}/check/`,
                    {},
                    { headers: headers }
                )
                return true

                // deleteTaskIfTurnOut(response)
                // cleanFieldsAfterSuccess()
            } catch (err) {
                console.log(err)
                // resultForTask.value = ResponseType.Error_while_passing
            }
            return false
        }

        // async function deleteTaskIfTurnOut(response: AxiosResponse) {
        //     if (response.data.detail === 'Check error') {
        //         if (movesLeft.value == 0) {
        //             postgresResponseHistory.value = []
        //             taskId.value = null
        //             resultForTask.value = ResponseType.Moves_over
        //             await makeRequestForDelitingdb()
        //         } else {
        //             resultForTask.value = ResponseType.Error_while_passing
        //         }
        //         return
        //     }
        // }

        function cleanFieldsAfterSuccess() {
            let selectedTask = tasksList.value.find((x) => x.id === taskId.value)
            if (typeof selectedTask === 'undefined') {
                return
            }
            selectedTask.completed = true
            resultForTask.value = ResponseType.Success_passed
            postgresResponseHistory.value = []
            taskId.value = null
        }

        return {
            resultForTask,
            isAuthenticated,
            dbIsStarting,
            taskId,
            postgresResponseHistory,
            tasksList,
            movesLeft,
            deployTask,
            sendCommand,
            sendTaskForChecking,
            endTaskWithoutChecking,
            getTasksOrPushToLoginPage
        }
    }
})
</script>

<style>
.tasks-control {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
}

.console-control {
    flex-direction: column;
    align-items: center;
    margin-top: 60px;
}
</style>
