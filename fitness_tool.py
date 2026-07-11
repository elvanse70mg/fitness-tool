import streamlit as st, json, re
from datetime import date
import pandas as pd
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv("fitness_tool_api_key.env")
api_key = os.getenv("GROQ_API_KEY")

food_result = {}
food_list = []

##json datei laden
def lade_daten():
    try:
        with open("daten.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "ernaehrung": {"mahlzeiten": []},
            "training": {"einheiten": []},
            "koerper": {"gewicht": []}
        }

##json datei speichern
def speichere_daten(daten):
    with open("daten.json", "w") as f:
        json.dump(daten, f)

daten = lade_daten()
tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
heute_tag = tage[date.today().weekday()]
heute = str(date.today())

##Täglicher Reset
if daten.get("letztes_datum") != heute:
    for mahlzeit in daten["ernaehrung"]["mahlzeiten"]:
        mahlzeit["abgehakt"] = False
    for einheit in daten["training"]["einheiten"]:
        einheit["abgehakt"] = False
    daten["letztes_datum"] = heute
    speichere_daten(daten)

st.title("💪 Fitness & Ernährungs Tool")
seite = st.sidebar.radio("Navigation", ["🍗 Ernährung", "💪 Training", "📊 Fortschritt"])

##Daten
nicht_abgehakt = []
abgehakt = []
kalorien_summe = 0
protein_summe = 0
trainings_einheiten_summe = 0


