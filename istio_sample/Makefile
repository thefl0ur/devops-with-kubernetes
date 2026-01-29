up:
	k3d cluster create istio-sample --api-port 127.0.0.1:6550 \
		-p '9080:80@loadbalancer' -p '9443:443@loadbalancer' \
		--agents 2 --k3s-arg '--disable=traefik@server:*'
	kubectl config use-context k3d-istio-sample
	kubectl create namespace istio-system

	istioctl install --set profile=ambient --set values.global.platform=k3d -y

	kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
	kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/experimental-install.yaml

deploy:
	kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/platform/kube/bookinfo.yaml
	kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/platform/kube/bookinfo-versions.yaml

gateway:
	kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/bookinfo/gateway-api/bookinfo-gateway.yaml
	kubectl annotate gateway bookinfo-gateway networking.istio.io/service-type=ClusterIP --namespace=default
	kubectl port-forward svc/bookinfo-gateway-istio 8080:80


label:
	kubectl label namespace default istio.io/dataplane-mode=ambient

visualize:
	kubectl apply -f https://raw.githubusercontent.com/istio/istio/refs/heads/master/samples/addons/prometheus.yaml
	kubectl apply -f https://raw.githubusercontent.com/istio/istio/refs/heads/master/samples/addons/kiali.yaml

ddos:
	for i in $(seq 1 100); do curl -sSI -o /dev/null http://localhost:8080/productpage; done

auth:
	kubectl apply -f manifests/auth.yaml

curl:
	kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.28/samples/curl/curl.yaml
	kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage"

policies:
	istioctl waypoint apply --enroll-namespace --wait
	kubectl apply -f manifests/l7auth.yaml
	kubectl apply -f manifests/auth2.yaml

	# denied
	kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage" -X DELETE

	# denied
	kubectl exec deploy/reviews-v1 -- curl -s http://productpage:9080/productpage

	# ok
	kubectl exec deploy/curl -- curl -s http://productpage:9080/productpage | grep -o "<title>.*</title>"

route:
	kubectl apply -f manifests/route.yaml
	kubectl exec deploy/curl -- sh -c "for i in \$(seq 1 10); do curl -s http://productpage:9080/productpage | grep 'reviews-v.'; done"
