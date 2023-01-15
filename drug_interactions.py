import requests
import json


def main():
    """?"""
    print('It is not this applications intention to provide specific medical advice, but rather to provide users with information to better understand their health and their medications. You should consult with a qualified physician for advice about medications.', end='\n\n')
    print("This application is intended for educational and scientific research purposes only and you expressly acknowledge and agree that use of this application is at your sole risk. The accuracy of this application's information is not guaranteed and reliance on this application shall be at your sole risk. This application is not intended as a substitute for professional medical advice, diagnosis or treatment.", end='\n\n')
    
    patient_drugs = ["10171", '153010']

    drug_name = input('Input drug name: ')
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
    """Check all drugs in users drug list against each other for any interactions"""
    for i, drug in enumerate(patient_drugs[:len(patient_drugs) - 1]):
        url = (f'https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui={drug}')
        response = requests.get(url).json()
        interaction_pairs = response["interactionTypeGroup"][0]["interactionType"][0]["interactionPair"]
        for pair in interaction_pairs:
            pair_rxcui = pair["interactionConcept"][1]["minConceptItem"]["rxcui"]
            pair_name = pair["interactionConcept"][1]["minConceptItem"]["name"]
            drug_name = pair["interactionConcept"][0]["minConceptItem"]["name"]
            if pair_rxcui in patient_drugs[i+1:]:
                print(f'{drug_name.capitalize()} may interact with {pair_name.capitalize()}, you may want to talk your doctor.')


if __name__ == '__main__':
    main()
