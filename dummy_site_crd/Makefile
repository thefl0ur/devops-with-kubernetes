include .env

# create cluster
up:
	k3d cluster create dummy-cluster --agents 1 --api-port 127.0.0.1:6550 -p "8081:80@loadbalancer"
	kubectl config use-context k3d-dummy-cluster

# destroy cluster
down:
	k3d cluster delete dummy-cluster

# buld image and inject into cluster
build:
	docker build -t $(IMAGE):$(VERSION) .
	k3d image import $(IMAGE):$(VERSION) -c dummy-cluster

# deploy CRD
deploy:
	kubectl apply -f manifests/

# deploy resource
test:
	kubectl apply -f example.yaml
