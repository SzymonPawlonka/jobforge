# Deployment na Google Cloud Run

Ta instrukcja zakłada projekt Google Cloud, zainstalowane `gcloud` i gotową bazę PostgreSQL dostępną z Cloud Run. Najprostsza ścieżka studencka to zewnętrzny zarządzany PostgreSQL z wymuszonym TLS. Cloud SQL jest poprawny, ale wymaga dodatkowej konfiguracji sieci lub konektora.

## 1. Zmienne

```bash
export PROJECT_ID="twoj-projekt"
export REGION="europe-central2"
export REPO="jobforge"
gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

## 2. Artifact Registry

```bash
gcloud artifacts repositories create "$REPO" \
  --repository-format=docker \
  --location="$REGION"
gcloud auth configure-docker "$REGION-docker.pkg.dev"
```

## 3. Zbuduj i wypchnij analizator Go

```bash
export ANALYZER_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/analyzer:latest"
gcloud builds submit services/analyzer-go --tag "$ANALYZER_IMAGE"
```

Wdróż gRPC z HTTP/2 end-to-end i portem 8080. Cloud Run ustawia zmienną `PORT`; serwer Go ją respektuje.

```bash
gcloud run deploy jobforge-analyzer \
  --image "$ANALYZER_IMAGE" \
  --region "$REGION" \
  --platform managed \
  --port 8080 \
  --use-http2 \
  --allow-unauthenticated \
  --set-env-vars ANALYZER_MAX_FILE_BYTES=1048576
```

Dla projektu zaliczeniowego `--allow-unauthenticated` upraszcza klienta gRPC. W wersji produkcyjnej zabezpiecz usługę IAM i dodaj token tożsamości w kliencie.

Zapisz host bez `https://`:

```bash
export ANALYZER_URL=$(gcloud run services describe jobforge-analyzer --region "$REGION" --format='value(status.url)')
export ANALYZER_HOST=${ANALYZER_URL#https://}
echo "$ANALYZER_HOST:443"
```

## 4. Zbuduj i wypchnij API

```bash
export API_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/api:latest"
gcloud builds submit services/api-python --tag "$API_IMAGE"
```

## 5. Migracja bazy

Najbezpieczniej uruchomić migrację lokalnie przeciwko chmurowej bazie albo utworzyć Cloud Run Job z tym samym obrazem. Lokalnie:

```bash
cd services/api-python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='postgresql+psycopg://USER:PASSWORD@HOST:5432/DB?sslmode=require'
alembic upgrade head
python -m app.scripts.create_admin
```

## 6. Wdróż API

Wygeneruj sekret:

```bash
export JWT_SECRET=$(python -c 'import secrets; print(secrets.token_urlsafe(48))')
```

Wdróż API. Nie używaj `--use-http2`, ponieważ ta usługa obsługuje WebSockety. Ustaw jedną instancję na demonstrację, bo połączenia są przechowywane w pamięci procesu.

```bash
gcloud run deploy jobforge-api \
  --image "$API_IMAGE" \
  --region "$REGION" \
  --platform managed \
  --port 8000 \
  --allow-unauthenticated \
  --max-instances 1 \
  --timeout 3600 \
  --set-env-vars "DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DB?sslmode=require,JWT_SECRET=$JWT_SECRET,GRPC_TARGET=$ANALYZER_HOST:443,GRPC_TLS=true,GRPC_TIMEOUT_SECONDS=10,CORS_ORIGINS=*"
```

Uwaga: hasła w `--set-env-vars` trafiają do konfiguracji rewizji. Lepsza wersja używa Secret Manager. Na zaliczenie możesz użyć konsoli Cloud Run do ustawienia sekretów, ale nie commituj ich do Git.

## 7. Weryfikacja

```bash
export API_URL=$(gcloud run services describe jobforge-api --region "$REGION" --format='value(status.url)')
curl "$API_URL/health"
echo "$API_URL/docs"
```

Wykonaj pełny scenariusz ze Swaggera. WebSocket używa `wss://`:

```bash
npx wscat -c "${API_URL/https:/wss:}/ws/jobs/JOB_ID?token=JWT"
```

## Typowe awarie

- `UNAVAILABLE` z gRPC: sprawdź `GRPC_TARGET`, port `443`, `GRPC_TLS=true` i czy analizator wdrożono z `--use-http2`.
- WebSocket rozłącza się po kilku minutach: zwiększ timeout usługi API i zadbaj o reconnect klienta.
- API nie łączy się z bazą: sprawdź allowlistę IP/VPC, `sslmode=require` i poprawność sterownika `postgresql+psycopg`.
- Migracje nie wykonały się: Cloud Run nie uruchamia Alembic automatycznie w tym wariancie; wykonaj krok 5.
