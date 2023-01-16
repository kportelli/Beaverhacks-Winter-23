#Beaverhacks Winter 2023 Hackathon
#Theme "Health"
#Team WCYM
#Tyson Pederson, Kathryn Portelli, Brittany Stachkunis, Hannah Weeks

import requests
import sys

def main():
    print('It is not this applications intention to provide specific medical advice, but rather to provide users with information to better understand their health and their medications. You should consult with a qualified physician for advice about medications.', end='\n\n')
    print("This application is intended for educational and scientific research purposes only and you expressly acknowledge and agree that use of this application is at your sole risk. The accuracy of this application's information is not guaranteed and reliance on this application shall be at your sole risk. This application is not intended as a substitute for professional medical advice, diagnosis or treatment.", end='\n\n')
    patient_drugs = generate_list()
    if len(patient_drugs) == 0:
        print('No drugs were input')
        sys.exit()
    count = contra_checker(patient_drugs)
    if count == 1:
        print('There was', count,'interaction found.')
    else:
        print('There were', count,'interactions found.')

def generate_list():
    """Builds list of patient rxcuis"""
    patient_drugs = []
    response = "y"
    #prompt user for drug name, reprompt if invalid name given
    while response == "y":
        drug_name = input('Input drug name, or "done" if done: ')
        rxcui = drug_id_finder(drug_name)
        if rxcui != False and rxcui not in patient_drugs:
            patient_drugs.append(rxcui)
            response = input('Add another medication? Enter Y or N: ').lower()
            while response != "n" and response != "y":
                response = input('Response must be Y or N: ').lower()
        elif rxcui in patient_drugs:
            print("Please do not duplicate drug names.")
        elif drug_name.lower() == 'done':
            break
        else:
            print("Invalid drug name.")
    return patient_drugs

def drug_id_finder(drug_name):
    """Queries National Library of Medicine api to pull the rxcui of given drug"""
    api_url = (f'https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}')
    response = requests.get(api_url)
    try:
        response = response.json()
        rxcui = response["idGroup"]["rxnormId"][0]
    except:
        return False
    return rxcui

def contra_checker(patient_drugs):
    """Check all drugs in users drug list against each other for any interactions"""
    count = 0
    # Format list of drugs to be usable with api
    patient_drugs = '+'.join(patient_drugs)
    url = f'https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={patient_drugs}'
    response = requests.get(url).json()
    # Try to find interactions, if none are available return 0
    try:
        interaction_pairs = response['fullInteractionTypeGroup'][0]['fullInteractionType']
    except KeyError:
        return count
    # Print a warning with both drug names for each interaction found
    for pair in interaction_pairs:
        drug1 = pair['interactionPair'][0]['interactionConcept'][0]['minConceptItem']['name'].capitalize()
        drug2 = pair['interactionPair'][0]['interactionConcept'][1]['minConceptItem']['name'].capitalize()
        print(f'{drug1} may interact with {drug2}, you may want to talk to your doctor.')
        count += 1
    return count

if __name__ == '__main__':
    main()
