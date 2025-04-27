import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from pathlib import Path
from Models.Molecule import Molecule

# PART 3 START
TDDFTTDA_list = [] # Alle TDDFT/TDA" waarden
TDDFT_list = [] # Alle TDDFT waarden

files_dir = "files"

dat_files = list(Path(files_dir).rglob("*.dat")) # Alle .dat bestanden
out_files = list(Path(files_dir).rglob("*.out")) # Alle .out bestanden
# We gaan door 1 van de lijsten 
# We hebben enkel de idx van de loop nodig, de lijsten zijn even groot door welke lijst je loopt maakt niet uit
for idx, file in enumerate(dat_files):
    # We maken een molucule object voor elke molecule
    # We geven de .out- en .dat bestand mee
    molucule = Molecule(str(out_files[idx]), str(dat_files[idx]))

    # We gaan hier de TDDFT/TDA waarden toevoegen aan onze grote lijst ( zie lijn 9 )
    TDDFTTDA_list.extend(molucule.return_possible_excited_states("TDDFT/TDA"))
    # We gaan hier de TDDFT waarden toevoegen aan onze grote lijst ( zie lijn 10 )
    TDDFT_list.extend(molucule.return_possible_excited_states("TDDFT"))
# We maken van de grote lijsten Numpy Arrays deze zijn sneller + scikit-learn accepteert alleen Numpy arrays
TDDFTTDA_array = np.array(TDDFTTDA_list).reshape(-1, 1) # We zetten de lijst om naar een 2D array ( LinearRegression().fit(X, y) accepteert enkel 2D arrays voor X)
TDDFT_array = np.array(TDDFT_list)

model = LinearRegression() # We maken onze regressie model
model.fit(TDDFTTDA_array, TDDFT_array) # Trein het model ( Hij gaat gwn die waarden doornemen en dan kan hij later een voorspelling maken "dalen of stijgen ze?" )

y_pred = model.predict(TDDFTTDA_array) # Hier maakt hij dan de voorspelling

diff = model.score(TDDFTTDA_array, TDDFT_array) # Dit is onze R² (determinatiecoëfficiënt)
# Hier gaan we het plot tekenen
plt.figure()
plt.scatter(TDDFTTDA_array, TDDFT_array, label="Molecullen") # Ik toon de molecullen ( ik ben niet zeker of het moet )
plt.plot(TDDFTTDA_array, y_pred, color='red', label=f'R^2 = {diff:.3f}') # Ik toon de waarde van R²
plt.xlabel('TDDFT/TDA excitation energies (eV)') # Wat betekenen de waarden van de X as?
plt.ylabel('TDDFT excitation energies (eV)') # Wat betekenen de waarden van de Y as?
plt.legend() # Toon zo een box met de betekenis van de kleurtjes 😎
plt.grid(True) # Een grid, de vakjes


# PART 3 FINISH

# PART 4 TEST

m = Molecule(out_files[0], dat_files[0]) # We maken hier een Molecule object met het eerste .dat- en .out bestand

m.draw_plot_of_spectrum() # We roepen de methode op

# PART 4 FINISH 