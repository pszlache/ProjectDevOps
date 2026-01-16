# Project DevOps – Flask + PostgreSQL + Docker

Projekt demonstracyjny przygotowany w ramach zajęć z DevOps.
Celem projektu było stworzenie kompletnego środowiska aplikacyjnego
z wykorzystaniem konteneryzacji Docker.

---

## Stack technologiczny

- Python 3.12
- Flask
- PostgreSQL 16
- Docker
- Docker Compose
- Nginx (reverse proxy)
- Pytest

---

## Architektura

Projekt składa się z następujących kontenerów:

- **app** – aplikacja Flask
- **db** – baza danych PostgreSQL
- **nginx** – reverse proxy
- **seed_runner** – jednorazowy kontener inicjalizujący dane w bazie

Komunikacja została rozdzielona na dwie sieci:
- `front_net` – dostęp z zewnątrz (Nginx)
- `back_net` – komunikacja backendowa (Flask ↔ PostgreSQL)

---

## Uruchomienie projektu

W katalogu głównym projektu:

```bash
docker compose up --build
