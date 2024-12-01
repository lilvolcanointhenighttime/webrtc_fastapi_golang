## Start (Старт)
k8s deployment(minikube)

```
kubectl apply -f kubectl apply -f https://raw.githubusercontent.com/nginxinc/kubernetes-ingress/v3.7.2/deploy/crds.yaml

minikube start
minikube addons enable ingress
minikube addons enable ingress-dns
```

Build docker images(just run)
```
docker-compose up -d
docker-compose down
```

```
minikube image load webrtc-fastapi-golang-webrtc_fastapi:latest
minikube image load webrtc-fastapi-golang-websocket_chat_golang:latest
minikube image load webrtc-fastapi-golang-nodejs:latest
```

```
kubectl apply -f ./src/ops/.kube/
kubectl get ing
```

Edit your local dns(hosts) pasting "domain ADDRESS" value

```
minikube tunnel
```