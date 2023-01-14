import requests
import json

patient_drugs = []
def main():
    drug_name = input('input drug name')
    rxcui = drug_id_finder(drug_name)
    if rxcui != False:
        patient_drugs.append(rxcui)
    else:
        print("invalid drug name")
    print(patient_drugs)
def drug_id_finder(drug_name):
    api_url = (f'https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}')
    response = requests.get(api_url)
    try:
        response = response.json()
        rxcui = response["idGroup"]["rxnormId"][0]
    except:
        return False
    return rxcui

if __name__ == '__main__':
  main()