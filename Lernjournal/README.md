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
- Unterschied V1 (max. 5.0) und V2 (bis 6.0)
- Wie eine CI/CD Pipeline funktioniert (Push → Docker Build → Deploy)
- Was Prometheus/Grafana für das Monitoring macht
- Wie Markdown-Links in GitHub funktionieren
- Git-Fehler `unrelated histories` mit `--allow-unrelated-histories` lösen

## Was war schwierig?
Die richtige Technologiewahl war am Anfang unklar, da ich noch keine Erfahrung hatte. Der Git-Fehler beim ersten Pull war unerwartet, aber schnell gelöst.

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

# Lernjournal – Woche 4

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