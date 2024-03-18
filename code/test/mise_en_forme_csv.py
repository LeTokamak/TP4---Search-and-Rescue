def mise_en_forme_csv(trigramme, num_strat, num_mesure):

    nom_fichier = f"{trigramme}_strat{num_strat}_mes{num_mesure}_brut.csv"
    nom_dossier = "test/resultats"

    with open(f"{nom_dossier}/{nom_fichier}", 'r') as file:
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].replace(';;', '\n')
            data[i] = data[i].replace(';' , ''  )
            
        data = ''.join(data)
        data = data.split('\n')
        for i in range(len(data)):
            data[i] = int(data[i])
        return data