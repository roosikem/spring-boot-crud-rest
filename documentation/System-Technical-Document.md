# System Technical Document

## 1. System Overview

### Business context
This repository implements a sample CRUD REST application named `spring-boot-crud-rest`. The likely business context is to demonstrate a small service that manages a catalog of applications (apps) with metadata such as name, version, and author. It's suitable as a learning project, demo, or template for building simple Spring Boot-backed REST services.

### High-level description
The system is a Spring Boot (Java) application exposing a RESTful API for managing "App" entities. It persists data using Spring Data JPA with an embedded H2 database (runtime). The application populates the database with sample data on startup and provides endpoints to create, read, update, and delete apps.

### Primary stakeholders and consumers
- Developers using the project as a demo or template.
- QA engineers running integration tests included in the repo.
- Potentially clients or services that consume the REST API (e.g., frontend apps or other backend services), although no client code is included.

## 2. Domain & Bounded Contexts

### Domains / bounded contexts
Based on the code, the system fits into a single domain: "Application Catalog" — responsible for CRUD operations on software application metadata. There are no multiple services or microservice boundaries visible in the repository.

### Module mapping
- Controller: `com.apka.tech.buddy.controller.AppController` — API layer / HTTP interface
- Service: `com.apka.tech.buddy.service.*` (interface and `impl.AppServiceImpl`) — business logic
- Repository: `com.apka.tech.buddy.repository.AppRepository` — persistence layer (Spring Data JPA)
- Model / DTO: `com.apka.tech.buddy.model.domain.App` and `com.apka.tech.buddy.model.dto.AppDTO` — domain model and transfer objects
- Builder / mapping: `com.apka.tech.buddy.builder.AppBuilder` and `org.modelmapper.ModelMapper` bean — mapping between domain and DTO
- Config: `com.apka.tech.buddy.config.AppConfig` — application configuration (ModelMapper bean)

## 3. Architecture Overview

### Overall style
- Modular monolith / layered architecture typical of small Spring Boot applications: controller -> service -> repository -> database.
- No distributed microservices visible; everything runs within a single Spring Boot process.

### Module interactions
- HTTP clients call REST endpoints in `AppController`.
- `AppController` delegates to `AppService` (interface) for operations.
- `AppServiceImpl` uses `AppRepository` to persist `App` entities and `AppBuilder` to map to/from `AppDTO`.
- `AppConfig` provides a shared `ModelMapper` bean used by `AppBuilder`.
- `CRUDRestApplication` bootstraps the app and populates sample data via `AppService.populate()`.

### Synchronous vs asynchronous communication
- All interactions are synchronous HTTP request/response flows using Spring MVC. No asynchronous messaging or background queues are present.

### External systems / integrations
- Embedded/runtime H2 database (declared dependency) for persistence.
- No external APIs, message brokers, cloud services, or third-party integrations other than libraries (ModelMapper, JavaFaker).

## 4. Module / Service Catalog

### AppController (com.apka.tech.buddy.controller.AppController)
- Responsibilities: Expose REST endpoints for Apps (CRUD) and map HTTP semantics (status codes, Location header on create).
- Key APIs / entry points:
  - POST /api/v1/apps — create new app (returns 201 Created and Location header)
  - GET /api/v1/apps — list all apps
  - GET /api/v1/apps/{id} — retrieve single app
  - PUT /api/v1/apps/{id} — update app (returns 204 No Content)
  - DELETE /api/v1/apps/{id} — delete app
- Data read/write: Accepts `AppDTO` in request bodies; returns `AppDTO` or lists of `AppDTO` in responses.
- Dependencies: `AppService`.

### AppService / AppServiceImpl (com.apka.tech.buddy.service)
- Responsibilities: Business logic for CRUD operations, population of sample data.
- Key APIs:
  - Long createNewApp(AppDTO dto)
  - List<Optional<AppDTO>> getAllApps()
  - Optional<AppDTO> getAppById(Long id)
  - Optional<AppDTO> updateApp(Long id, AppDTO dto)
  - void deleteAppById(Long id)
  - void populate()
- Data read/write: Reads/writes `App` entities via `AppRepository` and transforms to/from `AppDTO` using `AppBuilder`.
- Dependencies: `AppRepository`, `AppBuilder`, `Faker` for sample data.

### AppRepository (com.apka.tech.buddy.repository.AppRepository)
- Responsibilities: JPA repository for `App` entities.
- Key APIs: Inherits CRUD operations from JpaRepository<App, Long> (save, findById, findAll, deleteById, etc.).
- Data read/write: `App` JPA entities persisted to H2 database.
- Dependencies: Spring Data JPA

### App (com.apka.tech.buddy.model.domain.App)
- Responsibilities: JPA entity representing an application record.
- Key fields: id (Long, @GeneratedValue), author (String), name (String), version (String)

### AppDTO (com.apka.tech.buddy.model.dto.AppDTO)
- Responsibilities: HTTP transfer object with validation constraints.
- Key fields: name (appName, max 20 chars), version (appVersion), author (devName)
- Validation: `@NotEmpty` for all fields, `@Size(max=20)` for `name`.

### AppBuilder (com.apka.tech.buddy.builder.AppBuilder)
- Responsibilities: Map between `AppDTO` and `App` domain model using `ModelMapper`.
- Key methods: build(AppDTO) -> App, build(App) -> Optional<AppDTO>, build(AppDTO, App) -> App

