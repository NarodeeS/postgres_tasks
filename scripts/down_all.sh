docker-compose -f ./base-compose.yml \
    -f ./postgres_tasks/docker-compose.yml \
    -f ./postgres_front/docker-compose.yml \
    -f ./monitoring/docker-compose.yml \
    down
