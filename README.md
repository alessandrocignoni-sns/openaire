# SVR's OpenAIRE scripts
Python 3 scripts, useful to Research Assessment and Open Science Service of Scuola Normale Superiore.

Necessary libraries:

    requests

## Scripts English description
Code is written and commented in Italian. Here a brief description of the scripts:
- **251030_DatiPubblicazioniInCSVDaAutore.py** - From author ORCID id, it uses the researchProducts endopoint to get the data for each of their publication, then it writes them in a CSV file containing DOI, title and publishing date of each publication.
- **251103_DatiPubblicazioniInCSVDaOrganizzazione.py** - From organization ROR id, first it uses the organization endopoint to gets the OpenAIRE id of the organization, secondly it uses the researchProducts endopoint to get the data for each publication with at least an author affiliated to the organization, then it writes it in a CSV file containing DOI, title and publishing date of each publication.
- **251105_DatiPubblicazioniInCSVDaCSV.py** - From a CSV file in the same folder of the script containing name, surname, fiscal code and ORCID id of authors, it uses the researchProducts endopoint to get the data for each of their publication, then it writes them in a CSV file containing surname-name string, DOI, title and publishing date of each publication.
- **251127_DatiPubblicazioneAnniInCSVDaCSV.py**  - From a CSV file in the same folder of the script containing name, surname, fiscal code and ORCID id of authors, it uses the researchProducts endopoint to get the data for their publication in a given years frame, then it writes them in a CSV file containing surname-name string, DOI, title, publishing year, type of publication and bibliographical data of each publication.
