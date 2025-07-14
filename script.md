minikube start
minikube addons enable ingress
echo "$(minikube ip) madr.local" >> /etc/hosts
helm install madr deploy
