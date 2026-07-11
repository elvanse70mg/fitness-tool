# 💪 Fitness & Ernährungs Tool

Ein KI-gestützter Fitness- und Ernährungs-Tracker gebaut mit Python und Streamlit.

> *"Ich lerne Python seit 3 Wochen – das ist mein erstes echtes Projekt."*

---

## ✨ Features

### 🍗 Ernährung
- Tagesmahlzeiten tracken und abhaken
- Kalorien & Protein automatisch summieren
- KI-generierter Wochenplan basierend auf deinem Ziel (Bulk / Cut / Bodyrecomp)
- Persönlicher Proteinbedarf wird automatisch berechnet (1.8g/kg)
- Proteinshakes & Medikamente in der Planung berücksichtigbar
- Rezepte & Zubereitung pro Gericht (aufklappbar)
- Täglicher automatischer Reset um Mitternacht

### 🛒 Einkaufsliste
- Automatisch aus dem KI-Wochenplan generiert
- Gruppiert nach Kategorien (Fleisch/Fisch, Gemüse, Kohlenhydrate etc.)
- Mengen werden über die ganze Woche summiert

### 💪 Training
- Trainingseinheiten mit Sätzen & Wiederholungen tracken
- KI-Trainingsplan Generator (Geräte, Fokus, Level, Zeit)
- Tägliche Übersicht abhaken & rückgängig machen

### 📊 Fortschritt
- Körpergewicht täglich eintragen
- Gewichtsverlauf als interaktives Liniendiagramm

---

## 🛠️ Technologien

| Technologie | Verwendung |
|---|---|
| Python | Hauptsprache |
| Streamlit | Web-Interface |
| Groq API (Llama 3.3) | KI-Ernährungs- & Trainingsplanung |
| pandas | Datenvisualisierung |
| JSON | Persistente Datenspeicherung |
| python-dotenv | Sichere API Key Verwaltung |
| re (Regex) | JSON-Bereinigung der KI-Antworten |

---

## 🚀 Installation

**1. Repository klonen:**
```bash
git clone https://github.com/elvanse70mg/fitness-tool.git
cd fitness-tool
```

**2. Abhängigkeiten installieren:**
```bash
pip install streamlit groq pandas python-dotenv
```

**3. API Key einrichten:**

Erstelle eine Datei `fitness_tool_api_key.env`:
```
GROQ_API_KEY=dein_groq_api_key
```

Kostenlosen Groq API Key bekommst du auf [console.groq.com](https://console.groq.com)

**4. App starten:**
```bash
streamlit run fitness_tool.py
```

Oder per Doppelklick auf `start_fitness_tool.bat` (Windows)

---

## 📁 Projektstruktur

```
fitness-tool/
├── fitness_tool.py          # Hauptanwendung
├── .gitignore               # API Keys & lokale Daten ausgeschlossen
└── README.md                # Diese Datei
```

---

## 🧠 Was ich dabei gelernt habe

- Streamlit für schnelle Web-Apps
- REST API Integration (Groq/Llama)
- Prompt Engineering für strukturierte KI-Ausgaben (JSON)
- JSON Datenpersistenz & Fehlerbehandlung
- Regex (re.sub) für Datenbereinigung
- Git & GitHub Workflows
- OOP, Klassen, Vererbung
- Tägliche Reset-Logik mit datetime

---

## 👤 Über mich

Ich bin Klaus. Ich lerne seit Juni 2026.

📫 GitHub: [@elvanse70mg](https://github.com/elvanse70mg)

---

## 📋 Roadmap

- [x] Ernährungs-Tracker mit KI-Plan
- [x] Einkaufsliste mit Kategorien
- [x] Rezepte & Zubereitung
- [x] Training-Tracker mit KI-Plan
- [x] Gewichtsverlauf mit Chart
- [ ] Benutzerprofile speichern
- [ ] Datenbankanbindung (SQLite/Supabase)