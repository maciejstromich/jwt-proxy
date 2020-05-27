DOCKER_COMPOSE ?= docker-compose 
DC_RUN_ARGS ?= --rm
CONTAINER_NAME = proxy
DOCKER_SHELL ?= $(DOCKER_COMPOSE) run $(DC_RUN_ARGS) $(CONTAINER_NAME)
run:
	$(DOCKER_SHELL)


samlple_command:
	curl -v --data '{"user": "username", "date": "todays_date"}' -x POST http://localhost:8000/

build: 
	$(DOCKER_COMPOSE) build

format:
	$(DOCKER_SHELL) black -t py38 -l 120 


