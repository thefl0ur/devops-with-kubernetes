# DummySite

DummySite resource that can be used to create an HTML page from any URL.

## Acess with Port Forwarding:

## Accessing the DummySite Service

1. Find the service name:
```bash
   kubectl get svc
```
2. Find service created for your DummySite - `<your-resource-name>-dummysite-service`

3. Forward port:

```bash
kubectl port-forward service/<service-name> 8080:80
```

4. Open in browser [http://localhost:8080](http://localhost:8080)