# create namespace for all components
kubectl create namespace postgres-tasks

# deploy cert-manager
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.11.1/cert-manager.yaml

helm upgrade --install postgres-tasks postgres_tasks/ --values postgres_tasks/values.yaml