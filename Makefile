SHELL := /bin/bash

.PHONY: help install build run test clean docker-build docker-run

help:
	@echo "ForgeHub Build System"
	@echo "  make install      - Install frontend and backend dependencies"
	@echo "  make build        - Compile full stack (Maven & Vite)"
	@echo "  make run          - Launch containers with docker-compose"
	@echo "  make test         - Run automated JUnit and frontend tests"
	@echo "  make docker-build - Build production Docker containers"

install:
	npm install
	cd frontend && npm install
	python -m venv venv || true

build:
	cd frontend && npm run build
	cd backend && (./mvnw package -DskipTests || mvn package -DskipTests)

run:
	docker-compose up -d

test:
	cd backend && (./mvnw test || mvn test)

docker-build:
	docker build -t forgehub-backend ./backend
	docker build -t forgehub-frontend ./frontend
	docker build -t forgehub .

docker-run:
	docker-compose up -d

clean:
	rm -rf frontend/dist backend/target
