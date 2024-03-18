from mise_en_forme import mise_en_forme
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt

trigramme = "CCA"
strat = 2
mesure = 1
extension = "txt"
donnee_brut = mise_en_forme(trigramme, strat, mesure, extension)

print(donnee_brut)

donnee_reussite = [value[1]
                  for value in donnee_brut 
                  if value[0] == 1]

donnee_echec = [value[1]
               for value in donnee_brut 
               if value[0] == 0 and value[1] > 600]

donnee_plantage = [value[1]
                  for value in donnee_brut 
                  if value[0] == 0 and value[1] <= 600]

# === Gestion des échecs ===
nb_echec = len(donnee_echec)
pourcentage_echec = (nb_echec / len(donnee_brut)) * 100

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