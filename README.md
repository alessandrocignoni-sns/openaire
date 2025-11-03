# SVR's OpenAIRE scripts
Python 3 scripts, useful to Research Assessment and Open Science Service of Scuola Normale Superiore.

Necessary libraries:

    requests

## Scripts English description
Code is written and commented in Italian. Here a brief description of the scripts:
- **251030_DatiPubblicazioniInCSVDaAutore.py** - From author ORCID id, it uses the researchProducts endopoint to gets the data for each of their publication, then it writes them in a CSV file containing DOI, title and publishing date of each publication.
- **251103_DatiPubblicazioniInCSVDaOrganizzazione.py** - From institution ROR id, first it uses the organization endopoint to gets the OpenAIRE id of the organization, secondly for each of its works, it uses the researchProducts endopoint to gets the data for each of their publication then it writes them in a CSV file containing OpenAlex id, DOI, title and publishing date of each publication.
