include .env

all: build tag publish

build:
	docker build -t $(IMAGE) .
	
tag:
	docker tag $(IMAGE) $(IMAGE):$(VERSION)
	docker tag $(IMAGE) $(IMAGE):latest

publish:
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest
