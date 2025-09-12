include .env

IMAGES ?= generator server

all: $(IMAGES:%=publish-%)

build-%:
	docker build -f Dockerfile.$* -t $(IMAGE)_$* .

tag-%:
	docker tag $(IMAGE)_$* $(IMAGE)_$*:$(VERSION)
	docker tag $(IMAGE)_$* $(IMAGE)_$*:latest

publish-%: build-% tag-%
	docker push $(IMAGE)_$*:$(VERSION)
	docker push $(IMAGE)_$*:latest
