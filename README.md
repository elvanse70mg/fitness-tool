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
- TRT & Medikamente werden bei der Planung berücksichtigt
- Proteinshakes in den Plan integrierbar
- Täglicher automatischer Reset um Mitternacht

### 💪 Training
- Trainingseinheiten mit Sätzen & Wiederholungen tracken
- Tägliche Übersicht abhaken

### 📊 Fortschritt
- Körpergewicht täglich eintragen
- Gewichtsverlauf als interaktives Liniendiagramm

---

## 🛠️ Technologien

| Technologie | Verwendung |
|---|---|
| Python | Hauptsprache |
| Streamlit | Web-Interface |
| Groq API (Llama 3.3) | KI-Ernährungsplanung |
| pandas | Datenvisualisierung |
| JSON | Persistente Datenspeicherung |
| python-dotenv | Sichere API Key Verwaltung |

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
- JSON Datenpersistenz
- Prompt Engineering für strukturierte KI-Ausgaben
- Git & GitHub Workflows

---

## 👤 Über mich

Ich bin Klaus, 25 Jahre alt aus Arendsee. Ich lerne seit Juni 2026 Python und arbeite auf eine Umschulung zum **Fachinformatiker für Prozess- und Datenanalyse** hin. Mein Ziel ist ein Remote-Job als Python Developer oder ML Engineer.

📫 GitHub: [@elvanse70mg](https://github.com/elvanse70mg)

---

## 📋 Roadmap

- [ ] KI-Trainingsplan Generator
- [ ] Einkaufsliste aus Wochenplan
- [ ] Rezepte & Zubereitung
- [ ] Mobile App (iOS/Android)
