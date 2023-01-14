import requests
import json

drug_name = input('input drug name')
api_url = (f'https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui={drug_name}&sources=DrugBank')
response = requests.get(api_url)
print(json.dumps(response.json(), indent=2))
