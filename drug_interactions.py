#Beaverhacks Winter 2023 Hackathon
#Theme "Health"
#Team WYCM
#Tyson Pederson, Kathryn Portelli, Brittany Stachkunis, Hannah Weeks

import requests
def main():
    print('It is not this applications intention to provide specific medical advice, but rather to provide users with information to better understand their health and their medications. You should consult with a qualified physician for advice about medications.', end='\n\n')
    print("This application is intended for educational and scientific research purposes only and you expressly acknowledge and agree that use of this application is at your sole risk. The accuracy of this application's information is not guaranteed and reliance on this application shall be at your sole risk. This application is not intended as a substitute for professional medical advice, diagnosis or treatment.", end='\n\n')

    patient_drugs = generate_list()
    count = contra_checker(patient_drugs)
    print('There were', count,'interactions found.')

def generate_list():
    #"10171" advil, '153010'
    patient_drugs = []
    response = "y"
    while response == "y":
        drug_name = input('Input drug name: ')
        rxcui = drug_id_finder(drug_name)
        if rxcui != False and rxcui not in patient_drugs:
            patient_drugs.append(rxcui)
            response = input('Add another medication? Enter Y or N: ').lower()
            while response != "n" and response != "y":
                response = input('Response must be Y or N: ').lower()
        elif rxcui in patient_drugs:
            print("Please do not duplicate drug names.")
        else:
            print("Invalid drug name.")
    return patient_drugs


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


def contra_checker(patient_drugs):
    """Check all drugs in users drug list against each other for any interactions"""
    count = 0
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
                count = count + 1
    return count


if __name__ == '__main__':
    main()
