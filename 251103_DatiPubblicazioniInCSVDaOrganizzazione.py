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

# dati sull'organizzazione
nome_organizzazione = input("Nome dell'organizzazione: ")
ror_organizzazione = input("ROR dell'organizzazione: ")

# definizione dei parametri della richiesta per trovare l'id dell'organizzazione
# definizione dei parametri della richiesta per trovare le pubblicazioni dell'organizzazione
endpoint_organizzazione = "https://api.openaire.eu/graph/v1/organizations"
params_orgaizzazione = {
    "pid": ror_organizzazione
}
headers_organizzazione = {
    "accept": "application/json"
}

# inizio dello script
inizio = time.perf_counter()

# ottiene una risposta e la trasforma in dizionario
risposta_organizzazione = requests.get(endpoint_organizzazione, headers=headers_organizzazione, params=params_orgaizzazione)
if risposta_organizzazione.status_code == 200:
    dati_organizzazione = risposta_organizzazione.json()
else:
    print(f"Impossibile recuperare i dati: {risposta_organizzazione.status_code}")

#ottiene l'id dell'organizzazione
tempo_passato = time.perf_counter() - inizio
id_organizzazione = dati_organizzazione["results"][0]["id"]
print(orario_leggibile(round(tempo_passato)), "Id organizzazione:", id_organizzazione)

# definizione dei parametri della richiesta per trovare le pubblicazioni dell'organizzazione
endpoint = "https://api.openaire.eu/graph/v2/researchProducts"
headers = {
    "accept": "application/json"
}

# variabili per la scrittura
data_oggi = datetime.today()
data_standard = data_oggi.strftime("%y%m%d")
percorso_file = data_standard + "_" + nome_organizzazione +"_Pubblicazioni.csv"
campi = ["doi", "titolo", "data"]

# controllo esistenza del file, eventuale creazione
esistenza_file = os.path.exists(percorso_file)
file_csv = open(percorso_file, mode="a", newline="", encoding="utf-8")
writer = csv.DictWriter(file_csv, fieldnames=campi)
if not esistenza_file:
    writer.writeheader()
    file_csv.flush()

# parametri di paginazione
page = 1
page_size = 100
totale_trovati = 0

# divide la richiesta per anni per evitare il limite di 10k risultati
params = {}
for anno in range(1950, 2026):
    page = 1 # reset pagina per ogni anno
    params["fromPublicationDate"] = f"{anno}-01-01"
    params["toPublicationDate"] = f"{anno}-12-31"
    print(f"Pubblicazioni del {anno}.")
    # esegue la paginazione
    while True:
        params["relOrganizationId"] = id_organizzazione
        params["page"] = page
        params["pageSize"] = page_size
        risposta = requests.get(endpoint, headers=headers, params=params)
        if risposta.status_code != 200:
            print(f"Impossibile recuperare i dati: {risposta.status_code}")
            break

        tutti_dati = risposta.json()

        # ciclo i dati rilevanti delle pubblicazioni
        for i, pubblicazione in enumerate(tutti_dati["results"]):
            titolo = pubblicazione["mainTitle"]
            data = pubblicazione["publicationDate"]

            #recupera il doi
            doi = ""
            pids = pubblicazione["pids"]
            if pids != None:
                for pid in pids:
                    if pid["scheme"] == "doi":
                        doi = pid["value"]
                        break

            # forma la riga della pubblicazione
            dati_pubblicazione = {"doi": doi, "titolo": titolo, "data": data}

            # scrive la riga nel CSV
            writer.writerow(dati_pubblicazione)
            file_csv.flush()

            # attesa API e segni di vita
            tempo_passato = time.perf_counter() - inizio
            totale_trovati += 1
            print(totale_trovati, ") ", orario_leggibile(round(tempo_passato)),":", dati_pubblicazione["titolo"])

        if len(tutti_dati["results"]) < page_size:
            break

        page += 1
        time.sleep(0.5)

# scrive i dati in un file CSV
file_csv.close()
print("Completato.")
