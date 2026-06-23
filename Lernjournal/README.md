# Lernjournal – Woche 1

**Datum:**
**Modul:**

---

## Was habe ich gemacht?

## Was habe ich gelernt?

## Was war schwierig?

## Nächste Woche

---

# Lernjournal – Woche 2

**Datum:** 29. Mai 2026
**Modul:** M300 – Cloud-Lösungen realisieren

---

## Was habe ich gemacht?
- Projekt geplant: Pokémon Budget Tracker als cloudbasierte App
- Technologien ausgewählt: Docker, AWS, GitHub Actions, Prometheus, Grafana
- Cloud-Architektur definiert (EC2, RDS, S3, CloudWatch)
- GitHub Repository mit Ordnerstruktur aufgesetzt
- Projektbeschreibung und Checkliste erstellt

## Was habe ich gelernt?
- Was der Unterschied zwischen V1 (max. 5.0) und V2 (bis 6.0) ist
- Wie eine CI/CD Pipeline läuft: Push, Docker Build, Deploy
- Was Prometheus und Grafana machen
- Wie Markdown-Links in GitHub funktionieren
- Wie man den Git-Fehler `unrelated histories` mit `--allow-unrelated-histories` löst

## Was war schwierig?
Am Anfang war die Technologiewahl schwierig, weil ich nicht so viel mit dem Thema zu tun hatte. Der Git-Fehler beim ersten Pull war unerwartet, aber zum Glück schnell gelöst.

## Nächste Woche
App lokal mit Docker aufsetzen, EC2 Instanz starten und App manuell deployen.

---

# Lernjournal – Woche 3

**Datum:** 5. Juni 2026
**Modul:** M300 – Cloud-Lösungen realisieren

---

## Was habe ich gemacht?
- Backend mit Python Flask und MySQL aufgesetzt
- Dockerfile, docker-compose.yml, nginx.conf und prometheus.yml erstellt
- Datenbankschema mit init.sql und Foreign Keys definiert (cards, entries, portfolio)
- Frontend (index.html) mit der Pokémon TCG API verbunden
- App lokal mit Docker zum Laufen gebracht (`docker-compose up --build`)
- App auf `http://localhost` getestet und alles lief

## Was habe ich gelernt?
- Wie docker-compose mehrere Services gleichzeitig startet (MySQL, Flask, Nginx, Prometheus, Grafana)
- Warum eine separate `init.sql` sauberer ist als Tabellen direkt im Python-Code zu erstellen
- Wie Foreign Keys in MySQL funktionieren (cards zu entries, cards zu portfolio)
- Wie Nginx als Reverse Proxy funktioniert (Port 80 ans Backend weiterleiten)
- Wie Docker Volumes funktionieren (Daten bleiben auch nach einem Neustart gespeichert)

## Was war schwierig?
- Docker Desktop war nicht gestartet, deswegen konnte die App nicht gebaut werden
- Der `backend` Ordner hat beim ersten `docker-compose up --build` gefehlt
- Die Ordnerstruktur musste zuerst richtig angelegt werden bevor Docker überhaupt funktioniert hat

## Nächste Woche
AWS EC2 Instanz starten, App auf den Server deployen und GitHub Actions CI/CD Pipeline einrichten.

---

# Lernjournal – Woche 4

**Datum:** 12. Juni 2026
**Modul:** M300 – Cloud-Lösungen realisieren

---

## Was habe ich gemacht?
- Per SSH mit der EC2 Instanz verbunden
- Docker und Git auf EC2 installiert
- GitHub Repository auf EC2 geclont
- App mit `docker-compose up --build -d` gestartet
- Fehler entdeckt: EC2 Festplatte war zu 100% voll (nur 6.7GB)
- AWS Volume von 6.7GB auf 20GB vergrössert
- Versucht die Festplatte mit `growpart` und `resize2fs` zu erweitern, hat aber nicht geklappt, dann über AWS "Modify Volume" gemacht
- MySQL Container konnte wegen einem korrupten Volume nicht starten
- Verschiedene Lösungsversuche ausprobiert (docker prune, Volume löschen, Reboot)
- Am Ende entschieden die EC2 Instanz neu zu erstellen mit 20GB von Anfang an

## Was habe ich gelernt?
- Wie man sich per SSH auf einen Cloud-Server verbindet
- Wie Docker auf Ubuntu installiert wird
- Warum `sudo usermod -aG docker ubuntu` nötig ist und dass man sich danach neu einloggen muss damit es wirkt
- Wie man ein AWS Volume vergrössert
- Was Docker Volumes sind und warum ein korruptes Volume so Probleme macht
- Wie man Docker Logs analysiert mit `docker logs container-name`
- Was die Fehler `No space left on device` und `data directory has files in it` bedeuten

