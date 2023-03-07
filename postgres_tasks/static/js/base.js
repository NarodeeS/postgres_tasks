Vue.component('one-task-controler', {
    template: `
        <div class="card" id="one-task-control">
            <h5 class="card-header">{{task.task_name}}</h5>
            <div class="card-body">
                <h5 class="card-title">{{task.complexity}}</h5>
                <p class="card-text">{{task.description}}</p>
                <a @click="deployTask" class="btn btn-outline-primary"
                >Start task</a>
            </div>
        </div>
    `,
    props: {
        task: Object
    },
    methods: {
        deployTask() {
            this.$emit('deploy_task', this.task.id)
        }
    },
});


Vue.component('tasks-list-controler', {
    template: `
        <div id="task-list">
            <one-task-controler
                v-for="task in task_list" 
                :key="task.id"
                :task="task"
                @deploy_task="deployTask">
                        </one-task-controler>
        </div>
    `,
    props: {
        task_list: Array
    },
    methods: {
        deployTask(id) {
            this.$emit('deploy_task', id)
        }
    },
});


Vue.component('console', {
    template: `
    <div id="console-form">
      <div>
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
        <button type="button" @click="sendCommand" class="btn btn-outline-success">Run</button>
        <button type="button" class="btn btn-outline-primary" 
            data-bs-toggle="modal" data-bs-target="#forceCloseModal">Сдать задание</button>
        </div>
    </div>
    `,
    data: function() {
        return {
            command: ''
        }
    },
    methods: {
        sendCommand() {
            this.$emit('send_command', this.command)
        },
        endTask() {
            this.$emit('end_task')
        }
    },
});


var main_component = new Vue({
    el: "#app",

    data: function() {
        return {
            showForceClose: false,
            state: Object,
            selected_task_id: null,
            tasks: [
                {
                    id: 1,
                    task_name: "task 1",
                    description: "Intersting decription",
                    complexity: "Hard"
                },
                {
                    id: 2,
                    task_name: "task 2",
                    description: "Very intersting decription number two",
                    complexity: "Insane"
                },
            ]
        }
    },
    mounted() {
        this.getTasks()
    },
    methods: {
        getTasks() {
            console.log("making request for tasks")
        },
        deployTask(id) {

            if (this.selected_task_id != null) {
                alert("Вы не еще завешили начатое задание")
                return
            }

            this.selected_task_id = id

            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.withCredentials = true;
            axios({
                method: "post",
                url: "http://localhost:8000/db/"
            })
                .then(function() {
                    console.log("deploying task " + id)
                })
                .catch(function(response) {
                    console.log(response);
                });
        },
        sendCommand(commnad) {
            console.log(commnad)
        },
        endTask() {
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.withCredentials = true;
            axios({
                method: "delete",
                url: "http://localhost:8000/db/test_db"
            })
                .then(function() {
                    console.log("task " + this.selected_task_id + " has closed")
                })
                .catch(function(response) {
                    console.log(response);
                })

            this.selected_task_id = null


        }
    }
})
