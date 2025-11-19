# System Context & Container Diagrams

Task receipt
------------
I'll identify the main modules, external clients/dependencies, communication paths, and generate two Mermaid diagrams (System Context and Container/Service). The document is based only on the repository contents; I call out reasonable assumptions explicitly.

Checklist
---------
- [x] Identify main modules/services
- [x] Identify external clients and dependencies
- [x] Describe key communication paths
- [x] Produce System Context (Mermaid flowchart TD)
- [x] Produce Container / Service diagram (Mermaid flowchart LR)
- [x] Add Architect's Notes with inferences, coupling and risks

Notes on source of truth
------------------------
All information below is inferred from the repository code and config (notably: `pom.xml`, `src/main/java/...`, `src/main/resources/application.yml`, and tests). Where the repo does not provide explicit configuration (deployment, auth, external clients), I mark reasonable assumptions.

1) Main modules / services
---------------------------
- Application entry: `com.apka.tech.buddy.application.CRUDRestApplication` (Spring Boot main + CommandLineRunner)
- HTTP / API layer: `com.apka.tech.buddy.controller.AppController`
- Business logic: `com.apka.tech.buddy.service.AppService` and `com.apka.tech.buddy.service.impl.AppServiceImpl`
- Persistence/repository: `com.apka.tech.buddy.repository.AppRepository` (Spring Data JPA)
- Domain model: `com.apka.tech.buddy.model.domain.App`
- DTOs: `com.apka.tech.buddy.model.dto.AppDTO`
- Mapping / Builder: `com.apka.tech.buddy.builder.AppBuilder` backed by `ModelMapper` (bean in `AppConfig`)
- Configuration: `com.apka.tech.buddy.config.AppConfig`
- Exception: `com.apka.tech.buddy.exception.AppNotFoundException`
- Tests / tooling: integration tests use `TestRestTemplate`; controller tests use `MockMvc`.

2) External clients / consumers
-------------------------------
Inferred primary consumers:
- REST API clients (generic): front-end web apps, mobile apps, or other backend services calling the REST endpoints under `/api/v1/apps`.
- Test clients: the project includes integration tests (`TestRestTemplate`) and unit/controller tests (`MockMvc`) that act as automated clients.

Assumption: No UI code is present in this repo, so any web/mobile client is external.

3) External dependencies
------------------------
Direct/external dependencies visible in the repository:
- Database: H2 (runtime dependency; H2 console enabled via `application.yml`).
- Libraries: Spring Boot (web, data-jpa, validation), ModelMapper, JavaFaker (data seeding), Lombok (compile-time), JUnit + Mockito (tests).
- No message queues, external 3rd-party APIs, or cloud services are referenced in source code.

4) Key communication paths
--------------------------
- HTTP client -> AppController (REST endpoints: POST, GET, PUT, DELETE under `/api/v1/apps`)
- AppController -> AppService (service layer, business logic)
- AppServiceImpl -> AppRepository (JPA persistence, save/findAll/findById/deleteById)
- AppRepository -> H2 database (JDBC via Spring Data JPA / Hibernate)
- CRUDRestApplication (CommandLineRunner) -> AppService.populate() -> repository.save() (startup data seeding)
- AppBuilder <-> ModelMapper (mapping DTO <-> domain)

Mermaid Diagram A — System Context
----------------------------------
This diagram shows primary external users/clients and the system with its main external integration (H2 DB).

```mermaid
flowchart TD
  A[External Client\n(web/mobile/other)] -->|HTTP REST| S[Spring Boot CRUD REST Service]
  A2[Automated Tests\n(MockMvc / TestRestTemplate)] -->|HTTP REST| S
  S -->|JPA/Hibernate| DB[(H2 Database)]
  S -->|uses| LIBS[ModelMapper, JavaFaker, Lombok]
  note right of S
    Core responsibilities:
    - Expose /api/v1/apps
    - CRUD operations on App entity
    - Seed data at startup
  end
```

Mermaid Diagram B — Container / Service Diagram
-----------------------------------------------
This diagram breaks the application into logical containers/modules and shows data flows.

```mermaid
flowchart LR
  subgraph ClientLayer
    C[Client (web/mobile/other)]
    TI[Integration Tests]
  end

  subgraph AppContainer[Spring Boot Application]
    direction TB
    Controller[AppController\n(REST endpoints /api/v1/apps)]
    Service[AppServiceImpl\n(Business logic)]
    Builder[AppBuilder\n(ModelMapper mapping)]
    Repo[AppRepository\n(JPA Repository)]
    Model[App (JPA Entity)]
    Config[AppConfig\n(ModelMapper bean)]
    Starter[CRUDRestApplication\n(CommandLineRunner -> populate())]
  end

  DB[(H2 Database)]

  C -->|HTTP JSON| Controller
  TI -->|HTTP JSON| Controller
  Controller -->|calls| Service
  Service -->|maps| Builder
  Builder -->|uses| Config
  Service -->|persists/queries| Repo
  Repo -->|read/write| DB
  Starter -->|on start calls| Service
  Config -->|provides| Builder

  classDef ext fill:#f9f,stroke:#333,stroke-width:1px;
  classDef core fill:#bbf,stroke:#333,stroke-width:1px;
  class C,TI ext;
  class Controller,Service,Repo,Builder,Model,Config,Starter core;
```

Architect's Notes
-----------------
Key design decisions inferred
- Layered architecture: controller -> service -> repository is explicit and follows conventional Spring Boot patterns.
- ModelMapper is used to decouple DTOs from domain entities, handled centrally via `AppBuilder` and `AppConfig`.
- The app seeds sample data on startup (100 fake apps) using JavaFaker; useful for demos and local development.

Coupling and hotspots
- Tightly coupled:
  - Service and Repository: `AppServiceImpl` directly depends on Spring Data JPA repository methods and domain model; changes to persistence model will affect service logic.
  - Controller and Service API shape: controller relies on service interface returning DTO wrappers; breaking API changes will propagate to clients.
- Loosely coupled:
  - Mapping layer (`AppBuilder`) isolates mapping concerns — swapping ModelMapper or adjusting mappings is localized.
  - Configuration (`AppConfig`) centralizes ModelMapper configuration.

Potential risks and areas of improvement
- Data volume: `getAll` returns all rows (no pagination). In production this can be a performance issue.
- Persistence: `ddl-auto: update` is enabled; this is convenient for development but risky for production schema management.
- Security: no authentication/authorization (no Spring Security dependency) — endpoints are open unless protected by external infra.
- Observability: no Actuator/Metrics/Tracing integrated; production monitoring would need to be added.
- Error handling: limited global error handling; `AppNotFoundException` maps to 404 but other errors will return default server errors.

Assumptions
-----------
- The H2 dependency indicates a development-friendly default; production usage would require a configurable external RDBMS.
- No CI/CD or containerization artifacts are present in the repository; assume this project is intended as a demo/local-run service.

Next steps I can take
---------------------
- Add a README snippet to run the application locally (Maven commands) and how to access H2 console.
- Add a simple Dockerfile and `docker-compose.yml` swapping H2 for Postgres for a production-like setup.
- Generate PlantUML or more detailed sequence diagrams for the key flows.


---

Document created and saved to `documentation/System-Context-and-Containers.md`.

