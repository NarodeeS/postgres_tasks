# create namespace for all components
kubectl create namespace postgres-tasks

kubectl apply -f ./pvcs

helm upgrade --install postgres-tasks postgres_tasks/ --values postgres_tasks/values.yaml