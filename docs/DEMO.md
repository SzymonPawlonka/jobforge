# Scenariusz demonstracji JobForge

Przećwicz go co najmniej dwa razy przed oddaniem. Nie improwizuj na prezentacji.

## Przygotowanie

```bash
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

Wszystkie trzy usługi powinny być zdrowe.

## Przebieg

1. Otwórz Swagger UI pod `/docs`.
2. Zarejestruj użytkownika.
3. Zaloguj się i autoryzuj Swaggera tokenem.
4. Pokaż `/users/me`.
5. Utwórz zadanie `Analiza raportu`.
6. Pokaż listę i szczegóły.
7. Zmień nazwę zadania.
8. Prześlij `samples/report.txt`.
9. Pobierz plik i pokaż zgodność zawartości.
10. Otwórz WebSocket:

```bash
npx wscat -c "ws://localhost:8000/ws/jobs/JOB_ID?token=JWT"
```

11. Uruchom analizę.
12. Pokaż komunikaty `RUNNING` i `COMPLETED`.
13. Pokaż wynik: rozmiar, znaki, słowa, linie i SHA-256.
14. Pokaż `/stats/me`.
15. Zaloguj się jako administrator i pokaż `/stats/admin`.
16. Uruchom testy Python i Go.
17. Pokaż kolekcję Postman i raport Locust.
18. Usuń zadanie, potem pokaż `404` przy ponownym odczycie.

## Dowód, że Go nie jest atrapą

1. Utwórz drugie zadanie i prześlij plik.
2. Zatrzymaj analizator:

```bash
docker compose stop analyzer
```

3. Uruchom analizę — status powinien przejść do `FAILED`, a `error_message` zawierać błąd gRPC.
4. Uruchom analizator ponownie:

```bash
docker compose start analyzer
```

5. Utwórz kolejne zadanie i pokaż prawidłowy wynik.

Nie próbuj ponawiać zadania `FAILED` bez świadomego wyjaśnienia zachowania. W tej wersji ponowne uruchomienie jest dozwolone, o ile zadanie nie ma statusu `RUNNING`.