##Menu
##Ernährungsseite
if seite == "🍗 Ernährung":
    st.write("Gesund und Lecker")
    st.subheader("Heutige Mahlzeiten")

    ##Clear Button
    if st.button("🗑️ Mahlzeiten löschen"):
        daten["ernaehrung"]["mahlzeiten"] = []
        speichere_daten(daten)
        st.rerun()

    ##Tracker
    for index, mahlzeit in enumerate(daten["ernaehrung"]["mahlzeiten"]):
        if mahlzeit.get("tag", None) == heute_tag:
            if mahlzeit["abgehakt"]:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.success(mahlzeit["name"])
                    ##Zubereitung anzeigen falls vorhanden
                    if mahlzeit.get("zubereitung"):
                        with st.expander("📖 Rezept anzeigen"):
                            st.write(mahlzeit["zubereitung"])
                with col2:
                    if st.button("↩️", key=f"undo_essen_{index}"):
                        mahlzeit["abgehakt"] = False
                        speichere_daten(daten)
                        st.rerun()
                kalorien_summe += mahlzeit["kalorien"]
                protein_summe += mahlzeit["protein"]
            else:
                if st.checkbox(mahlzeit["name"], key=f"check_essen_{index}"):
                    mahlzeit["abgehakt"] = True
                    speichere_daten(daten)
                    st.rerun()
                ##Zubereitung anzeigen falls vorhanden
                if mahlzeit.get("zubereitung"):
                    with st.expander("📖 Rezept anzeigen", key=f"rezept_{index}"):
                        st.write(mahlzeit["zubereitung"])

    st.metric("Heutige Kalorien", kalorien_summe)
    st.metric("Heutige Proteine", protein_summe)

    ##Hinzufügen
    st.subheader("➕ Neue Mahlzeit hinzufügen")
    name = st.text_input("Name")
    kalorien = st.number_input("Kalorien")
    protein = st.number_input("Protein")
    zubereitung = st.text_area("Zubereitung (optional)")
    tag = st.selectbox("Wochentag", tage, index=tage.index(heute_tag))

    if st.button("Hinzufügen"):
        neue_mahlzeit = {
            "name": name,
            "kalorien": kalorien,
            "protein": protein,
            "tag": tag,
            "zubereitung": zubereitung,
            "abgehakt": False
        }
        daten["ernaehrung"]["mahlzeiten"].append(neue_mahlzeit)
        speichere_daten(daten)
        st.rerun()

    ##Plan erstellen mit AI
    st.subheader("🤖 KI Ernährungsplan")

    ##Nutzereingaben sammeln
    budget = st.number_input("Wochenbudget (€)", value=50)
    geschlecht = st.selectbox("Geschlecht", ["Mann", "Frau"])
    groesse = st.number_input("Größe (cm)", value=175)
    gewicht_start = st.number_input("Gewicht (kg)", value=78)
    protein_bedarf = gewicht_start * 1.8

    ##Ziel
    ziel = st.selectbox("Was ist dein Ziel?", ["Bodyrecomp", "Bulk", "Cut"])

    ##Sonstige Medikamente
    weitere_medikamente = st.checkbox("Nimmst du weitere Medikamente ein?")
    if weitere_medikamente:
        medikament_name = st.text_input("Wie lautet der Name des Medikaments?")
        medikament_dosis = st.text_input("Welche Dosis?")

    ##Shake Abfrage
    nutzt_shakes = st.checkbox("Nutzt du Protein Shakes?")
    if nutzt_shakes:
        shake_name = st.text_input("Shake Bezeichnung")
        anzahl_shakes = st.number_input("Anzahl pro Tag", value=1)

    ##Generieren Button
    if st.button("🥗 Plan generieren"):

        ##Prompt bauen
        prompt = f"""
        Ich bin ein {geschlecht} mit {groesse} cm Größe und {gewicht_start} kg Gewicht.
        Mein Budget beträgt {budget} EUR pro Woche, ich habe wenig Zeit zum Kochen
        und benötige eine proteinreiche Ernährung.
        Erstelle mir einen Wochenplan. Mein Ziel ist {ziel}. Bitte gib mir für jeden Tag der Woche 
        ein Gericht mit Name, Kalorien und Protein an. Mein täglicher Proteinbedarf ist {protein_bedarf}.
        Gebe auch die Zutatenliste und eine kurze Zubereitung für jedes Gericht an.
        Kategorisiere die Zutaten in Kategorien: Fleisch/Fisch, Gemüse, Kohlenhydrate, Milchprodukte, Gewürze/Öle, Sonstiges.
        Wichtig: Nutze IMMER einen Punkt als Dezimaltrennzeichen, niemals ein Komma (also 0.5 nicht 0,5).
        Antworte AUSSCHLIESSLICH mit einem JSON-Array ohne weitere Erklärungen oder Text.
        Nutze genau dieses Format:
        [
          {{"tag": "Montag", "name": "Hähnchenbrust", "kalorien": 450, "protein": 35, "zubereitung": "1. Hähnchen würzen. 2. In Pfanne anbraten.", "zutaten": [
            {{"name": "Hähnchenbrust", "menge": 200, "einheit": "g", "kategorie": "Fleisch/Fisch"}},
            {{"name": "Olivenöl", "menge": 1, "einheit": "EL", "kategorie": "Gewürze/Öle"}}
          ]}},
          ...
        ]
        """

        ##Shake Prompt hinzufügen falls nötig
        if nutzt_shakes:
            prompt += f"""
            Ich trinke {anzahl_shakes} Proteinshakes pro Tag der Marke {shake_name}.
            Berücksichtige dies im Kalorienziel und erstelle den Plan für die restlichen Mahlzeiten.
            """

        if weitere_medikamente:
            prompt += f"""
            Ich nehme zusätzlich das Medikament {medikament_name} in einer Dosis von {medikament_dosis}.
            Berücksichtige dies bei der Erstellung des Ernährungsplans.
            """

        ##API Aufruf
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        ##Speichern
        try:
            ##Deutsches Komma durch Punkt ersetzen
            rohtext = response.choices[0].message.content
            rohtext = re.sub(r'(\d),(\d)', r'\1.\2', rohtext)
            mahlzeiten = json.loads(rohtext)
            for mahlzeit in mahlzeiten:
                mahlzeit["abgehakt"] = False
                daten["ernaehrung"]["mahlzeiten"].append(mahlzeit)
            speichere_daten(daten)
            st.rerun()
        except json.JSONDecodeError:
            st.error("Fehler beim Verarbeiten der Antwort. Bitte versuche es erneut.")

    ##Einkaufsliste
    st.subheader("🛒 Wocheneinkaufsliste")
    kategorien = {}
    for mahlzeit in daten["ernaehrung"]["mahlzeiten"]:
        for zutat in mahlzeit.get("zutaten", []):
            if isinstance(zutat, dict):
                kat = zutat.get("kategorie", "Sonstiges")
                name = zutat["name"]
                menge = zutat.get("menge", 0)
                einheit = zutat.get("einheit", "")

                if kat not in kategorien:
                    kategorien[kat] = {}

                schluessel = f"{name}_{einheit}"
                if schluessel not in kategorien[kat]:
                    kategorien[kat][schluessel] = {"name": name, "menge": menge, "einheit": einheit}
                else:
                    kategorien[kat][schluessel]["menge"] += menge

    if kategorien:
        for kat, zutaten in kategorien.items():
            st.subheader(f"🏷️ {kat}")
            for zutat in zutaten.values():
                st.write(f"• {zutat['menge']} {zutat['einheit']} {zutat['name']}")
    else:
        st.write("Noch kein Plan generiert.")