## Was war schwierig?
Das MySQL Volume war durch den vollen Speicher kaputt gegangen und liess sich nicht löschen weil der Container es noch benutzt hat. Dazu hat AppArmor das Stoppen der Container verhindert und kein einziger Standardbefehl hat funktioniert. Hab viel Zeit mit verschiedenen Lösungsversuchen verloren.

## Nächste Woche
Neue EC2 Instanz mit 20GB Storage erstellen, App erfolgreich deployen und GitHub Actions CI/CD Pipeline einrichten.

---

# Lernjournal – Woche 5

**Datum:** 19/20. Juni 2026
**Modul:** M300 – Cloud-Lösungen realisieren

---

## Was habe ich gemacht?
- Alle 5 Container erfolgreich auf EC2 gestartet (MySQL, Flask, Nginx, Prometheus, Grafana)
- Security Groups angepasst: Port 3000 (Grafana) und 9090 (Prometheus) geöffnet
- Prometheus als Datenquelle in Grafana verbunden (`http://prometheus:9090`)
- Grafana Dashboard **Pokemon-Tracker** mit 4 Panels erstellt:
  - HTTP Anfragen total
  - API Antwortzeit
  - CPU Verbrauch
  - RAM Verbrauch
- Prometheus Target überprüft, Status war **UP** (`http://backend:5000/metrics`)
- Docker Hub Access Token erstellt (`m300-pipeline`, Read & Write)
- GitHub Secrets gesetzt (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `EC2_HOST`, `EC2_KEY`)
- CI/CD Pipeline mit GitHub Actions eingerichtet (`.github/workflows/deploy.yml`)
- Pipeline getestet und erfolgreich, Status **Success** in 41 Sekunden

## Was habe ich gelernt?
- Wie man Grafana mit Prometheus als Datenquelle verbindet
- Wie man Panels in Grafana erstellt und Prometheus Queries eingibt
- Was `http_requests_total`, `process_cpu_seconds_total` und `process_resident_memory_bytes` bedeuten
- Wie GitHub Actions funktioniert (Trigger, Jobs, Steps)
- Wie man Docker Hub Access Tokens erstellt und warum `Read & Write` nötig ist
- Warum GitHub Secrets so wichtig sind (Passwörter gehören nie in den Code)
- Den Unterschied zwischen `docker-compose` und `docker compose` auf neueren Ubuntu Versionen
- Wie man einen fehlgeschlagenen Pipeline-Run analysiert und den Fehler findet

## Was war schwierig?
Die Pipeline ist beim ersten Versuch fehlgeschlagen weil `docker-compose` auf der neuen EC2 nicht mehr verfügbar war. Der richtige Befehl ist `docker compose` ohne Bindestrich. Ausserdem war Port 9090 zuerst nicht erreichbar weil die Security Group noch nicht angepasst war.

## Nächste Woche
Grafana Alert einrichten, Reflexion schreiben und Dokumentation fertigstellen.

---

# Lernjournal – Woche 6

**Datum:** 23. Juni 2026
**Modul:** M300 – Cloud-Lösungen realisieren

---

## Was habe ich gemacht?
- Elastic IP in AWS erstellt und der EC2 Instanz zugewiesen (18.233.206.180)
- GitHub Secret `EC2_HOST` mit der neuen Elastic IP aktualisiert
- Grafana Alert eingerichtet (Backend Down, IS BELOW 1, Evaluate every 1m)
- Netzwerkdiagramme erstellt (Zugriff von aussen und AWS Infrastruktur)
- Systemdokumentation fertiggestellt mit allen Screenshots und Diagrammen
- Lernjournal angepasst

## Was habe ich gelernt?
- Was eine Elastic IP ist und warum man sie braucht: ohne Elastic IP ändert sich die öffentliche IP bei jedem Neustart der EC2 Instanz, mit Elastic IP bleibt sie immer gleich
- Wie man GitHub Secrets nachträglich anpassen kann
- Wie man Alerts in Grafana konfiguriert (Alert Rule, Evaluation Group, Pending Period)
- Wie man eine Systemdokumentation sauber aufbaut mit Screenshots und Diagrammen

## Was war schwierig?
Nach dem Erstellen der Elastic IP musste das GitHub Secret `EC2_HOST` manuell aktualisiert werden, sonst hätte die CI/CD Pipeline nicht mehr funktioniert. Sowas vergisst man schnell.

## Nächste Woche
Reflexion schreiben, Lernjournal abschliessen und alles für die Abgabe fertigmachen.

---