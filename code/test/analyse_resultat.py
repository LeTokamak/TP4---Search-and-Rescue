from mise_en_forme import mise_en_forme
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt

import os
import pandas as pd

LECTURE_BATCH = True
dossier_resultat = "code/test/resultats"

trigramme = "CCA"
strat = 3

if not LECTURE_BATCH:

    mesure = 1
    extension = "txt"
    donnee_brut = mise_en_forme(trigramme, strat, mesure, extension)

    a = [i[0] for i in donnee_brut]

    nb_0 = a.count(0)
    nb_1 = a.count(1)
    nb_2 = a.count(2)
    print(f"Nombre de 0: {nb_0}")
    print(f"Nombre de 1: {nb_1}")
    print(f"Nombre de 2: {nb_2}")

    START = 0
    DONE = 1
    STOP = 2

    donnee_bug = [value[1]
                for value in donnee_brut 
                if value[0] == START]

    donnee_reussite = [value[1]
                    for value in donnee_brut 
                    if value[0] == DONE]

    donnee_echec = [value[1]
                for value in donnee_brut 
                if value[0] == STOP and value[1] > 450]

    donnee_plantage = [value[1]
                    for value in donnee_brut 
                    if value[0] == STOP and value[1] <= 450]

    donnee_propre = donnee_reussite + donnee_echec
    
    print(f"\nNombre de bug: {len(donnee_bug)}")
    print(f"Nombre de réussite: {len(donnee_reussite)}")
    print(f"Nombre de échec: {len(donnee_echec)}")
    print(f"Nombre de plantage: {len(donnee_plantage)}")
    print(f"\nNombre de données propres: {len(donnee_propre)}")
    print(f"Nombre de données brutes: {len(donnee_brut)}")

else :
    liste_data = []
    mesure = "*"
    for file in os.listdir(dossier_resultat):
        if file.endswith(".csv") and "batch" in file and trigramme in file and str(strat) in file:
            liste_data.append(pd.read_csv(f"{dossier_resultat}/{file}"))
        
    donnee_brut = pd.concat(liste_data, axis=0, ignore_index=True)
    donnee_brut = donnee_brut.drop(["RunId", "iteration", "items", "Delivered", "Unnamed: 0"], axis=1)
    
    donnee_brut = list(donnee_brut["Step"])
    
    donnee_reussite = [ value
                        for value in donnee_brut 
                        if value != 1000]

    donnee_echec = [value
                    for value in donnee_brut 
                    if value == 1000]
    
    donnee_propre = donnee_reussite + donnee_echec
        
        



# === Gestion des échecs ===
nb_echec = len(donnee_echec)
pourcentage_echec = (nb_echec*100 / len(donnee_propre))

# === Paramètres de la loi normale ===
mu = np.mean(donnee_reussite)
sigma = np.std(donnee_reussite)

# === Intervalle de confiance ===
n = len(donnee_reussite)
alpha = 0.95  # Confidence level
z = 1.96  # Z-score for 95% confidence level

ci_mu = (mu - z * (sigma / np.sqrt(n)), mu + z * (sigma / np.sqrt(n)))
ci_sigma = (sigma * np.sqrt((n - 1) / chi2.ppf((1 + alpha) / 2, n - 1)), sigma * np.sqrt((n - 1) / chi2.ppf((1 - alpha) / 2, n - 1)))

print(f"Intervalle de confiance pour mu: {ci_mu}")
print(f"Intervalle de confiance pour sigma: {ci_sigma}")


# === Graphique ===
fig, ax1 = plt.subplots()

ax1.hist(donnee_reussite, bins=100)
ax1.set_xlabel('Nombre de step')
ax1.set_ylabel("Fréquence sur l'histogramme")

ax2 = ax1.twinx()
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
y = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2))
ax2.plot(x, y, 'r', label=f"Loi normale, centré sur {round(mu, 2)} d'écart-type {round(sigma, 2)}")
ax2.set_ylabel("Loi normale")
ax2.legend(loc='upper right')

fig.suptitle(f"Test de la stratégie {strat} de {trigramme} (mesure n°{mesure})", fontsize=16)
ax1.set_title(f"{len(donnee_reussite)} réussites et {nb_echec} échecs (soit {round(pourcentage_echec, 2)}% d'échec)")
fig.show()
plt.show()

"""
top=0.88,
bottom=0.11,
left=0.11,
right=0.88,
hspace=0.2,
wspace=0.2
"""