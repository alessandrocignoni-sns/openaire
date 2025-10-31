import requests
import csv
import os
import time
from datetime import datetime

# funzione di conversione secondi in ore, minuti, secondi
def orario_leggibile(secondi_totali):
    ore = secondi_totali // 3600
    minuti = (secondi_totali % 3600) // 60
    secondi = secondi_totali % 60
    return f"{ore}h {minuti}m {secondi}s"

# dati sull'autore
cognome_autore = input("Cognome dell'autore: ")
orcid_autore = input("Inserisci l'orcid dell'autore: ")

# definizione dei parametri della richiesta
endpoint = "https://api.openaire.eu/graph/v2/researchProducts" # URL dell'endpoint delle API
params = {
    "authorOrcid": orcid_autore
}
headers = {
    "accept": "application/json"
}

# variabili per la scrittura
data_oggi = datetime.today()
data_standard = data_oggi.strftime("%y%m%d")
percorso_file = data_standard + "_" + cognome_autore +"_Works.csv"
campi = ["doi", "titolo", "data"]

# inizio dello script
inizio = time.perf_counter()

# controllo esistenza del file, eventuale creazione
esistenza_file = os.path.exists(percorso_file)
file_csv = open(percorso_file, mode="a", newline="", encoding="utf-8")
writer = csv.DictWriter(file_csv, fieldnames=campi)
if not esistenza_file:
    writer.writeheader()
    file_csv.flush()

# ottiene una risposta e la trasforma in dizionario
risposta = requests.get(endpoint, headers=headers, params=params)
if risposta.status_code == 200:
    tutti_dati = risposta.json()
else:
    print(f"Impossibile recuperare i dati: {risposta.status_code}")

# ciclo i dati rilevanti delle pubblicazioni
for i, pubblicazione in enumerate(tutti_dati["results"]):
    titolo = pubblicazione["mainTitle"]
    data = pubblicazione["publicationDate"]

    #recupera il doi
    doi = ""
    pids = pubblicazione["pids"]
    for pid in pids:
        if pid["scheme"] == "doi":
            doi = pid["value"]
            break

    # forma la riga della pubblicazione
    dati_pubblicazione = {"doi": doi, "titolo": titolo, "data": data}

    # scrive la riga nel CSV
    tempo_passato = time.perf_counter() - inizio
    writer.writerow(dati_pubblicazione)
    file_csv.flush()
    print(i + 1, ") ", orario_leggibile(round(tempo_passato)),":", dati_pubblicazione["titolo"])

# scrive i dati in un file CSV
file_csv.close()
print("Completato.")