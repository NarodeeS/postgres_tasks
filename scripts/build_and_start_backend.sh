export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

docker-compose -f ./base-compose.yml \
    -f ./postgres_tasks/docker-compose.yml \
    build

docker-compose -f ./base-compose.yml \
    -f ./postgres_tasks/docker-compose.yml \
    up -d
