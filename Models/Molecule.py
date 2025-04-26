# PART 1 START
class Molecule:
    def __init__(self, out_path: str, dat_path: str):
        self.out_path = out_path
        self.dat_path = dat_path
   
    # PART 1 FINISH

    # PART 2 START
    
    def returnPossibleExcitedState(self, key_word: str):
        start_marker = ""
        end_marker = ""

        if key_word == "TDDFT/TDA":
            # Achter deze lijn vinden we de info die we nodig hebben (eV)
            start_marker = "         TDDFT/TDA Excitation Energies              "
            # Wat na deze lijn staat intereseert ons niet
            end_marker = " Direct TDDFT calculation will be performed"
        elif key_word == "TDDFT":
            # Achter deze lijn vinden we de info die we nodig hebben (eV)
            start_marker = "             TDDFT Excitation Energies              "
            # Wat na deze lijn staat intereseert ons niet
            end_marker = " Starting SETmanPost()"

        energies = []
        # Hier gaan we het bestand openen zodat we deze kunnen lezen
        with open(self.out_path) as file:
            # We gaan eerst alles doorlezen en opslaan, dit maakt het filteren later makkelijker
            lines = file.readlines()
        # Dit houd het nummer van de lijn waar achter de info zit die we nodig hebben
        start_idx = None
        # We gaan door alle lijnen in ons bestand
        for idx, line in enumerate(lines):
            # Is de lijn gelijk aan een marker?
            if start_marker in line:
                # Dan gaan we de index bijhouden in onze variable
                start_idx = idx
                break

        # Hier geld hetzelfde als bij het starten
        end_idx = None
        # We gaan hier alleen door de lijnen die na onze start lijn komen
        for idx, line in enumerate(lines[start_idx:], start=start_idx):
            if end_marker in line:
                end_idx = idx
                break
        # We hebben nu de sectie waarin onze info zit (eV energies)
        # Nu gaan we erdoor zoeken
        for line in lines[start_idx:end_idx]:
            # Staat "excitation energy (eV) ="  in een lijn?
            if "excitation energy (eV) =" in line:
                try:
                    # Gaan we de info ophalen die na de '=' staat en escape characters er uit halen (\n, \b...)
                    energy_str = line.split('=')[1].strip()
                    # We zetten de string om naar een komma getal
                    energy = float(energy_str)
                    # We gaan die aan 'energies' toevoegen (zie lijn 26)
                    energies.append(energy)
                except (ValueError, IndexError):
                    continue
        # We geven de lijst terug
        return energies

        
    # PART 2 FINISH
