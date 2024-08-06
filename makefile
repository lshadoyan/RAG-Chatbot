PYTHON = python3
PYTHON_V = venv/bin/python3
PIP = venv/bin/pip
ACTIVATE = venv/bin/activate
DOCKER_COMPOSE = docker-compose

.DEFAULT_GOAL := help

.PHONY: venv preprocess build run clean

$(ACTIVATE): requirements.txt
	$(PYTHON) -m venv venv
	chmod +x $(ACTIVATE)
	. $(ACTIVATE)
	$(PIP) install -r requirements.txt

venv: $(ACTIVATE)
	. ./$(ACTIVATE)

preprocess: venv
	$(PYTHON_V) preprocess.py 

build:
	$(DOCKER_COMPOSE) up --build -d

run:
	$(DOCKER_COMPOSE) up -d

stop:
	$(DOCKER_COMPOSE) stop

clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

help:
	@echo "Available targets:"
	@echo "  venv        - Create and activate a Python virtual environment"
	@echo "  preprocess  - Run the preprocessing script in the virtual environment"
	@echo "  build       - Build and start Docker containers in detached mode"
	@echo "  run         - Start Docker containers in detached mode"
	@echo "  stop        - Stop the Docker containers"
	@echo "  clean       - Stop and remove all Docker containers, images, and volumes"
	@echo "  help        - Display this help message"
