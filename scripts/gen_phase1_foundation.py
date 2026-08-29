import os

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as out:
        out.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.strip().splitlines())} lines)")

pom = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.3</version>
        <relativePath/>
    </parent>
    <groupId>com.forgehub</groupId>
    <artifactId>forgehub-backend</artifactId>
    <version>1.0.0</version>
    <name>forgehub-backend</name>
    <description>ForgeHub - Enterprise Developer Collaboration Platform</description>

    <properties>
        <java.version>21</java.version>
        <jgit.version>6.10.0.202406030300-r</jgit.version>
        <jjwt.version>0.12.6</jjwt.version>
        <springdoc.version>2.6.0</springdoc.version>
        <bouncycastle.version>1.78.1</bouncycastle.version>
        <bucket4j.version>8.10.1</bucket4j.version>
        <commonmark.version>0.22.0</commonmark.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-websocket</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.flywaydb</groupId>
            <artifactId>flyway-core</artifactId>
        </dependency>
        <dependency>
            <groupId>org.flywaydb</groupId>
            <artifactId>flyway-database-postgresql</artifactId>
        </dependency>
        <dependency>
            <groupId>org.eclipse.jgit</groupId>
            <artifactId>org.eclipse.jgit</artifactId>
            <version>${jgit.version}</version>
        </dependency>
        <dependency>
            <groupId>org.eclipse.jgit</groupId>
            <artifactId>org.eclipse.jgit.archive</artifactId>
            <version>${jgit.version}</version>
        </dependency>
        <dependency>
            <groupId>org.eclipse.jgit</groupId>
            <artifactId>org.eclipse.jgit.http.server</artifactId>
            <version>${jgit.version}</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>${jjwt.version}</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.bouncycastle</groupId>
            <artifactId>bcprov-jdk18on</artifactId>
            <version>${bouncycastle.version}</version>
        </dependency>
        <dependency>
            <groupId>com.bucket4j</groupId>
            <artifactId>bucket4j-core</artifactId>
            <version>${bucket4j.version}</version>
        </dependency>
        <dependency>
            <groupId>org.commonmark</groupId>
            <artifactId>commonmark</artifactId>
            <version>${commonmark.version}</version>
        </dependency>
        <dependency>
            <groupId>org.commonmark</groupId>
            <artifactId>commonmark-ext-gfm-tables</artifactId>
            <version>${commonmark.version}</version>
        </dependency>
        <dependency>
            <groupId>org.commonmark</groupId>
            <artifactId>commonmark-ext-autolink</artifactId>
            <version>${commonmark.version}</version>
        </dependency>
        <dependency>
            <groupId>org.commonmark</groupId>
            <artifactId>commonmark-ext-task-list-items</artifactId>
            <version>${commonmark.version}</version>
        </dependency>
        <dependency>
            <groupId>org.owasp.encoder</groupId>
            <artifactId>encoder</artifactId>
            <version>1.2.3</version>
        </dependency>
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>${springdoc.version}</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.dataformat</groupId>
            <artifactId>jackson-dataformat-yaml</artifactId>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.datatype</groupId>
            <artifactId>jackson-datatype-jsr310</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>21</source>
                    <target>21</target>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""
w("backend/pom.xml", pom)

app_yml = """server:
  port: 8080
  servlet:
    context-path: /

spring:
  application:
    name: forgehub-backend
  profiles:
    active: dev
  jackson:
    serialization:
      write-dates-as-timestamps: false
      fail-on-empty-beans: false
    default-property-inclusion: non_null

forgehub:
  jwt:
    secret: 404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970
    access-token-expiration-ms: 900000
    refresh-token-expiration-ms: 604800000
    issuer: forgehub-auth
  git:
    storage-root: ./data/git-repositories
    max-file-size-bytes: 10485760
    diff-max-lines: 5000
  storage:
    type: local
    local-root: ./data/uploads
  ci:
    max-concurrent-jobs: 10
    default-timeout-seconds: 1800
    workspace-root: ./data/ci-workspaces
  crypto:
    vault-key: 635266556A586E3272357538782F413F4428472B4B6250645367566B5970404E
  webhook:
    delivery-timeout-ms: 10000
    max-retry-attempts: 5
"""
w("backend/src/main/resources/application.yml", app_yml)

