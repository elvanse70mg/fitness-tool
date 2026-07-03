import streamlit as st, json
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
if daten.get("letztes_datum") != heute:
    for mahlzeit in daten["ernaehrung"]["mahlzeiten"]:
        mahlzeit["abgehakt"] = False
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
##Tracker
if seite == "🍗 Ernährung":
    st.write("Gesund und Lecker")
    st.subheader("Heutige Mahlzeiten")
    
    for index, mahlzeit in enumerate(daten["ernaehrung"]["mahlzeiten"]):
        if mahlzeit.get("tag", None) == heute_tag:
            if mahlzeit["abgehakt"]:
                col1, col2 = st.columns([4, 1])
                with col1:
                 st.success(mahlzeit["name"])
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
    st.metric("Heutige Kalorien", kalorien_summe)
    st.metric("Heutige Proteine", protein_summe)

    ##Hinzufügen
    st.subheader("➕ Neue Mahlzeit hinzufügen")
    name = st.text_input("Name")
    kalorien = st.number_input("Kalorien")
    protein = st.number_input("Protein")
    tag= st.selectbox("Wochentag", tage, index = tage.index(heute_tag))

    if st.button("Hinzufügen"):
        neue_mahlzeit = {
            "name" : name,
            "kalorien" : kalorien,
            "protein" : protein,
            "tag" : tag,
            "abgehakt" : False
        }
        daten["ernaehrung"]["mahlzeiten"].append(neue_mahlzeit)
        speichere_daten(daten)
        st.rerun()




    ##Plan erstellen mit AI
    st.subheader("🤖 KI Ernährungsplan")
    
    ##Nutzereingaben sammeln
    budget = st.number_input("Wochenbudget (€)", value=50)
    geschlecht = st.selectbox("Geschlecht", ["Mann", "Frau"])
    groesse = st.number_input("Größe (cm)", value=172)
    gewicht_start = st.number_input("Gewicht (kg)", value=78)
    protein_bedarf = gewicht_start * 1.8

    ##Ziel
    ziel = st.selectbox("Was ist dein Ziel?", ["Bodyrecomp", "Bulk", "Cut"])

    ##TRT
    trt = st.checkbox("Bist du in einer Testosteronersatztherapie?")
    if trt:
        trt_ester = st.text_input("Welcher Ester?")
        trt_dosis = st.number_input("Welche Dosis?")
        trt_haeufigkeit = st.text_input("Wie oft?")

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
        Antworte AUSSCHLIESSLICH mit einem JSON-Array ohne weitere Erklärungen oder Text.
Nutze genau dieses Format:
[
  {{"tag": "Montag", "name": "Gerichtname", "kalorien": 000, "protein": 00}},
  ...
]
        """

        ##Shake Prompt hinzufügen falls nötig
        if nutzt_shakes:
            prompt += f"""
            Ich trinke {anzahl_shakes} Proteinshakes pro Tag der Marke {shake_name}.
            Berücksichtige dies im Kalorienziel und erstelle den Plan für die restlichen Mahlzeiten.
            """

        if trt:
            prompt += f"""
            Ich bin in einer Testosteronersatztherapie mit dem Ester {trt_ester} und einer Dosis von {trt_dosis} mg {trt_haeufigkeit}.
            Berücksichtige dies bei der Erstellung des Ernährungsplans.
            """

        if weitere_medikamente:
            prompt += f"""
            Ich nehme zusätzlich das Medikament {medikament_name} in einer Dosis von {medikament_dosis}.
            Berücksichtige dies bei der Erstellung des Ernährungsplans.
            """

        # API Aufruf ersetzen
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}])
        st.write(response.choices[0].message.content)

        #Speichern
        mahlzeiten = json.loads(response.choices[0].message.content)
        for mahlzeit in mahlzeiten:
            mahlzeit["abgehakt"] = False
            daten["ernaehrung"]["mahlzeiten"].append(mahlzeit)
        speichere_daten(daten)
        st.rerun()




##Trainingsseite
elif seite == "💪 Training":
    st.write("Hart und Schwer")
    st.subheader("Heutige Trainingseinheiten")
    
    for index, uebung in enumerate(daten["training"]["einheiten"]):
        if uebung["abgehakt"]:
            st.success(f"{uebung['name']} – {uebung['saetze']} Sätze x {uebung['uebung']} Wdh")
            trainings_einheiten_summe += uebung["uebung"]
            
        else:
            if st.checkbox(uebung["name"], key=f"check_training_{index}"):
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
            "name" : name,
            "uebung" : uebung_sum,
            "saetze" : saetze,
            "abgehakt" : False
        }
        daten["training"]["einheiten"].append(neue_mahlzeit)
        speichere_daten(daten)
        st.rerun()





##Fortschritt-Seite
elif seite == "📊 Fortschritt":
    st.subheader("⚖️ Gewicht eintragen")
    st.write("Alle the way up!")
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
    st.line_chart(df, x="datum", y="gewicht")





















