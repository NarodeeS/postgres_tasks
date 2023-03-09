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

Vue.component('table-result', {
    template: `
    <table v-if="data_colums != null" class="table">
        <thead >
            <tr>
                <th scope="col">#</th>
                <th scope="col" v-for="column in data_colums">{{column}}</th>
            </tr>
        </thead> 

        <tbody>
            <tr v-for="element in data_results">
            <td scope="col" v-for="raw_element in element">{{raw_element}}</td>
            </tr>
        </tbody>
    </table> 
    `,
    props: {
        data_results: Array,
        data_colums: Array
    },
});


Vue.component('console', {
    template: `
    <div id="console-form">
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
            <table-result 
                :data_results="response_from_postgres.result"
                :data_colums="response_from_postgres.columns"
            ></table-result>
        
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
        </div>
    
    </div>
    `,
    props: {
        db_is_starting: Boolean,
        response_from_postgres: Object | Array,
    },
    data: function() {
        return {
            command: ''
        }
    },
    methods: {
        sendCommand() {
            this.$emit('send_command', this.command)
            this.command = ""
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
            postgres_response_on_command: {
                "status": "",
                "columns": null,
                "result": [],
                "error": ""
            },
            db_is_starting: false,
            tasks: [
                {
                    id: 1,
                    task_name: "task1",
                    description: "Intersting decription",
                    complexity: "Hard"
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
        delay(milliseconds) {
            return new Promise(resolve => {
                setTimeout(resolve, milliseconds);
            });
        },
        async checkIsDbStarted() {
            await this.delay(1000);

            let max_retries = 5;
            let try_number = 0;
            while (max_retries !== try_number || this.db_is_starting === false) {
                try_number += 1;

                let res = await axios.get(
                    "http://localhost:8000/db/test_db/"
                )
                    .then(response => {
                        if (response.data.status === "up") {
                            this.db_is_starting = false;
                            return
                        }
                    })
                    .catch(response => {
                        console.log(response);
                        this.selected_task_id = null
                    })

                if (this.db_is_starting === false) {
                    break
                } else {
                    await this.delay(1000);
                }
            }
            if (this.db_is_starting === true) {
                this.selected_task_id = null
                this.db_is_starting === false
            }
        },

        deployTask(id) {
            if (this.selected_task_id != null) {
                alert("Вы не еще завешили начатое задание")
                return
            }
            this.selected_task_id = id
            this.db_is_starting = true

            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.withCredentials = true;

            let selected_task = this.tasks.find(x => x.id === this.selected_task_id)
            axios({
                method: "post",
                url: `http://localhost:8000/db/`,
                data: { "task_name": selected_task.task_name }
            })
                .then(function() {
                    console.log("start deploing task " + id)
                })
                .catch(function(response) {
                    // console.log(response);
                });
            this.checkIsDbStarted()
        },

        async sendCommand(commnad) {
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.withCredentials = true;

            this.postgres_response_on_command.status = ""
            this.postgres_response_on_command.result = []
            this.postgres_response_on_command.error = ""

            try {
                const response = await axios.post("http://localhost:8000/db/test_db/command/",
                    { "command": commnad }
                )

                this.postgres_response_on_command['status'] = response.data.status
                this.postgres_response_on_command['result'] = response.data.result
                this.postgres_response_on_command['columns'] = response.data.columns
                let index = 1
                if (this.postgres_response_on_command['result'] != null) {
                    this.postgres_response_on_command['result'].forEach(el => {
                        el.unshift(index)
                        index += 1
                    })
                }
            }
            catch (err) {
                console.log(err)
                if (typeof (err.response.data) != "undefined")
                    this.postgres_response_on_command['error'] = err.response.data.error
            }
        },

        endTask() {
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.withCredentials = true;
            axios({
                method: "delete",
                url: "http://localhost:8000/db/test_db/"
            })
                .catch(function(response) {
                    console.log(response);
                })

            this.selected_task_id = null

        }
    }
})
