# ForgeHub - Enterprise Developer Collaboration Platform

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
.\venv\Scripts\activate
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
