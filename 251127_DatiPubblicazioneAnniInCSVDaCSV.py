import csv
import requests
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
nome_elenco = input('Nome dell\'elenco: ')
nome_file = input("Nome del file senza estensione: ")
anno_inizio = input("Anno di inizio: ")
anno_fine = input("Anno di fine: ")

# variabili per la scrittura
data_oggi = datetime.today()
data_standard = data_oggi.strftime("%y%m%d")
percorso_file = data_standard + "_" + nome_elenco +"_Pubblicazioni_"+ anno_inizio + "-" + anno_fine + ".csv"
campi = ["cognome_nome", "doi", "titolo", "anno", "tipo", "biblio"]

# inizio dello script
inizio = time.perf_counter()

# controllo esistenza del file, eventuale creazione
esistenza_file = os.path.exists(percorso_file)
file_csv = open(percorso_file, mode="a", newline="", encoding="utf-8")
writer = csv.DictWriter(file_csv, fieldnames=campi)
if not esistenza_file:
    writer.writeheader()
    file_csv.flush()

# Apri il file CSV e popola la lista degli autori
lista_autori = []
with open(nome_file + '.csv', mode='r', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    contenuto_csv = [riga for riga in reader]

for riga in contenuto_csv:
    lista_autori.append(riga)

# parametri di paginazione
page = 1
page_size = 100
totale_trovati = 0

# variabili per la connessione
lista_pubblicazioni = []
params = {}
headers = {
    "accept": "application/json"
}
endpoint = "https://api.openaire.eu/graph/v2/researchProducts"

# converte gli anni in interi così da permettere i confronti
anno_inizio = int(anno_inizio)
anno_fine = int(anno_fine)

# cicla sugli autori, popolando la lista
for autore in lista_autori:
    cognome_nome = autore['COGNOME'] + " " + autore['NOME']
    print('Pubblicazioni di:', cognome_nome)
    page = 1

    # ottiene una risposta per autore
    while True:
        params = {
            "authorOrcid": autore['ORCID'],
            "page": page,
            "pageSize": page_size
        }
        risposta = requests.get(endpoint, headers=headers, params=params)
        if risposta.status_code != 200:
            print(f"Impossibile recuperare i dati: {risposta.status_code}")
            break

        tutti_dati = risposta.json()
        if len(tutti_dati["results"])== 0:
            print("Nessuna pubblicazione associata.")

        # ciclo i dati rilevanti delle pubblicazioni, saltando quelle non nell'intervallo di tempo
        for i, pubblicazione in enumerate(tutti_dati["results"]):
            if pubblicazione["publicationDate"] is not None:
                anno = int(pubblicazione["publicationDate"][:4])
                if (anno >= anno_inizio and anno <= anno_fine):
                    titolo = pubblicazione["mainTitle"]

                    #recupera il doi
                    doi = ""
                    pids = pubblicazione["pids"]
                    if pids != None:
                        for pid in pids:
                            if pid["scheme"] == "doi":
                                doi = pid["value"]
                                break

                    tipo = pubblicazione["type"]
                    biblio = str(pubblicazione["container"])

                    # forma la riga della pubblicazione
                    dati_pubblicazione = {"cognome_nome": cognome_nome, "doi": doi, "titolo": titolo, "anno": anno, "tipo": tipo, "biblio": biblio}

                    # scrive la riga nel CSV
                    tempo_passato = time.perf_counter() - inizio
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