app_dev_yml = """spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:h2:mem:forgehubdb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE;MODE=PostgreSQL
    driverClassName: org.h2.Driver
    username: sa
    password: 
  jpa:
    database-platform: org.hibernate.dialect.H2Dialect
    hibernate:
      ddl-auto: none
    show-sql: false
    properties:
      hibernate:
        format_sql: true
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
  data:
    redis:
      host: localhost
      port: 6379

logging:
  level:
    com.forgehub: DEBUG
    org.springframework.security: INFO
"""
w("backend/src/main/resources/application-dev.yml", app_dev_yml)

app_prod_yml = """spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: jdbc:postgresql://${DB_HOST:localhost}:${DB_PORT:5432}/${DB_NAME:forgehub}
    username: ${DB_USER:forgehub}
    password: ${DB_PASSWORD:forgehub_secure_pass}
    hikari:
      maximum-pool-size: 30
      minimum-idle: 10
      idle-timeout: 30000
      max-lifetime: 1800000
      connection-timeout: 20000
  jpa:
    database-platform: org.hibernate.dialect.PostgreSQLDialect
    hibernate:
      ddl-auto: validate
    show-sql: false
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD:}

logging:
  level:
    com.forgehub: INFO
    org.springframework.security: WARN
"""
w("backend/src/main/resources/application-prod.yml", app_prod_yml)

pkg_json = """{
  "name": "forgehub-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "@monaco-editor/react": "^4.7.0",
    "@stomp/stompjs": "^7.0.0",
    "@tanstack/react-query": "^5.56.2",
    "@tanstack/react-table": "^8.20.5",
    "axios": "^1.7.7",
    "clsx": "^2.1.1",
    "date-fns": "^3.6.0",
    "lucide-react": "^0.441.0",
    "monaco-editor": "^0.51.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-hook-form": "^7.53.0",
    "react-markdown": "^9.0.1",
    "react-router-dom": "^6.26.2",
    "recharts": "^2.12.7",
    "remark-gfm": "^4.0.0",
    "sockjs-client": "^1.6.1",
    "tailwind-merge": "^2.5.2",
    "zod": "^3.23.8",
    "zustand": "^4.5.5"
  },
  "devDependencies": {
    "@types/node": "^22.5.4",
    "@types/react": "^18.3.5",
    "@types/react-dom": "^18.3.0",
    "@types/sockjs-client": "^1.5.4",
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.45",
    "tailwindcss": "^3.4.11",
    "typescript": "^5.5.3",
    "vite": "^5.4.3"
  }
}
"""
w("frontend/package.json", pkg_json)

tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": false,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""
w("frontend/tsconfig.json", tsconfig)

tsconfig_node = """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
"""
w("frontend/tsconfig.node.json", tsconfig_node)

vite_config = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8080',
        ws: true,
      },
    },
  },
});
"""
w("frontend/vite.config.ts", vite_config)

tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        forge: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          950: '#082f49',
        },
        surface: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        }
      }
    },
  },
  plugins: [],
}
"""
w("frontend/tailwind.config.js", tailwind_config)

postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
w("frontend/postcss.config.js", postcss_config)

index_html = """<!doctype html>
<html lang="en" class="dark">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ForgeHub | Enterprise Developer Collaboration Platform</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body class="bg-surface-950 text-slate-100 font-sans antialiased selection:bg-forge-500 selection:text-white min-h-screen">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
w("frontend/index.html", index_html)

gitignore = """target/
node_modules/
dist/
data/
*.class
*.log
.DS_Store
Thumbs.db
.idea/
*.iml
.vscode/
.env
.env.local
"""
w(".gitignore", gitignore)

env_example = """SERVER_PORT=8080
SPRING_PROFILES_ACTIVE=dev
DB_HOST=localhost
DB_PORT=5432
DB_NAME=forgehub
DB_USER=forgehub
DB_PASSWORD=forgehub_secure_pass
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
VAULT_KEY=635266556A586E3272357538782F413F4428472B4B6250645367566B5970404E
GIT_STORAGE_ROOT=./data/git-repositories
UPLOADS_STORAGE_ROOT=./data/uploads
CI_WORKSPACE_ROOT=./data/ci-workspaces
"""
w(".env.example", env_example)

print("Phase 1 Foundation complete.")