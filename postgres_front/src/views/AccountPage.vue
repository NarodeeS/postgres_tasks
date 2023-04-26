<template>
    <div>
    
        <div id="main-part" class="container-fluid" v-if="is_auntificated === true">
                  <div class="row">
                      <div class="col-4 tasks-control">
                          <h3>Задания:</h3>
                        <TaskListControlerComponent
                        :task_list="tasks" 
                        @deploy_task="deployTask"></TaskListControlerComponent>  
                      </div>
                    <div class="col-8 console-control">
                    <div v-if="task_controler.selected_task_id != null">
                      <div v-if="task_controler.task_passed_with_eror === true">
                      <ErrorAlertComponent></ErrorAlertComponent>
                      </div>  
                        <ConsoleComponent
                              @send_command="sendCommand"
                              @end_task="sendTaskForChecking"
                              @close_task="endTaskWithoutChecking" 
                              :db_is_starting="db_is_starting"
                              :task_passed_with_eror="task_controler.task_passed_with_eror"
                              :response_from_postgres_list="postgresResponseHistory"></ConsoleComponent>
                      </div>
                      <div v-else-if="task_controler.task_is_passed === true">
                          <SucessAlertComponent></SucessAlertComponent>
                          </div>
                    </div>
                </div>
        </div>
      </div>
    
    </template>
    
    <script lang="ts">
    import { defineComponent, ref } from "vue";
    import axios, {AxiosResponse}  from 'axios';
    import { useCookie } from 'vue-cookie-next'
    
    import type Task from "@/types/Task";
    import type TaskControler from "@/types/TaskControler";
    
    import TaskListControlerComponent from "@/components/TaskListControlerComponent.vue";
    import PostgresCommandResponse from "@/types/PostgresCommandResponse";
    import ConsoleComponent from "@/components/ConsoleComponent.vue";
    import SucessAlertComponent from "@/components/SucessAlertComponent.vue";
    import ErrorAlertComponent from "@/components/ErrorAlertComponent.vue";
    import router from "@/router";
    
    export default defineComponent({
      name: "App",
      components: {
          TaskListControlerComponent, 
          ConsoleComponent,
          SucessAlertComponent,
          ErrorAlertComponent,
        },
      mounted() {
          // axios.defaults.baseURL = `http://${process.env.VUE_APP_BASE_URL}/`
          // // axios.defaults.baseURL = `http://localhost:80/`
          // axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
          // axios.defaults.xsrfCookieName = "csrftoken";
          // axios.defaults.withCredentials = true;
    
          const cookie = useCookie()
          
          let token = cookie.getCookie("token")
    
          if (token) {
              this.is_auntificated = true;
              this.GeyTasks()
          } 
          else {
              this.is_auntificated = false;
              router.push({name: "login"})
          }
      }, 
      setup() {
          const cookie = useCookie()
          const headers = {
            Authorization: 'Token ' + cookie.getCookie("token")
          }          

          let token = cookie.getCookie("token")
          const dbName = ref<null | string>(null);
          const is_auntificated = ref(false);
          const db_is_starting = ref(false);
          const task_controler = ref<TaskControler>({
            showForceClose: false,
            selected_task_id: null,
            task_is_passed: false,
            task_passed_with_eror: false,
          });
          const postgresResponseHistory = ref<PostgresCommandResponse[]>([]);
    
          const tasks = ref<Task[]>([]);
      

          async function GeyTasks() {
            try {
              const response = await axios.get("api/tasks/", 
              {headers: headers});
              response.data.forEach((element: Task) => {
                tasks.value.push(element);
              });
            } catch (err) {
              router.push({name: "login"})
            }
          }

          function delay(milliseconds: number) {
                  return new Promise(resolve => {
                      setTimeout(resolve, milliseconds);
                });
          }
    
          async function endTaskWithoutChecking() {
                  try {
                    await axios.delete(`api/databases/${dbName.value}/` , {headers: headers})
                    postgresResponseHistory.value = []
                  } catch (err) {
                      return
                  }
                  clearFieldsAfterEndTaskWithoutChecking()
              }
  
          function clearFieldsAfterEndTaskWithoutChecking() {
                  task_controler.value.selected_task_id = null
                  task_controler.value.task_is_passed = false
                  task_controler.value.task_passed_with_eror = false
          }
    
          async function deployTask(id: number) {
                  if (task_controler.value.selected_task_id != null) {
                      alert("Вы не еще завешили начатое задание")
                      return
                  }
                  prepareFieldsBeforeDeployingTask(id)
                  let selected_task = tasks.value.find(x => x.id === task_controler.value.selected_task_id)
                  if (typeof selected_task === 'undefined'){
                    return
                  }
                  try {
                      const response = await axios.post(`/api/tasks/`,
                      {"task_id": selected_task.id,},
                      {headers: headers})
                        dbName.value = response.data.db_name
    
                  } catch (err) {
                     alert("Ошибка при создании базы данных")
                     return
                  }
                  checkIsDbStarted()
          }
          function prepareFieldsBeforeDeployingTask(id: number) {
                  task_controler.value.selected_task_id = id
                  db_is_starting.value = true
                  task_controler.value.task_is_passed = false
                  task_controler.value.task_passed_with_eror = false
              }
    
          async function checkIsDbStarted() {
                  await delay(1000);
    
                  let max_retries = 5;
                  let try_number = 0;
                  while (max_retries !== try_number || db_is_starting.value === false) {
                      try_number += 1;
                      await isDbStartedRequest()
    
                      if (db_is_starting.value === false) {
                          return
                      } 
                  }
              }
    
          async function isDbStartedRequest() {
                try {
                    const response = await axios.get(`api/databases/${dbName.value}/`, {headers: headers})
                    if (response.data.status === "up") {
                        db_is_starting.value = false;
                    }
                }
                catch (err) {
                    console.log(err);
                    task_controler.value.selected_task_id = null
                }
            }
    
          function updatePostgresResponseFields(response: AxiosResponse, command: string) {
                let index = 1
                let new_response: PostgresCommandResponse = {
                  status: response.data.status,
                  result: [],
                  error_message: response.data.error_message,
                  columns: response.data.columns,
                  command: command
                }

                if(response.data.result !== null){
                  response.data.result.forEach(function(el: any){
                      let raw = {
                        id : index,
                        data : el
                      } 
                      new_response.result.push(raw)
                      index += 1
                    })
                }
            
                postgresResponseHistory.value.push(new_response)
            }
      
          async function sendCommand(command: string) {
              task_controler.value.task_passed_with_eror = false
    
              try {
                  const response = await axios.post(`/api/databases/${dbName.value}/command/`,
                      { "command": command }, 
                      {headers: headers}
                  )
                  updatePostgresResponseFields(response, command)
              }
              catch (err: any) {
                  alert("Ошибка при выполнении команды")
                  return
              }
          }
          
          async function sendTaskForChecking() {
              try {
                  const response = await axios.post(`/api/databases/${dbName.value}/check/`, {}, {headers: headers})
                  if (response.data.detail === "Check error") {
                      task_controler.value.task_passed_with_eror = true
                      return
                  }
                  postgresResponseHistory.value = []
                  let selected_task = tasks.value.find(x => x.id === task_controler.value.selected_task_id)!
                  selected_task.completed = true
                  updateFieldsAfterSucses()
              }
              catch (err) {
                  task_controler.value.task_passed_with_eror = true
              }
          }
          function updateFieldsAfterSucses() {
              task_controler.value.selected_task_id = null
              task_controler.value.task_is_passed = true
          }
      
        return {
          is_auntificated,
          db_is_starting,
          task_controler,
          postgresResponseHistory,
          tasks,
          deployTask,
          sendCommand,
          sendTaskForChecking,
          endTaskWithoutChecking,
          GeyTasks,
        };
      },
    });
    </script>

<style>
.tasks-control{
    display: flex;
    flex-direction: column;
    /* align-items: center;
    justify-content: center; */
    margin-top: 20px;
}

.console-control{
    flex-direction: column;
    align-items: center; 
    margin-top: 60px;
}
</style>
