# Systemplanung – Pokémon Budget Tracker

**Modul:** M300 – Cloud-Lösungen realisieren
**Datum:** 29. Mai 2026

---

## Inhaltsverzeichnis
1. [Übersicht](#1-übersicht)
2. [Architektur](#2-architektur)
3. [AWS Infrastruktur](#3-aws-infrastruktur)
4. [Netzwerk](#4-netzwerk)
5. [Docker & Container](#5-docker--container)
6. [Datenbank](#6-datenbank)
7. [CI/CD Pipeline](#7-cicd-pipeline)
8. [Monitoring](#8-monitoring)
9. [Logging & Fehleranalyse](#9-logging--fehleranalyse)
10. [Backup & Sicherheit](#10-backup--sicherheit)

---

## 1. Übersicht

Der Pokémon Budget Tracker ist eine cloudbasierte Web-Applikation auf AWS. Sie ermöglicht das Erfassen von Ausgaben und Einnahmen beim Pokémon-Kartensammeln und ruft über die Pokémon TCG API live Marktpreise ab.

| Eigenschaft | Wert |
|-------------|------|
| Cloud-Provider | Amazon Web Services (AWS) |
| Region | eu-central-1 (Frankfurt) |
| Deployment | Docker Container auf EC2 |
| Datenbank | PostgreSQL auf AWS RDS |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |
| Logging | AWS CloudWatch |

---

## 2. Architektur

```
┌─────────────────────────────────────────────────────┐
│                    Internet                          │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS (443)
┌──────────────────────▼──────────────────────────────┐
│                  AWS Cloud                           │
│  ┌─────────────────────────────────────────────┐    │
│  │              VPC (10.0.0.0/16)              │    │
│  │  ┌──────────────────────────────────────┐   │    │
│  │  │         Public Subnet                │   │    │
│  │  │  ┌────────────────────────────────┐  │   │    │
│  │  │  │       EC2 (t2.micro)           │  │   │    │
│  │  │  │  ┌──────────┐  ┌───────────┐  │  │   │    │
│  │  │  │  │ Frontend │  │  Backend  │  │  │   │    │
│  │  │  │  │ (Nginx)  │  │  (Flask)  │  │  │   │    │
│  │  │  │  └──────────┘  └─────┬─────┘  │  │   │    │
│  │  │  │  ┌──────────┐        │        │  │   │    │
│  │  │  │  │Prometheus│  ┌─────▼─────┐  │  │   │    │
│  │  │  │  │+ Grafana │  │    RDS    │  │  │   │    │
│  │  │  │  └──────────┘  │(PostgreSQL│  │  │   │    │
│  │  │  └────────────────┴───────────┴──┘  │   │    │
│  │  └──────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────┘    │
│  ┌──────────┐  ┌─────────────┐                      │
│  │    S3    │  │ CloudWatch  │                      │
│  │(Backups) │  │  (Logging)  │                      │
│  └──────────┘  └─────────────┘                      │
└─────────────────────────────────────────────────────┘

         ▲ Pokémon TCG API (externe API)
```

---

## 3. AWS Infrastruktur

### EC2 – App Server

| Eigenschaft | Wert |
|-------------|------|
| Instance Type | t2.micro (Free Tier) |
| OS | Ubuntu 22.04 LTS |
| Storage | 8 GB gp2 |
| Public IP | Elastische IP (statisch) |
| Region | eu-central-1 |

**Begründung:** t2.micro reicht für eine kleine Web-App, ist kostenlos im Free Tier und einfach zu verwalten.

### RDS – Datenbank

| Eigenschaft | Wert |
|-------------|------|
| Engine | PostgreSQL 15 |
| Instance Type | db.t3.micro (Free Tier) |
| Storage | 20 GB gp2 |
| Multi-AZ | Nein (Entwicklungsumgebung) |
| Backup | Automatisch täglich |

**Begründung:** Managed Service – AWS übernimmt Updates, Backups und Verfügbarkeit automatisch.

### S3 – Backups

| Eigenschaft | Wert |
|-------------|------|
| Bucket Name | pokemon-tracker-backups |
| Versioning | Aktiviert |
| Lifecycle | Backups älter als 30 Tage löschen |

---

## 4. Netzwerk

### VPC Konfiguration

```
VPC: 10.0.0.0/16
│
├── Public Subnet:  10.0.1.0/24  (EC2, Grafana)
└── Private Subnet: 10.0.2.0/24  (RDS)
```

### Security Groups

**EC2 – App Server:**

| Port | Protokoll | Quelle | Zweck |
|------|-----------|--------|-------|
| 22 | TCP | Meine IP | SSH Zugriff |
| 80 | TCP | 0.0.0.0/0 | HTTP |
| 443 | TCP | 0.0.0.0/0 | HTTPS |
| 3000 | TCP | Meine IP | Grafana Dashboard |
| 9090 | TCP | Meine IP | Prometheus |

**RDS – Datenbank:**

| Port | Protokoll | Quelle | Zweck |
|------|-----------|--------|-------|
| 5432 | TCP | EC2 Security Group | PostgreSQL (nur von EC2) |

**Begründung:** RDS ist nicht öffentlich erreichbar – nur der EC2 Server darf auf die Datenbank zugreifen. Das erhöht die Sicherheit deutlich.

---

## 5. Docker & Container

### Containerstruktur

```
docker-compose.yml
│
├── frontend    (Nginx – statische HTML/JS Dateien)
├── backend     (Python Flask – REST API)
├── prometheus  (Metriken sammeln)
└── grafana     (Dashboard & Alerts)
```

### Dockerfile (Backend)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### docker-compose.yml (Struktur)

```yaml
version: '3.8'
services:
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@rds-endpoint/pokemon
    depends_on:
      - prometheus

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

**Begründung:** Docker stellt sicher, dass die App auf jedem System gleich läuft. Mit docker-compose können alle Services mit einem Befehl gestartet werden.

---

## 6. Datenbank

### Schema

```sql
-- Einträge (Käufe & Verkäufe)
CREATE TABLE entries (
    id          SERIAL PRIMARY KEY,
    type        VARCHAR(10) NOT NULL,  -- 'buy', 'sell', 'pack'
    name        VARCHAR(255) NOT NULL,
    amount      DECIMAL(10,2) NOT NULL,
    date        DATE NOT NULL,
    card_id     VARCHAR(50),           -- Pokémon TCG API ID
    market_price DECIMAL(10,2),        -- Live-Preis zum Zeitpunkt
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Portfolio (aktuell gehaltene Karten)
CREATE TABLE portfolio (
    id          SERIAL PRIMARY KEY,
    card_id     VARCHAR(50) NOT NULL,
    name        VARCHAR(255) NOT NULL,
    quantity    INT NOT NULL DEFAULT 1,
    buy_price   DECIMAL(10,2) NOT NULL,
    market_price DECIMAL(10,2),
    set_name    VARCHAR(255),
    updated_at  TIMESTAMP DEFAULT NOW()
);
```

---

## 7. CI/CD Pipeline

### Ablauf

```
Developer pusht Code auf GitHub (main branch)
          │
          ▼
GitHub Actions startet automatisch
          │
          ├── 1. Code auschecken
          ├── 2. Unit-Tests ausführen
          ├── 3. Docker Image bauen
          ├── 4. Image auf Docker Hub pushen
          └── 5. Per SSH auf EC2 deployen
                    │
                    ├── docker pull (neues Image holen)
                    └── docker-compose up -d (neu starten)
```

### GitHub Actions Workflow (`.github/workflows/deploy.yml`)

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run tests
        run: |
          pip install -r backend/requirements.txt
          pytest backend/tests/

      - name: Build & Push Docker Image
        run: |
          docker login -u ${{ secrets.DOCKERHUB_USERNAME }} \
                       -p ${{ secrets.DOCKERHUB_TOKEN }}
          docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/pokemon-tracker .
          docker push ${{ secrets.DOCKERHUB_USERNAME }}/pokemon-tracker

      - name: Deploy to EC2
        run: |
          ssh -o StrictHostKeyChecking=no \
              -i key.pem \
              ubuntu@${{ secrets.EC2_HOST }} \
              'cd /app && docker-compose pull && docker-compose up -d'
```

### GitHub Secrets

| Secret | Inhalt |
|--------|--------|
| `DOCKERHUB_USERNAME` | Docker Hub Benutzername |
| `DOCKERHUB_TOKEN` | Docker Hub Access Token |
| `EC2_HOST` | Öffentliche IP des EC2 Servers |
| `EC2_KEY` | SSH Private Key (.pem Datei) |

---

## 8. Monitoring

### Prometheus

Prometheus sammelt alle 15 Sekunden Metriken vom Backend:

| Metrik | Beschreibung |
|--------|-------------|
| `http_requests_total` | Anzahl API-Anfragen |
| `http_request_duration_seconds` | Antwortzeit der API |
| `process_cpu_seconds_total` | CPU-Verbrauch |
| `process_resident_memory_bytes` | RAM-Verbrauch |

### Grafana Dashboard

Das Dashboard zeigt folgende Panels:

- CPU-Auslastung (%)
- RAM-Verbrauch (MB)
- API-Anfragen pro Minute
- Durchschnittliche Antwortzeit (ms)
- Fehlerrate (HTTP 5xx)

### Alerts

| Alert | Bedingung | Benachrichtigung |
|-------|-----------|-----------------|
| App down | HTTP 200 fehlt > 1 Min | E-Mail |
| CPU hoch | CPU > 80% > 5 Min | E-Mail |
| Disk voll | Disk > 90% | E-Mail |

---

## 9. Logging & Fehleranalyse

### CloudWatch

Alle Logs werden nach AWS CloudWatch gesendet:

| Log-Gruppe | Inhalt |
|------------|--------|
| `/pokemon-tracker/app` | Flask Applikations-Logs |
| `/pokemon-tracker/nginx` | Nginx Access/Error Logs |
| `/pokemon-tracker/system` | System-Logs (journald) |

### Fehler-Kategorisierung

| Kategorie | Beispiel | Priorität |
|-----------|---------|-----------|
| Kritisch | App startet nicht, DB nicht erreichbar | Hoch |
| Warnung | API-Timeout, langsame Antwortzeit | Mittel |
| Info | Erfolgreiche Deployments, neue Einträge | Niedrig |

---

## 10. Backup & Sicherheit

### Backup-Strategie

| Was | Wie | Wann | Aufbewahrung |
|-----|-----|------|-------------|
| RDS Datenbank | Automatischer AWS Snapshot | Täglich 02:00 Uhr | 7 Tage |
| S3 Bucket | Versionierung aktiviert | Bei jeder Änderung | 30 Tage |

### Sicherheitsmassnahmen

- SSH-Zugriff nur mit Key-Pair (kein Passwort-Login)
- RDS nicht öffentlich erreichbar (nur aus VPC)
- Secrets in GitHub Secrets gespeichert (nicht im Code)
- HTTPS mit SSL-Zertifikat (Let's Encrypt)
- Security Groups: nur notwendige Ports offen
- Datenbankpasswort als Umgebungsvariable (nicht hardcoded)

---

*Dokument erstellt: 29. Mai 2026*
*Letzte Aktualisierung: 29. Mai 2026*