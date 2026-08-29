# ForgeHub - Enterprise Developer Collaboration Platform

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
