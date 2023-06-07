docker-compose -f ./base-compose.yml \
    -f ./minio-compose.yml \
    -f ./postgres_tasks/docker-compose.yml \
    -f ./postgres_front/docker-compose.yml \
    -f ./monitoring/docker-compose.yml \
    down
