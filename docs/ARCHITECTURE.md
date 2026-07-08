# Architektura

## Przepływ analizy

```text
POST /jobs/{id}/run
        |
        v
FastAPI: walidacja właściciela i pliku
        |
        v
status RUNNING + commit + WebSocket
        |
        v
Go gRPC AnalyzeFile(filename, content)
        |
        +---- sukces ----> result JSON + COMPLETED + WebSocket
        |
        +---- błąd ------> error_message + FAILED + WebSocket
```

## Model danych

```mermaid
erDiagram
    USERS ||--o{ JOBS : owns
    USERS ||--o{ API_REQUEST_LOGS : creates
    JOBS ||--o| FILES : has

    USERS {
      uuid id PK
      varchar email UK
      varchar password_hash
      varchar role
      timestamp created_at
    }
    JOBS {
      uuid id PK
      uuid user_id FK
      varchar name
      varchar status
      json result
      text error_message
      timestamp created_at
      timestamp updated_at
    }
    FILES {
      uuid id PK
      uuid job_id FK,UK
      varchar filename
      varchar content_type
      integer size_bytes
      bytea data
      timestamp created_at
    }
    API_REQUEST_LOGS {
      uuid id PK
      uuid user_id FK
      varchar method
      varchar path
      integer status_code
      float duration_ms
      timestamp created_at
    }
```

## Decyzje techniczne

- SQLAlchemy używa typów przenośnych `Uuid`, `JSON` i `LargeBinary`, które poprawnie mapują się na PostgreSQL i pozwalają uruchamiać szybkie testy na SQLite.
- Logi API są zapisywane w oddzielnej sesji po zakończeniu odpowiedzi. Awaria mechanizmu logowania nie psuje odpowiedzi biznesowej.
- Token WebSocket jest przekazywany w query string, ponieważ przeglądarkowy API WebSocket nie pozwala swobodnie ustawiać nagłówka `Authorization`.
- Manager WebSocket działa w pamięci procesu. To poprawne dla jednej instancji demonstracyjnej, ale nie dla skalowania poziomego.
- Analiza gRPC ma timeout i nie wykonuje automatycznych retry, aby uniknąć ukrywania awarii podczas demonstracji.
