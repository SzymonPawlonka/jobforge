# Test wydajnoœciowy JobForge

Data: 2026-07-08

## Konfiguracja

- Narzêdzie: Locust 2.44.4
- U¿ytkownicy: 10
- Tempo uruchamiania: 2 u¿ytkowników/s
- Czas testu: 1 minuta
- Host: http://localhost:8000

## Scenariusz

Ka¿dy u¿ytkownik:
1. rejestrowa³ konto,
2. logowa³ siê,
3. tworzy³ zadanie pocz¹tkowe,
4. wykonywa³ GET /jobs,
5. wykonywa³ GET /jobs/{id},
6. okresowo wykonywa³ POST /jobs.

## Wyniki

- £¹czna liczba ¿¹dañ: 478
- Liczba b³êdów: 0
- RPS: 8.09
- Œredni czas odpowiedzi: 34 ms
- Mediana: 26 ms
- p95: 89 ms
- Maksymalny czas odpowiedzi: 182 ms

## Wnioski

Test zakoñczy³ siê bez b³êdów. Dla 10 równoczesnych u¿ytkowników lokalna instancja JobForge obs³u¿y³a wszystkie ¿¹dania poprawnie. Najwolniejsz¹ operacj¹ by³a rejestracja u¿ytkownika, natomiast odczyt zadañ pozostawa³ poni¿ej oko³o 100 ms w zdecydowanej wiêkszoœci przypadków.
