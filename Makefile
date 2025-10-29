# Makefile

# Use bash as the default shell
SHELL := /bin/bash

.PHONY: help build up down logs migrate shell clean

help:
	@echo "Available commands:"
	@echo "  make build    Build or rebuild the api docker image"
	@echo "  make up       Start all services (api, db) in the background"
	@echo "  make down     Stop and remove all services"
	@echo "  make logs     Follow the logs of the api service"
	@echo "  make migrate  Run Prisma database migrations inside the api container"
	@echo "  make shell    Get a bash shell inside the running api container"
	@echo "  make clean    Stop services and remove the database volume (DANGER: DATA LOSS)"

build:
	@echo "Building docker images..."
	docker-compose build

up:
	@echo "Starting services in detached mode..."
	docker-compose up --build -d

down:
	@echo "Stopping services..."
	docker-compose down

logs:
	@echo "Following logs for the api service..."
	docker-compose logs -f api

# This is the command to run Prisma migrations within the running container
migrate:
	@echo "Running database migrations..."
	docker-compose exec api prisma migrate dev

shell:
	@echo "Accessing bash shell in the api container..."
	docker-compose exec api bash

clean: down
	@echo "Removing database volume..."
	docker-compose down -v