##Trainingsseite
elif seite == "💪 Training":
    st.write("Hart und Schwer")
    st.subheader("Heutige Trainingseinheiten")

    ##Clear Button
    if st.button("🗑️ Trainingsplan löschen"):
        daten["training"]["einheiten"] = []
        speichere_daten(daten)
        st.rerun()

    for index, uebung in enumerate(daten["training"]["einheiten"]):
        if uebung.get("tag", None) == heute_tag:
            if uebung["abgehakt"]:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.success(f"{uebung['name']} – {uebung.get('saetze', '?')} Sätze x {uebung.get('wiederholungen', uebung.get('uebung', '?'))} Wdh")
                with col2:
                    if st.button("↩️", key=f"undo_training_{index}"):
                        uebung["abgehakt"] = False
                        speichere_daten(daten)
                        st.rerun()
                trainings_einheiten_summe += uebung.get("wiederholungen", uebung.get("uebung", 0))
            else:
                label = f"{uebung['name']} – {uebung.get('saetze', '?')} Sätze x {uebung.get('wiederholungen', uebung.get('uebung', '?'))} Wdh"
                if st.checkbox(label, key=f"check_training_{index}"):
                    uebung["abgehakt"] = True
                    speichere_daten(daten)
                    st.rerun()

    st.metric("Heutige Trainingseinheiten", trainings_einheiten_summe)

    ##Hinzufügen
    st.subheader("➕ Neue Einheit hinzufügen")
    name = st.text_input("Name")
    uebung_sum = st.number_input("Wiederholungen")
    saetze = st.number_input("Saetze")

    if st.button("Hinzufügen"):
        neue_mahlzeit = {
            "name": name,
            "uebung": uebung_sum,
            "saetze": saetze,
            "abgehakt": False
        }
        daten["training"]["einheiten"].append(neue_mahlzeit)
        speichere_daten(daten)
        st.rerun()

    ##Trainingsplan erstellen mit AI
    st.subheader("🤖 KI Trainingsplan")

    geraete = st.multiselect("Welche Geräte hast du zur Verfügung?", ["Laufband", "Rudergerät", "Klimmzugstange", "Hantelbank", "Kurzhanteln", "Langhantel", "Kabelzug", "Kettlebell", "Bodyweight"])
    trainingstage = st.number_input("Wie viele Tage pro Woche möchtest du trainieren?", min_value=1, max_value=7, value=3)
    fokus = st.radio("Was ist dein Trainingsfokus?", ["Kraft", "Ausdauer", "Ausdauer und Kraft"])
    erfahrung = st.radio("Wie ist dein Trainingslevel?", ["Anfänger", "Fortgeschritten", "Experte"])
    trainingszeit = st.number_input("Wie viele Minuten pro Trainingseinheit?", min_value=10, max_value=180, value=60)

    if st.button("🏋️‍♂️ Trainingsplan generieren"):
        prompt = f"""
        Ich habe folgende Geräte zur Verfügung: {', '.join(geraete)}.
        Ich möchte {trainingstage} Tage pro Woche trainieren.
        Mein Trainingsfokus ist {fokus}.
        Mein Trainingslevel ist {erfahrung}.
        Jede Trainingseinheit soll ungefähr {trainingszeit} Minuten dauern.
        Bitte erstelle mir einen Trainingsplan für eine Woche.
        Antworte AUSSCHLIESSLICH mit einem JSON-Array ohne weitere Erklärungen oder Text.
        Nutze genau dieses Format:
        [
          {{"tag": "Montag", "name": "Übungsname", "saetze": 0, "wiederholungen": 0}},
          ...
        ]
        """

        ##API Aufruf
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        ##Speichern mit try/except
        try:
            rohtext = response.choices[0].message.content
            rohtext = re.sub(r'(\d),(\d)', r'\1.\2', rohtext)
            einheiten = json.loads(rohtext)
            for einheit in einheiten:
                einheit["abgehakt"] = False
                daten["training"]["einheiten"].append(einheit)
            speichere_daten(daten)
            st.rerun()
        except json.JSONDecodeError:
            st.error("Fehler beim Generieren des Trainingsplans.")


##Fortschritt-Seite
elif seite == "📊 Fortschritt":
    st.subheader("⚖️ Gewicht eintragen")
    

    ##Clear Button
    if st.button("🗑️ Gewichtsverlauf löschen"):
        daten["koerper"]["gewicht"] = []
        speichere_daten(daten)
        st.rerun()

    gewicht = st.number_input("Gewicht (kg)")

    if st.button("Eintragen"):
        neuer_eintrag = {
            "datum": str(date.today()),
            "gewicht": gewicht
        }
        daten["koerper"]["gewicht"].append(neuer_eintrag)
        speichere_daten(daten)
        st.rerun()

    df = pd.DataFrame(daten["koerper"]["gewicht"])
    if not df.empty:
        st.line_chart(df, x="datum", y="gewicht")
    else:
        st.write("Noch keine Gewichtsdaten vorhanden.")