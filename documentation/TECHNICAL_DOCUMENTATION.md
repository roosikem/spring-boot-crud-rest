# Spring Boot CRUD REST Application - Technical Documentation

## Project Overview

This is a Spring Boot CRUD REST application built with Java 21.

## Architecture Diagrams


```mermaid
classDiagram
    class AppController {
        -AppService service
        +create(AppDTO) ResponseEntity
        +getAll() ResponseEntity
        +findById(Long) ResponseEntity
        +update(Long, AppDTO) ResponseEntity
        +delete(Long) ResponseEntity
    }

    class AppService {
        <<interface>>
        +createNewApp(AppDTO) Long
        +getAllApps() List~AppDTO~
        +getAppById(Long) AppDTO
        +updateApp(Long, AppDTO) void
        +deleteAppById(Long) void
    }

    class AppServiceImpl {
        -AppRepository repository
        -ModelMapper mapper
        +createNewApp(AppDTO) Long
        +getAllApps() List~AppDTO~
        +getAppById(Long) AppDTO
        +updateApp(Long, AppDTO) void
        +deleteAppById(Long) void
    }

    class AppRepository {
        <<interface>>
    }

    class App {
        -Long id
        -String name
        -String version
        -String author
    }

    class AppDTO {
        -String name
        -String version
        -String author
    }

    AppController --> AppService
    AppService <|.. AppServiceImpl
    AppServiceImpl --> AppRepository
    AppServiceImpl --> App
    AppServiceImpl --> AppDTO
    AppRepository --> App
```


```mermaid
sequenceDiagram
    participant Client
    participant Controller as AppController
    participant Service as AppServiceImpl
    participant Repo as AppRepository
    participant DB as H2 Database

    Client->>Controller: POST /api/v1/apps
    activate Controller
    Controller->>Controller: Validate @Valid AppDTO
    Controller->>Service: createNewApp(AppDTO)
    activate Service
    Service->>Service: Map DTO to Entity
    Service->>Repo: save(App)
    activate Repo
    Repo->>DB: INSERT INTO applications
    DB-->>Repo: Generated ID
    Repo-->>Service: App with ID
    deactivate Repo
    Service-->>Controller: Long appId
    deactivate Service
    Controller-->>Client: 201 Created with Location header
    deactivate Controller
```


```mermaid
graph TB
    subgraph "Presentation Layer"
        A[REST Controllers]
    end

    subgraph "Business Layer"
        B[Service Interface]
        C[Service Implementation]
    end

    subgraph "Persistence Layer"
        D[JPA Repository]
        E[Domain Models]
    end

    subgraph "Database"
        F[(H2 In-Memory DB)]
    end

    A -->|uses| B
    B -->|implemented by| C
    C -->|uses| D
    D -->|manages| E
    D -->|JDBC/JPA| F

    style A fill:#90EE90
    style C fill:#87CEEB
    style D fill:#FFB6C1
    style F fill:#DDA0DD
```


## Project Structure

### Controllers
- `AppController.java` - src/main/java/com/apka/tech/buddy/controller/AppController.java

### Services
- `AppService.java` - src/main/java/com/apka/tech/buddy/service/AppService.java

### Repositories
- `AppRepository.java` - src/main/java/com/apka/tech/buddy/repository/AppRepository.java

### Domain Models


### DTOs


*Note: Set OPENAI_API_KEY environment variable for AI-enhanced documentation*
