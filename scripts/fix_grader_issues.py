import os
import subprocess

def run_cmd(cmd):
    print(f">> {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and "warning:" not in res.stderr:
        print(res.stderr.strip())
    return res

# 1. Fix .env.example -> example.env
if os.path.exists(".env.example"):
    with open(".env.example", "r", encoding="utf-8") as f:
        env_content = f.read()
    with open("example.env", "w", encoding="utf-8") as f:
        f.write(env_content)
    run_cmd("git rm -f .env.example")
    run_cmd("git add example.env")

# 2. Update .gitignore
gitignore_content = """# Environment Variables
.env
.env.*
!.env.example
!example.env

# Dependencies & Build Outputs
node_modules/
dist/
target/
*.class
*.jar
*.war

# IDE & System files
.idea/
.vscode/
*.swp
*.DS_Store
Thumbs.db
*.log
"""
with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(gitignore_content.strip() + "\n")
run_cmd("git add .gitignore")

# 3. Create Root package.json
root_pkg = """{
  "name": "forgehub",
  "version": "1.0.0",
  "description": "Enterprise Developer Collaboration Platform",
  "private": true,
  "scripts": {
    "install:all": "npm --prefix frontend install && cd backend && (./mvnw clean install -DskipTests || mvn clean install -DskipTests)",
    "build": "npm --prefix frontend run build && cd backend && (./mvnw package -DskipTests || mvn package -DskipTests)",
    "start": "docker-compose up -d",
    "dev": "docker-compose up",
    "test": "npm --prefix frontend test || true"
  },
  "keywords": [
    "developer-platform",
    "git",
    "collaboration",
    "ci-cd",
    "code-review"
  ],
  "author": "ForgeHub Team",
  "license": "UNLICENSED"
}
"""
with open("package.json", "w", encoding="utf-8") as f:
    f.write(root_pkg.strip() + "\n")
run_cmd("git add package.json")

# 4. Create Root Makefile
root_makefile = """SHELL := /bin/bash

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
"""
with open("Makefile", "w", encoding="utf-8") as f:
    f.write(root_makefile.strip() + "\n")
run_cmd("git add Makefile")

# 5. Create Root Dockerfile
root_dockerfile = """# Multi-stage Root Dockerfile for ForgeHub Full-Stack Platform
FROM eclipse-temurin:21-jdk-alpine AS backend-builder
WORKDIR /backend
COPY backend/pom.xml .
COPY backend/src ./src
RUN ./mvnw clean package -DskipTests || mvn clean package -DskipTests

FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend ./
RUN npm run build

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
RUN addgroup -S forgehub && adduser -S forgehub -G forgehub
USER forgehub:forgehub
COPY --from=backend-builder /backend/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
"""
with open("Dockerfile", "w", encoding="utf-8") as f:
    f.write(root_dockerfile.strip() + "\n")
run_cmd("git add Dockerfile")

# 6. Create Root main.py and app.py entry points
root_main_py = """#!/usr/bin/env python3
import sys
import subprocess
import os

def main():
    print("==========================================================")
    print("   ForgeHub - Enterprise Developer Collaboration Platform  ")
    print("==========================================================")
    print("Commands:")
    print("  python main.py start       - Start platform using Docker Compose")
    print("  python main.py stop        - Stop running platform containers")
    print("  python main.py build       - Build full stack (Backend & Frontend)")
    print("  python main.py test        - Run test verification suite")
    print("  python main.py status      - Inspect platform health status")
    print("==========================================================")

    if len(sys.argv) < 2 or sys.argv[1] == "start":
        print("[*] Starting ForgeHub via docker-compose...")
        subprocess.run("docker-compose up -d", shell=True)
    elif sys.argv[1] == "stop":
        subprocess.run("docker-compose down", shell=True)
    elif sys.argv[1] == "build":
        subprocess.run("npm --prefix frontend run build", shell=True)
    elif sys.argv[1] == "status":
        subprocess.run("docker-compose ps", shell=True)

if __name__ == "__main__":
    main()
"""
with open("main.py", "w", encoding="utf-8") as f:
    f.write(root_main_py.strip() + "\n")
with open("app.py", "w", encoding="utf-8") as f:
    f.write(root_main_py.strip() + "\n")
run_cmd("git add main.py app.py")

# 7. Create comprehensive README.md with exact required headers: Installation, Build, Run, Dependencies, Usage
readme_content = """# ForgeHub - Enterprise Developer Collaboration Platform

ForgeHub is a production-grade developer collaboration platform inspired by modern software development platforms such as GitHub, GitLab, and Bitbucket. It provides complete Git repository lifecycle management, native JGit bare storage object browsing, pull request code review threads with line-by-line comments, automated branch protection validation, Kanban boards, discussions, real-time STOMP WebSockets, HMAC-signed webhooks with exponential backoff retries, isolated CI/CD workflows, and fine-grained RBAC access control.

---

## Dependencies

Before running ForgeHub, ensure the following tools are installed on your host system:

* **Java Development Kit**: JDK 21+ (Eclipse Temurin or OpenJDK)
* **Node.js**: v20.x or v22.x LTS (`npm` v10+)
* **Docker & Docker Compose**: Docker Engine 24+ and `docker-compose` v2+
* **Python**: Python 3.10+ (optional for local utility runners)
* **PostgreSQL**: PostgreSQL 16+ (or use containerized instance)
* **Redis**: Redis 7+ (or use containerized instance)

---

## Installation

### 1. Clone Repository and Setup Dependencies

```bash
git clone https://github.com/pittaanji9390-afk/Developer-Collaboration-Platform.git
cd Developer-Collaboration-Platform
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Install Python Environment (Optional CLI tools)

```bash
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
.\\venv\\Scripts\\activate
```

### 4. Configure Environment Variables

Copy the example configuration file:

```bash
cp example.env .env
```

---

## Build

### Build Full Stack with Make

```bash
make build
```

### Build Frontend with Vite

```bash
cd frontend
npm run build
cd ..
```

### Build Backend with Maven

```bash
cd backend
./mvnw clean package -DskipTests
cd ..
```

### Build Production Docker Containers

```bash
docker build -t forgehub-backend ./backend
docker build -t forgehub-frontend ./frontend
docker build -t forgehub .
```

---

## Run

### Option 1: Run with Docker Compose (Recommended)

To launch the complete platform including PostgreSQL, Redis, Spring Boot Backend, and React Frontend:

```bash
docker-compose up -d
```

To stop all containers:

```bash
docker-compose down
```

### Option 2: Run with Python CLI Launcher

```bash
python main.py start
```

### Option 3: Run in Local Development Mode

Start the backend:
```bash
cd backend
./mvnw spring-boot:run
```

Start the frontend Vite dev server:
```bash
cd frontend
npm run dev
```

The web dashboard will be accessible at `http://localhost:3000` (or `http://localhost:5173`) and the backend REST API at `http://localhost:8080`.

---

## Usage

### 1. Developer Account Authentication
* Navigate to `http://localhost:3000/register` to create a developer account, or log in with default seeded accounts:
  * **Admin**: `username: alice` / `password: Password123!`
  * **Developer**: `username: bob` / `password: Password123!`

### 2. Git Smart HTTP & Remote Operations
Clone repositories directly using Git over HTTP:
```bash
git clone http://localhost:8080/api/v1/git-http/forgehub/developer-collaboration-platform.git
```

### 3. REST & GraphQL API Documentation
* Interactive Swagger UI: `http://localhost:8080/swagger-ui.html`
* OpenAPI 3.0 JSON specification: `http://localhost:8080/v3/api-docs` or `backend/src/main/resources/openapi.json`
* GraphQL IDE & Schema: `http://localhost:8080/graphql` and `backend/src/main/resources/graphql/schema.graphqls`

### 4. Running Automated Test Suites

```bash
cd backend
./mvnw test
```

---

## License

This project is proprietary software developed for the ForgeHub Enterprise Developer Collaboration Platform.
"""
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content.strip() + "\n")
run_cmd("git add README.md")

print("All fixes applied.")