### AppConfig (com.apka.tech.buddy.config.AppConfig)
- Responsibilities: Spring configuration; provides a `ModelMapper` bean configured to skip null properties during mapping.

### CRUDRestApplication (com.apka.tech.buddy.application.CRUDRestApplication)
- Responsibilities: Spring Boot application entrypoint. Implements CommandLineRunner to call `service.populate()` on startup, seeding the database with sample data.

## 5. Key Flows

### Flow 1 — Create App (POST /api/v1/apps)
1. Client sends POST with JSON body matching `AppDTO` (fields: appName, appVersion, devName).
2. `AppController.create()` validates the DTO (`@Valid`) and calls `service.createNewApp(dto)`.
3. `AppServiceImpl.createNewApp()` maps DTO to `App` using `AppBuilder.build(dto)`, saves to `AppRepository.save(app)`, and returns the generated id.
4. Controller builds Location header `/api/v1/apps/{id}` and returns HTTP 201 Created with Location header.

Error handling: Validation failures return standard Spring MVC validation errors (400). If repository save fails, exceptions bubble up (no custom error handling beyond tests expecting standard 404 for not found on read/update).

### Flow 2 — Read App (GET /api/v1/apps/{id})
1. Client sends GET with id.
2. `AppController.findById(id)` calls `service.getAppById(id)`.
3. `AppServiceImpl.getAppById()` uses `repository.findById(id)` and maps domain to DTO using `AppBuilder.build(domain)`. If not found, it throws `AppNotFoundException` annotated with `@ResponseStatus(HttpStatus.NOT_FOUND)`.
4. Controller returns HTTP 200 with AppDTO or 404 if exception thrown.

Error handling: `AppNotFoundException` produces a 404 response.

### Flow 3 — Update App (PUT /api/v1/apps/{id})
1. Client sends PUT with DTO.
2. `AppController.update()` calls `service.updateApp(id, dto)`.
3. `AppServiceImpl.updateApp()` finds entity by id, maps DTO -> existing domain via `builder.build(dto, domain)`, saves, and returns updated DTO.
4. Controller returns HTTP 204 No Content on success.

Error handling: If id not found, `AppServiceImpl` throws `AppNotFoundException` -> 404.

## 6. Data & Persistence

### Main data store
- H2 (in-memory or file-based depending on runtime configuration). Declared dependency and H2 console enabled in `application.yml`.
- JPA/Hibernate used via Spring Data JPA.

### Important entities
- App (table name: `applications`) with columns: id (PK), author, name, version.

### Relationships
- Single entity model; no relationships to other entities present.

## 7. Cross-Cutting Concerns

### Authentication & Authorization
- No authentication or authorization is implemented in the code. Endpoints are public by default. If required, security would need to be added (Spring Security) — this is an assumption based on the absence of security-related dependencies or config.

### Logging, tracing, auditing
- No explicit logging/tracing/auditing code present. The project relies on default Spring Boot logging. Tests and classes contain no custom log statements.

### Configuration management
- `application.yml` used for Spring JPA and H2 console settings. The `pom.xml` and `AppConfig` provide bean configuration for `ModelMapper`.

### Caching, performance
- No caching layer present. Repository operations use JPA; Hibernate DDL auto-update is enabled (`ddl-auto: update`). For larger datasets, consider indexing and pagination (not present currently).

## 8. Operational Aspects

### Deployment assumptions
- The project is a standard Spring Boot application packaged as a JAR using `spring-boot-maven-plugin`. It can run as a standalone process.
- Reasonable assumptions: packaged as container-friendly JAR and can be dockerized, but no Dockerfile provided in the repo (assumption).

### Environments
- No environment-specific profiles detected in the code. Typical setup would include dev/test/prod profiles; currently the app uses H2 and is suitable for dev/test. Production would require switching to a production-grade RDBMS and adding externalized configuration.

### Monitoring & alerting
- No monitoring/alerting hooks are present. For production, recommend adding actuator, metrics (Micrometer), and expose endpoints for health and metrics.

## 9. Risks, Constraints & Tech Debt

### Observed assumptions and constraints
- In-memory H2 DB used by default: not production-ready. `ddl-auto: update` on startup can be dangerous for schema changes in production.
- No security: endpoints are unprotected.
- No pagination or filtering on list endpoints — `getAll` returns all records which may be problematic with large datasets.

### Likely tech debt areas
- Lack of API versioning beyond the single `/api/v1/` prefix.
- No error handling middleware (global exception handlers) beyond `@ResponseStatus` on `AppNotFoundException`.
- No logging/tracing or observability integrations.
- DTOs and domain mapping rely on ModelMapper generic behavior — edge cases might require explicit mapping.

### Suggestions for improvements
- Add Spring Security for authentication/authorization and integrate with OAuth2/OIDC for orgs.
- Add pagination (Pageable) to `getAll` and index fields in DB.
- Add global exception handler (ControllerAdvice) for structured error responses.
- Add Spring Boot Actuator and Micrometer for monitoring.
- Externalize datasource configuration and support production RDBMS.

## 10. Assumptions
- This document is created solely from the contents of the repository and the included tests. Any mention of deployment patterns, production-readiness, or missing features are inferred and marked as assumptions.


---

Generated on 2025-11-19 based on repository state.

