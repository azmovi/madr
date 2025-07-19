#! /bin/bash
if helm status madr -n madr > /dev/null 2>&1; then
    helm uninstall madr -n madr
fi

minikube start
minikube addons enable ingress
sleep 30
eval $(minikube docker-env)
docker build -t backend:latest backend
docker build -t frontend:latest frontend
helm install madr deploy -n madr --create-namespace
