include .env

all: build tag publish

build:
	docker build -f Dockerfile.generator -t $(IMAGE)_generator .
	docker build -f Dockerfile.server -t $(IMAGE)_server .

tag:
	docker tag $(IMAGE)_generator $(IMAGE)_generator:$(VERSION)
	docker tag $(IMAGE)_generator $(IMAGE)_generator:latest

	docker tag $(IMAGE)_server $(IMAGE)_server:$(VERSION)
	docker tag $(IMAGE)_server $(IMAGE)_server:latest

publish:
	docker push $(IMAGE)_generator:$(VERSION)
	docker push $(IMAGE)_generator:latest

	docker push $(IMAGE)_server:$(VERSION)
	docker push $(IMAGE)_server:latest
