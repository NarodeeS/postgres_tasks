# create namespace for all components
kubectl create namespace postgres-tasks

# start all components except tls
kubectl apply -f ./config_maps --recursive
kubectl apply -f ./secrets/secrets.yml --recursive
kubectl apply -f ./pvcs --recursive
kubectl apply -f ./backend --recursive
kubectl apply -f ./frontend --recursive
kubectl apply -f ./monitoring --recursive
kubectl apply -f ./ingress-dev.yml --recursive
