# create namespace for all components
kubectl create namespace postgres-tasks

# deploy kubernetes dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# deploy cert-manager
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.11.1/cert-manager.yaml

# deploy all other resources
kubectl apply -f ./config_maps --recursive
kubectl apply -f ./secrets/secrets.yml --recursive
kubectl apply -f ./pvcs --recursive
kubectl apply -f ./backend --recursive
kubectl apply -f ./frontend --recursive
kubectl apply -f ./monitoring --recursive
kubectl apply -f ./tls--recursive
