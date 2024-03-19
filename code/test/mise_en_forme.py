def mise_en_forme(trigramme, num_strat, num_mesure, extension):

    nom_fichier = f"{trigramme}_strat{num_strat}_mes{num_mesure}_brut.{extension}"
    nom_dossier = "test/resultats"
    data_final  = []

    with open(f"{nom_dossier}/{nom_fichier}", 'r') as file:
        data = file.readlines()
        data_propre = []
        
        for i in range(len(data)):
            if data[i] in ['\n',
                           'Search and rescue\n',
                           '    Step\n',
                           '    About\n',
                           '    Reset\n',
                           'Frames Per Second\n',
                           '20\n',
                           '1\n']:
                data[i] = ''
                
            if data[i] != '':
                data_propre.append(data[i])
        
        for i in range(len(data_propre)):
            data_propre[i] = data_propre[i].replace('    ', '')
            data_propre[i] = data_propre[i].replace('Current Step: ', '')
        i = 0
        while i != len(data_propre):
            if data_propre[i] in ('Start\n', 'Done\n', 'Stop\n'):
                if data_propre[i] == 'Start\n': etat = 0
                if data_propre[i] ==  'Done\n': etat = 1
                if data_propre[i] ==  'Stop\n': etat = 2
                
                data_final.append((etat, int(data_propre[i+1][:-1])))
            i+=1
    
    return data_final    