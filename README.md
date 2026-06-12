# m300

# Pokémon Budget Tracker – Modul 300

## Projektidee
Ein cloudbasierter Pokémon Budget Tracker, der meine Ausgaben und Einnahmen beim Kartensammeln verfolgt. Die App ruft über die Pokémon TCG API live Marktpreise ab und zeigt meinen aktuellen Profit oder Verlust.

## Dokumentation
- [Projektbeschreibung](Dokumentation/README.md)

## Lernjournal
- [Lernjournal Übersicht](Lernjournal/README.md)

## Variante
V2 – Eigenes Projekt

## Technologien
- **Docker** – Containerisierung der Applikation
- **AWS EC2** – Cloud-Server für die App
- **AWS RDS (PostgreSQL)** – Datenbank
- **AWS S3** – Backups
- **GitHub Actions** – CI/CD Pipeline (automatisches Deployment)
- **Prometheus + Grafana** – Monitoring und Alerts
- **CloudWatch** – Logging und Fehleranalyse
- **Pokémon TCG API** – Live-Marktpreise

## Abgedeckte Kompetenzen
| Code | Thema | Umsetzung |
|------|-------|-----------|
| A1 | Services ermitteln | AWS-Services analysieren und begründen |
| B1 | Integrationskonzept | Architekturdiagramm, Netzwerkdesign, CI/CD-Plan |
| C1 | Konfiguration & Monitoring | EC2, RDS, Docker, Prometheus konfigurieren |
| D1 | Netzwerkverbindungen | VPC, Security Groups, HTTPS einrichten |
| E1 | Service-Integration | GitHub Actions Pipeline, Pokémon TCG API |
| E2 | Betrieb & Überwachung | Grafana Dashboard, Alerts, Backups |
| F1 | Fehleranalyse | CloudWatch Logs dokumentieren und analysieren |
| I1 | Dokumentation | Architektur-, Netzwerk- und CI/CD-Diagramme |

## Zeitplan
| Woche | Inhalt |
|-------|--------|
| 1 | GitHub Repo, Ordnerstruktur, App lokal mit Docker |
| 2 | AWS EC2 aufsetzen, App manuell deployen |
| 3 | GitHub Actions CI/CD Pipeline |
| 4 | Prometheus + Grafana Monitoring |
| 5 | CloudWatch Logging, S3 Backups |
| 6 | Dokumentation, Lernjournal abschliessen |

## Arbeitstechnik
- Wöchentliches Lernjournal in `docs/lernjournal/`
- Alle Entscheidungen werden mit Begründung dokumentiert
- Eigenes Vorgehen wird wöchentlich reflektiert

---

# Lernjournal – Woche 3

**Datum:** 5. Juni 2026
**Modul:** M300 – Cloud-Lösungen realisieren

---

## Was habe ich gemacht?
- Backend mit Python Flask und MySQL aufgesetzt
- Dockerfile, docker-compose.yml, nginx.conf und prometheus.yml erstellt
- Datenbankschema mit init.sql und Foreign Keys definiert (cards, entries, portfolio)
- Frontend (index.html) mit Pokémon TCG API verbunden
- App lokal mit Docker zum Laufen gebracht (`docker-compose up --build`)
- App erfolgreich auf `http://localhost` geöffnet und getestet

## Was habe ich gelernt?
- Wie docker-compose mehrere Services gleichzeitig startet (MySQL, Flask, Nginx, Prometheus, Grafana)
- Wie ein Dockerfile aufgebaut ist
- Warum eine separate `init.sql` besser ist als Tabellen im Python-Code zu erstellen
- Wie Foreign Keys in MySQL funktionieren (cards → entries, cards → portfolio)
- Wie Nginx als Reverse Proxy funktioniert (Port 80 → Backend weiterleiten)
- Wie Docker Volumes funktionieren (Daten bleiben gespeichert auch nach Neustart)

## Was war schwierig?
- Docker Desktop war nicht gestartet – App konnte nicht gebaut werden
- Der `backend` Ordner fehlte beim ersten `docker-compose up --build`
- Die Ordnerstruktur musste zuerst korrekt angelegt werden bevor Docker funktionierte

## Nächste Woche
AWS EC2 Instanz starten, App auf den Server deployen und GitHub Actions CI/CD Pipeline einrichten.

---

# Lernjournal – Woche 3

**Datum:** 12. Juni 2026
**Modul:** M300 – Cloud-Lösungen realisieren

---

## Was habe ich gemacht?
- Per SSH mit EC2 Instanz verbunden
- Docker und Git auf EC2 installiert
- GitHub Repository auf EC2 geclont
- App mit `docker-compose up --build -d` gestartet
- Fehler entdeckt: EC2 Festplatte war zu 100% voll (nur 6.7GB)
- AWS Volume von 6.7GB auf 20GB vergrössert
- Festplatte mit `growpart` und `resize2fs` zu erweitern versucht, aber dann doch auf AWS mit "modify volume".
- MySQL Container konnte nicht starten wegen korruptem Volume
- Verschiedene Lösungsversuche (docker prune, Volume löschen, Reboot)
- Entschieden die EC2 Instanz neu zu erstellen mit 20GB von Anfang an

## Was habe ich gelernt?
- Wie man per SSH auf einen Cloud-Server verbindet
- Wie Docker auf Ubuntu installiert wird
- Warum `sudo usermod -aG docker ubuntu` nötig ist und dass man sich neu einloggen muss damit es wirkt
- Was `df -h` zeigt und wie man den Festplattenverbrauch überwacht
- Wie man ein AWS Volume vergrössert und mit `growpart` + `resize2fs` aktiviert
- Was Docker Volumes sind und warum ein korruptes Volume Probleme verursacht
- Wie man Docker Logs analysiert (`docker logs container-name`)
- Fehler `No space left on device` und `data directory has files in it` verstehen

## Was war schwierig?
- Das MySQL Volume war durch den vollen Speicher korrumpiert und liess sich nicht mehr löschen da der Container es noch benutzte
- AppArmor verhinderte das Stoppen der Container – kein Standard-Befehl hat funktioniert
- Viel Zeit verloren mit verschiedenen Lösungsversuchen

## Nächste Woche
Neue EC2 Instanz mit 20GB Storage erstellen, App erfolgreich deployen und GitHub Actions CI/CD Pipeline einrichten.

---
