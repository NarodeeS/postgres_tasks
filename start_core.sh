docker-compose -f ./base-compose.yml \
    -f ./postgres_tasks/docker-compose.yml \
    -f ./postgres_front/docker-compose.yml \
    up -d
