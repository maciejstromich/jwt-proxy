DOCKER_COMPOSE ?= docker-compose 
DC_RUN_ARGS ?= --rm
CONTAINER_NAME = proxy
DOCKER_SHELL ?= $(DOCKER_COMPOSE) run $(DC_RUN_ARGS) $(CONTAINER_NAME)
run:
	$(DOCKER_SHELL)


sample_command:
	curl -v --data '{"key1": "value", "key2": "value"}' -H "Content-Type: application/json" -X POST http://localhost:8000/

status:
	curl -v http://localhost:8000/status

build: 
	$(DOCKER_COMPOSE) build

format:
	$(DOCKER_SHELL) /usr/local/bin/black -t py38 -l 120 . 


