import requests
import json


def main():
    """?"""
    patient_drugs = ["10171"]
    drug_name = input('input drug name')
    rxcui = drug_id_finder(drug_name)
    if rxcui != False:
        patient_drugs.append(rxcui)
    else:
        print("invalid drug name")
    contra_checker(patient_drugs)
def drug_id_finder(drug_name):
    """returns the rxcui of a given drug"""
    api_url = (f'https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}')
    response = requests.get(api_url)
    try:
        response = response.json()
        rxcui = response["idGroup"]["rxnormId"][0]
    except:
        return False
    return rxcui

#Once RxCUI numbers are in the list, start iterating through the list and check for references of all other drugs in the list
def contra_checker(patient_drugs):
    for i, drug in enumerate(patient_drugs):
        print(i, drug)
        url = (f'https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui={drug}')
        #&sources=ONCHigh
        response = requests.get(url).json()
        interaction_pairs = response["interactionTypeGroup"][0]["interactionType"][0]["interactionPair"]
        for pair in interaction_pairs:
            pair_rxcui = pair["interactionConcept"][1]["minConceptItem"]["rxcui"]
            if pair_rxcui in patient_drugs:
                print(pair["description"])


if __name__ == '__main__':
  main()


