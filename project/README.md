# The Project also known as ToDo App

Creates webserver on `$PORT` or 8000.


## HOWTOs

With makefile next operations are available:
* `build` - builds image with name `$IMAGE`
* `tag` - set `$VERSION` `$IMAGE`
* `publish` - publishes `$IMAGE`to Dockerhub

### Deploy into cluster

```bash
kubectl create deployment project --image=$IMAGE
```

Validate working

```bash
kubectl logs -f project-<some-uuid>
```
or

```bash
kubectl logs -f deployments/project
```

Port forwarding

```bash
kubectl port-forward project--<some-uuid> <local_port>:<internal_port>
```

Create forlder used as pv
```
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/todo_app/
```