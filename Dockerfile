# Multi-stage Root Dockerfile for ForgeHub Full-Stack Platform
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
