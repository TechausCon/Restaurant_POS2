# Restaurant POS System

Dies ist ein vollständiges, modernes Point-of-Sale (POS) Kassensystem für ein Restaurant, das von Grund auf neu entwickelt wurde. Es deckt alle wesentlichen Abläufe von der Bestellung über die Küchenverwaltung bis hin zur Abrechnung ab.

## Hauptfunktionen

Das System besteht aus drei Hauptkomponenten, die nahtlos über eine zentrale Backend-API kommunizieren:

### 1. Administrations-Backend
Eine webbasierte Oberfläche zur Verwaltung der Restaurantgrundlagen.
- **Tischverwaltung:** Tische hinzufügen, bearbeiten und löschen.
- **Speisekarten-Management:** Kategorien (z.B. Vorspeisen, Hauptgerichte) und einzelne Gerichte/Artikel verwalten.
- **Benutzerverwaltung:** Administratoren, Kellner und Küchenpersonal anlegen und deren Rollen verwalten.
- **Analytics:** Ein einfaches Dashboard zur Anzeige von Gesamtumsätzen und der Anzahl der Rechnungen.

### 2. Bestell-Frontend (für Kellner)
Eine für Kellner optimierte Web-App zur Verwaltung des Gastraums.
- **Bestellaufnahme:** Bestellungen für Tische aufnehmen und direkt an die Küche senden.
- **Rechnungserstellung:** Rechnungen für Tische generieren.
- **Zahlungsabwicklung:** Zahlungen als "Bar" oder "Karte" verbuchen.

### 3. Küchen-Display
Eine spezielle Anzeige für die Küche, die Bestellungen in Echtzeit empfängt.
- **Echtzeit-Bestellanzeige:** Neue Bestellungen erscheinen sofort dank WebSockets.
- **Status-Updates:** Das Küchenpersonal kann den Status einer Bestellung ändern (z.B. "In Bearbeitung", "Fertig").

## Technologie-Stack

- **Backend:**
  - **Python 3**
  - **FastAPI:** Für die Erstellung der performanten REST-API und der WebSocket-Verbindung.
  - **SQLAlchemy:** Als ORM für die Datenbankinteraktion.
  - **SQLite:** Als einfache, dateibasierte Datenbank für die Entwicklung.
  - **Pydantic:** Zur Datenvalidierung und -serialisierung.
  - **JWT (JSON Web Tokens):** Für die Benutzerauthentifizierung und den Schutz der API-Endpunkte.

- **Frontend:**
  - **HTML5, CSS3, JavaScript (ES6):** Keine Frameworks, um die grundlegende Implementierung einfach zu halten.
  - **Playwright:** Für automatisierte End-to-End-Tests während der Entwicklung.

## Einrichtung und Start

Folgen Sie diesen Schritten, um die Anwendung lokal auszuführen.

### 1. Backend-Setup

**a. Abhängigkeiten installieren:**
Navigieren Sie in das `backend`-Verzeichnis und installieren Sie die notwendigen Python-Pakete.
```bash
pip install -r backend/requirements.txt
```

**b. Backend-Server starten:**
Führen Sie den folgenden Befehl aus dem Projektstammverzeichnis aus:
```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Der Backend-Server läuft nun auf `http://localhost:8000`. Die Datenbank wird beim ersten Start automatisch erstellt und mit Beispieldaten gefüllt.

### 2. Frontend-Setup

**a. Frontend-Server starten:**
Öffnen Sie ein **neues Terminalfenster** im Projektstammverzeichnis und starten Sie einen einfachen HTTP-Server, um die Frontend-Dateien auszuliefern.
```bash
cd frontend && python3 -m http.server 8080
```

### 3. Anwendung nutzen

Die Anwendung ist nun einsatzbereit. Sie können die verschiedenen Teile des Systems über die folgenden URLs aufrufen:

- **Login-Seite:** `http://localhost:8080/login/`
- **Admin-Panel:** `http://localhost:8080/admin/`
- **Kellner-App:** `http://localhost:8080/waiter/`
- **Küchen-Display:** `http://localhost:8080/kitchen/`

#### Standard-Login-Daten

Die Datenbank wird mit den folgenden Benutzern initialisiert:

| Rolle     | Benutzername | Passwort |
|-----------|--------------|----------|
| Admin     | `admin`      | `admin`  |
| Kellner   | `waiter`     | `waiter` |
| Küche     | `kitchen`    | `kitchen`|
