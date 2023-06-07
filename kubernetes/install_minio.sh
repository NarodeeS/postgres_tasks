kubectl create namespace postgres-tasks

helm upgrade --install minio minio/ --values minio/values.yaml
