## Log Output

Simple app that generates random string and writes it to STDOUT every 5 seconds

## HOWTOs

With makefile next operations are available:
* `build` - builds image with name `$IMAGE`
* `tag` - set `$VERSION` `$IMAGE`
* `publish` - publishes `$IMAGE`to Dockerhub

### Manual deploy into cluster

```bash
kubectl create deployment log-output --image=$IMAGE
```

Validate working

```bash
kubectl logs -f log-output-<some-uuid>
```
or

```bash
kubectl logs -f deployments/log-output
```

### Applying manifest

```basg
kubectl apply -f manifests/deployment.yaml
```