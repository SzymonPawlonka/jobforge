# Zacznij tutaj — JobForge od zera do działającej demonstracji

## 0. Najpierw usuń ryzyko formalne

W wymaganiach jest „realizacja aplikacji w Go (obowiązkowo)”, a ten projekt ma główne API w Pythonie i obowiązkowy, rzeczywiście używany analizator w Go. Zanim zainwestujesz czas w oddanie, uzyskaj od prowadzącego pisemne potwierdzenie, że architektura wieloserwisowa spełnia wymaganie.

Wyślij krótkie pytanie:

> Czy akceptuje Pan/Pani architekturę, w której główne REST API jest w Python/FastAPI, a obowiązkowa usługa wykonawcza w Go działa przez gRPC i jest niezbędna do zakończenia scenariusza biznesowego?

Jeżeli odpowiedź brzmi „nie”, ten projekt trzeba przebudować tak, aby główne API było w Go. Nie próbuj liczyć, że prowadzący „jakoś to uzna” na końcu.

## 1. Zainstaluj narzędzia

Minimum do najprostszej ścieżki:

- Git;
- Docker Desktop (Windows/macOS) albo Docker Engine + Compose (Linux);
- przeglądarka.

Python 3.12 i Go 1.23 są potrzebne tylko do uruchamiania testów poza Dockerem i pracy nad kodem.

Sprawdź:

```bash
git --version
docker --version
docker compose version
```

## 2. Rozpakuj i otwórz projekt

```bash
cd jobforge
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

## 3. Skonfiguruj sekrety

Wygeneruj sekret JWT:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Otwórz `.env` i zmień co najmniej:

```env
JWT_SECRET=WKLEJ_WYGENEROWANY_SEKRET
ADMIN_PASSWORD=TwojeMocneHaslo123!
```

Nie commituj `.env`. Repozytorium zawiera wyłącznie `.env.example`.

## 4. Uruchom całość

```bash
docker compose up --build -d
```

Pierwszy build może potrwać kilka minut. Sprawdź stan:

```bash
docker compose ps
docker compose logs --tail=100 api analyzer db
```

Oczekiwany rezultat: `db`, `analyzer` i `api` działają, a API jest dostępne pod:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`

Gdy API nie działa, nie klikaj losowo. Najpierw przeczytaj błąd:

```bash
docker compose logs -f api
```

## 5. Wykonaj pierwszy pełny scenariusz w Swaggerze

1. `POST /auth/register` — utwórz użytkownika.
2. `POST /auth/login` — pole `username` to adres e-mail.
3. Skopiuj `access_token`.
4. Kliknij **Authorize** i podaj token.
5. `POST /jobs` — utwórz zadanie.
6. Skopiuj `id` zadania.
7. `POST /jobs/{job_id}/file` — wybierz `samples/report.txt`.
8. `POST /jobs/{job_id}/run`.
9. `GET /jobs/{job_id}` — status powinien być `COMPLETED`, a `result` zawierać pięć metryk.
10. `GET /jobs/{job_id}/file` — pobierz oryginalny plik.
11. `GET /stats/me` — pokaż logi/statystyki.

## 6. Pokaż WebSocket

Najprościej z `wscat`:

```bash
npx wscat -c "ws://localhost:8000/ws/jobs/JOB_ID?token=JWT"
```

Po połączeniu zobaczysz obecny status. Utwórz nowe zadanie z plikiem i uruchom analizę. Powinny przyjść komunikaty `RUNNING` i `COMPLETED`.

## 7. Uruchom testy

### Python

Linux/macOS:

```bash
cd services/api-python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

Windows PowerShell:

```powershell
cd services/api-python
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
```

### Go

```bash
cd services/analyzer-go
go test ./...
```

Nie oddawaj projektu, dopóki oba zestawy testów nie przechodzą.

## 8. Postman

Importuj pliki z katalogu `postman/`, wybierz środowisko `JobForge Local` i uruchamiaj requesty po kolei. Przy uploadzie ręcznie wskaż `samples/report.txt`.

## 9. Test wydajnościowy

```bash
pip install -r load-tests/requirements.txt
locust -f load-tests/locustfile.py --host http://localhost:8000
```

Test Locust uruchom w trybie headless zgodnie z poleceniem w README.

## 10. Git i repozytorium

Nie twórz fałszywej historii commitów. To łatwo wykryć i nie dowodzi pracy. Zrób repozytorium teraz, poznaj kod i wprowadzaj prawdziwe zmiany w logicznych krokach:

```bash
git init
git add .
git commit -m "chore: initialize JobForge baseline"
```

Następne commity powinny odpowiadać realnym zmianom: poprawki dokumentacji, dodatkowe testy, konfiguracja deploymentu, wynik Locust, poprawki po review prowadzącego.

## 11. Deployment

Wykonaj dokładnie `docs/DEPLOY_CLOUD_RUN.md`. Najpierw wdrażaj Go Analyzer, potem migrację bazy, na końcu API. Nie wdrażaj przed działającą wersją lokalną.

## 12. Co musisz umieć wyjaśnić na obronie

- dlaczego gRPC jest potrzebne i co się stanie po wyłączeniu Go;
- jak JWT identyfikuje użytkownika i gdzie sprawdzany jest właściciel zadania;
- dlaczego plik ma limit 1 MiB i jest przechowywany w `BYTEA`;
- jak status przechodzi przez `RUNNING`, `COMPLETED` i `FAILED`;
- dlaczego WebSocket w pamięci wymaga jednej instancji API;
- czym różnią się REST, WebSocket i gRPC w tym projekcie;
- co robi Alembic i dlaczego nie używamy `create_all()` w produkcji;
- jak testy udowadniają brak dostępu do cudzego zadania.

Jeżeli nie potrafisz odpowiedzieć na te pytania, projekt nie jest jeszcze „Twój”, nawet gdy kod działa.

