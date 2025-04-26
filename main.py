import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from pathlib import Path
from Models.Molecule import Molecule

# PART 3 START
TDDFTTDA_list = []
TDDFT_list = []

files_dir = "files"

dat_files = list(Path(files_dir).rglob("*.dat"))
out_files = list(Path(files_dir).rglob("*.out"))

for idx, file in enumerate(dat_files):
    molucule = Molecule(str(out_files[idx]), str(dat_files[idx]))

    TDDFTTDA_list.extend(molucule.returnPossibleExcitedState("TDDFT/TDA"))
    TDDFT_list.extend(molucule.returnPossibleExcitedState("TDDFT"))

TDDFTTDA_array = np.array(TDDFTTDA_list).reshape(-1, 1)
TDDFT_array = np.array(TDDFT_list)

model = LinearRegression()
model.fit(TDDFTTDA_array, TDDFT_array)

y_pred = model.predict(TDDFTTDA_array)

diff = model.score(TDDFTTDA_array, TDDFT_array)  

plt.scatter(TDDFTTDA_array, TDDFT_array, label="Molecullen")
plt.plot(TDDFTTDA_array, y_pred, color='red', label=f'R^2 = {diff:.3f}')
plt.xlabel('TDDFT/TDA excitation energies (eV)')
plt.ylabel('TDDFT excitation energies (eV)')
plt.legend()
plt.grid(True)
plt.show()

# PART 3 FINISH