from common_writer import write_file

backend_docker = """# Build stage
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /workspace
COPY pom.xml .
COPY src ./src
RUN ./mvnw clean package -DskipTests || mvn clean package -DskipTests

# Run stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
RUN addgroup -S forgehub && adduser -S forgehub -G forgehub
USER forgehub:forgehub
COPY --from=builder /workspace/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
"""
write_file("backend/Dockerfile", backend_docker)

frontend_docker = """# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
write_file("frontend/Dockerfile", frontend_docker)

docker_compose = """version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: forgehub-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: forgehub
      POSTGRES_USER: forgehub
      POSTGRES_PASSWORD: forgehub_secure_pass
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U forgehub"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: forgehub-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: forgehub-backend
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      SPRING_PROFILES_ACTIVE: prod
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: forgehub
      DB_USER: forgehub
      DB_PASSWORD: forgehub_secure_pass
      REDIS_HOST: redis
      REDIS_PORT: 6379
      VAULT_KEY: 635266556A586E3272357538782F413F4428472B4B6250645367566B5970404E
    volumes:
      - gitdata:/app/data/git-repositories
      - uploaddata:/app/data/uploads
    ports:
      - "8080:8080"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: forgehub-frontend
    restart: unless-stopped
    depends_on:
      - backend
    ports:
      - "3000:80"

volumes:
  pgdata:
  redisdata:
  gitdata:
  uploaddata:
"""
write_file("docker-compose.yml", docker_compose)

k8s_backend = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: forgehub-backend
  namespace: forgehub
  labels:
    app: forgehub-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: forgehub-backend
  template:
    metadata:
      labels:
        app: forgehub-backend
    spec:
      containers:
        - name: backend
          image: forgehub/backend:1.0.0
          ports:
            - containerPort: 8080
          envFrom:
            - configMapRef:
                name: forgehub-config
            - secretRef:
                name: forgehub-secrets
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2000m
              memory: 2Gi
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 20
            periodSeconds: 5
"""
write_file("infrastructure/kubernetes/backend-deployment.yaml", k8s_backend)

ci_workflow = """name: ForgeHub Platform CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: maven
      - name: Build with Maven
        run: mvn clean verify -B
        working-directory: backend

  frontend-build-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      - name: Install dependencies
        run: npm ci
        working-directory: frontend
      - name: Build frontend
        run: npm run build
        working-directory: frontend
"""
write_file(".github/workflows/ci.yml", ci_workflow)

readme = """# ForgeHub - Enterprise Developer Collaboration Platform

ForgeHub is a production-grade developer collaboration platform inspired by modern engineering systems like GitHub and GitLab. It provides complete Git repository lifecycle management, native JGit object browsing, pull request code review threads, automated branch protection validation, Kanban boards, discussions, real-time STOMP WebSockets, HMAC-signed webhooks with exponential backoff retries, isolated CI/CD workflows, and fine-grained RBAC access control.

## System Architecture

- **Backend**: Modular monolith built with **Java 21**, **Spring Boot 3.3**, **Spring Security**, **Spring Data JPA**, **JGit 6.10**, **Flyway**, **PostgreSQL 16**, and **Redis 7**.
- **Frontend**: Single Page Application built with **React 18/19**, **TypeScript**, **Vite**, **Tailwind CSS**, **Monaco Editor**, **TanStack Query**, and **Zustand**.
- **Security**: Argon2id password hashing, rotating JWT refresh tokens, AES-256-GCM encrypted secrets vault, OWASP XSS sanitizer, and server-side RBAC SpEL evaluators for IDOR protection.

## Quick Start (Docker Compose)

```bash
docker-compose up -d
```

Access the web interface at `http://localhost:3000` and the REST API at `http://localhost:8080/swagger-ui.html`.

## REST API Overview

| Path | Description |
| :--- | :--- |
| `POST /api/v1/auth/register` | Register developer account |
| `POST /api/v1/auth/login` | Authenticate and obtain JWT access & refresh tokens |
| `GET /api/v1/repositories` | List public Git repositories |
| `POST /api/v1/repositories` | Create a new Git repository |
| `GET /api/v1/repositories/{id}/git/tree` | Explore directory tree at revision |
| `GET /api/v1/repositories/{id}/git/blob` | Retrieve file content and line metadata |
| `GET /api/v1/repositories/{id}/git/commits` | Walk commit history |
| `GET /api/v1/repositories/{id}/git/commits/{sha}/diff` | Calculate commit diff hunks |
| `POST /api/v1/repositories/{id}/issues` | Create an issue |
| `POST /api/v1/repositories/{id}/pulls` | Open a pull request |
| `POST /api/v1/repositories/{id}/pulls/{number}/merge` | Merge pull request with strategy |

## License

MIT License (c) 2026 ForgeHub Contributors
"""
write_file("README.md", readme)

print("gen_phase14_infra_docs complete.")