# create namespace for all components
kubectl create namespace postgres-tasks

# deploy cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml

kubectl apply -f ./pvcs

helm upgrade --install postgres-tasks postgres_tasks/ --values postgres_tasks/values.yaml