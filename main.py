from Models.Molecule import Molecule
# PART 1 START
m = Molecule("files/Cyanidin_H_tddft_short.out", "files/Cyanidin_H_tddft_full_simspec.dat");

# PART 1 FINSIH

# PART 2 START
print("TDDFT Energies eV")

for i in m.returnPossibleExcitedState("TDDFT"):
    print(i)

print("TDDFT/TDA Energies eV")

for i in m.returnPossibleExcitedState("TDDFT/TDA"):
    print(i)

# PART 2 FINISH
