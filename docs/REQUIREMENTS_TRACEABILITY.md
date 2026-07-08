# Macierz wymagań i dowodów

Ta tabela nie zastępuje demonstracji. Pokazuje, gdzie znajduje się implementacja i jaki dowód należy przedstawić.

| Wymaganie | Implementacja | Dowód na prezentacji |
|---|---|---|
| Projekt REST API | `app/routers/`, `app/schemas.py` | Swagger `/docs` |
| Swagger/OpenAPI | FastAPI `app/main.py` | `/docs`, `/openapi.json` |
| PostgreSQL i projekt bazy | `app/models.py`, `alembic/versions/0001_initial.py` | migracja + tabele |
| CRUD zadań | `app/routers/jobs.py` | POST, GET, PATCH, DELETE |
| Go obowiązkowo | `services/analyzer-go/` | wynik analizy i awaria po zatrzymaniu Go |
| gRPC | `proto/analyzer.proto`, klient Python, serwer Go | `POST /jobs/{id}/run` |
| JWT | `app/security.py`, `app/deps.py` | logowanie, Authorize, 401/404 |
| Role USER/ADMIN | `require_admin`, `/stats/admin` | USER dostaje 403, ADMIN 200 |
| Upload/download | `app/routers/files.py` | upload i pobranie tego samego pliku |
| Limit i typ pliku | walidacja `.txt/.csv/.json`, 1 MiB | próba `.exe` lub >1 MiB |
| WebSocket | `app/routers/websocket.py`, manager | `RUNNING`, `COMPLETED` |
| Logi API | `app/middleware.py` | rekordy i `/stats/me` |
| Statystyki | `app/routers/stats.py` | `/stats/me`, `/stats/admin` |
| Testy Python | `services/api-python/tests/` | `pytest -q` |
| Test Go | `internal/analyzer/analyzer_test.go` | `go test ./...` |
| Postman | `postman/` | uruchomiona kolekcja |
| Locust | `load-tests/`, `docs/performance.md` | raport z prawdziwymi wynikami |
| Docker | oba Dockerfile, `docker-compose.yml` | `docker compose ps` |
| HTTPS/deploy | `docs/DEPLOY_CLOUD_RUN.md` | publiczny adres Cloud Run |
| VCS | repozytorium Git | prawdziwe, logiczne commity |
| README | `README.md`, `START_HERE.md` | uruchomienie na czystym środowisku |

## Krytyczna próba odbiorowa

Projekt jest gotowy dopiero wtedy, gdy na czystej bazie możesz bez ręcznej edycji rekordów wykonać:

```text
register -> login -> create job -> upload -> WebSocket -> run
-> gRPC Go -> COMPLETED -> result -> download -> stats -> delete
```

Następnie zatrzymaj Go i pokaż kontrolowane `FAILED`. Brak tego dowodu osłabia argument, że Go jest niezbędną częścią systemu.
