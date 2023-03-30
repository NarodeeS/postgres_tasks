<template>
    <div>
    
        <div id="main-part" class="container-fluid" v-if="is_auntificated === true">
                  <div class="row">
                      <div class="col-4">
                          <h3>Задания:</h3>
                        <TaskListControlerComponent
                        :task_list="tasks" 
                        @deploy_task="deployTask"></TaskListControlerComponent>  
                      </div>
                    <div class="col-8">
                    <div v-if="task_controler.selected_task_id != null">
                      <div v-if="task_controler.task_passed_with_eror === true">
                      <ErrorAlertComponent></ErrorAlertComponent>
                      </div>  
                      
                      <h3>Консоль:</h3>
                        <ConsoleComponent 
                              @send_command="sendCommand"
                              @end_task="sendTaskForChecking"
                              @close_task="endTaskWithoutChecking" 
                              :db_is_starting="db_is_starting"
                              :task_passed_with_eror="task_controler.task_passed_with_eror"
                              :response_from_postgres="postgres_response_on_command"></ConsoleComponent>
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
          axios.defaults.baseURL = `http://${process.env.VUE_APP_BASE_URL}:8000/`
          axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
          axios.defaults.xsrfCookieName = "csrftoken";
          axios.defaults.withCredentials = true;
    
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
          
          let token = cookie.getCookie("token")
     
          const is_auntificated = ref(false);
          const db_is_starting = ref(false);
          const task_controler = ref<TaskControler>({
            showForceClose: false,
            selected_task_id: null,
            task_is_passed: false,
            task_passed_with_eror: false,
          });
          const postgres_response_on_command = ref<PostgresCommandResponse>({
            status: "",
            results: [],
            columns: null,
            error: "",
          });
    
          const tasks = ref<Task[]>([
            {
              id: 1,
              title: "Task1",
              description:
                "Создать таблицу user с полями name, surname, age и внести в нее 2 строки",
              difficulty: "Hard",
            },
          ]);
      

          async function GeyTasks() {
            try {
              const response = await axios.get("api/tasks/", 
              {   headers: {
                'Authorization': 'Token ' + token
              }});
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
                      await axios.delete("/db/test_db/")
                  } catch (err) {
                      console.log(err);
                      return
                  }
                  clearFieldsAfterEndTaskWithoutChecking()
                  clearPostgresResponseFields()
              }
    
          function clearPostgresResponseFields() {
                  postgres_response_on_command.value.status = ""
                  postgres_response_on_command.value.results = []
                  postgres_response_on_command.value.error = ""
                  postgres_response_on_command.value.columns = null
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
                      await axios.post(`/db/`,
                      {"task_name": selected_task.title,},
                            )
    
                  } catch (err) {
                      console.error(err);
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
                      } else {
                          console.log("db dont started")
                      }
                  }
              }
    
          async function isDbStartedRequest() {
                try {
                    const response = await axios.get("/db/test_db/")
                    if (response.data.status === "up") {
                        db_is_starting.value = false;
                    }
                }
                catch (err) {
                    console.log(err);
                    task_controler.value.selected_task_id = null
                }
            }
    
          function updatePostgresResponseFields(response: AxiosResponse) {
                let index = 1
                postgres_response_on_command.value.status = response.data.status
                response.data.result.forEach(function(el: any){
                      let raw = {
                        id : index,
                        data : el
                      } 
                      postgres_response_on_command.value.results.push(raw)
                      index += 1
                    })
      
                postgres_response_on_command.value.columns = response.data.columns
            }
      
          async function sendCommand(commnad: string) {
              clearPostgresResponseFields()
              task_controler.value.task_passed_with_eror = false
    
              try {
                  const response = await axios.post("/db/test_db/command/",
                      { "command": commnad }
                  )
                  updatePostgresResponseFields(response)
              }
              catch (err: any) {
                  if (err !instanceof TypeError){
                    return
                  }
                  else {
                    if (typeof (err.response.data) != "undefined")
                        postgres_response_on_command.value.error = err.response.data.error
                   } 
            }
          }
          
          async function sendTaskForChecking() {
              try {
                  await axios.post("/db/test_db/check/")
                  clearPostgresResponseFields()
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
          postgres_response_on_command,
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
    
    </style>
    