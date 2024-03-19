import json

trigramme = "CCA"
num_strat = 2
num_mesure = 1

nom_fichier = f"{trigramme}_strat{num_strat}_mes{num_mesure}.json"
nom_dossier = "test/resultats"

def enregistrement(etat, nb_step):
    try :
        with open(f"{nom_dossier}/{nom_fichier}", 'r') as f:
            data = json.load(f)
        num = data[-1]['num'] + 1
    except FileNotFoundError:
        data = []
        num = 0
    
    data.append({'etat': etat, 'nb_step': nb_step, 'num': num})
    
    with open('data.json', 'w') as f:
        json.dump(data, f)
    
    return num

def mise_en_forme(texte):
    
    liste_phrase = texte.split('\n')
    data_final  = []
    
    for phrase in liste_phrase :
        if phrase in ['',
                      'Search and rescue',
                      '    Step',
                      '    About',
                      '    Reset',
                      'Frames Per Second',
                      '20',
                      '1']:
            phrase = ''
    
    liste_phrase_propre = [p 
                           for p in liste_phrase
                           if p != '']
    
    for i in range(len(liste_phrase_propre)):
        liste_phrase_propre[i] = liste_phrase_propre[i].replace('    ', '')
        liste_phrase_propre[i] = liste_phrase_propre[i].replace('Current Step: ', '')
    
    if   liste_phrase_propre[0] == 'Stop' : etat = 0
    elif liste_phrase_propre[0] == 'Done' : etat = 1
    elif liste_phrase_propre[0] == 'Start': etat = 2
    else : etat = -1
    
    nb_step = int(liste_phrase_propre[1])
    
    return etat, nb_step

num = 0
while True :
    texte = input(f" Entrée n°{num} : ")
    etat, nb_step = mise_en_forme(texte)
    num = enregistrement(etat, nb_step)
    print(f"Entrée n°{num} => Etat : {etat}, Nombre de step : {nb_step}")