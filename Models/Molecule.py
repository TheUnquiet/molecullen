import numpy as np
import matplotlib.pyplot as plt

# PART 1 START
class Molecule:
    def __init__(self, name: str, out_path: str, dat_path: str):
        self.name = name # We geven hier de naam
        self.out_path = out_path
        self.dat_path = dat_path
   
    # PART 1 FINISH

    # PART 2 START
    
    def return_possible_excited_states(self, key_word: str):
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

    # PART 4 START
    def draw_plot_of_spectrum(self):
        wavelengths = [] # X as waarden ( golflengte )
        intensity = [] # Y as waarden ( intensiteit )

        # We gaan hier de waarden die we inlezen opslaan
        initial_value = None 
        final_value = None
        increment = None

        # We gaan het bestand openen
        with open(self.dat_path) as file:
            # We houden alle lijnen die in het bestand staan
            lines = file.readlines()
        # We gaan door alle lijnen
        for line in lines:
            # Bevat de lijn die we nu lezen de string INITIAL_VALUE = ?
            if "INITIAL_VALUE =" in line:
                # Slagen we de waarde na de '=' zonder spaties en ' (nm)' op in initial_value
                initial_value = float(line.split('=')[1].strip().strip(' (nm)'))
            # Bevat de lijn die we nu lezen de string FINAL_VALUE = ?
            elif "FINAL_VALUE =" in line:
                # Slagen we de waarde na de '=' zonder spaties en ' (nm)' op in final_value
                final_value = float(line.split('=')[1].strip().strip(' (nm)'))
            # Bevat de lijn die we nu lezen de string INCREMENT = ?
            elif "INCREMENT =" in line:
                # Slagen we de waarde na de '=' zonder spaties en ' (nm)' op in increment
                increment = float(line.split('=')[1].strip().strip(' (nm)'))
        # Als al onze variabelen ingevuld zijn ( dus niet gelijk aan None )
        if initial_value is not None and final_value is not None and increment is not None:
            # Gaan we een numpy array maken van alle waarden tussen initial_value (350 nm) tot en met final_value (800 nm)
            # Met als tussen stap increment (.1)
            wavelengths = np.arange(initial_value, final_value + increment, increment)
        # We gaan opnieuw doo alle lijnen 
        for line in lines:
            # Deze lijnen hebben we niet meer nodig
            if "UV/VIS SPECTRUM" in line or "INITIAL_VALUE" in line or "FINAL_VALUE" in line or "INCREMENT" in line:
                # Skip deze lijnen maar
                continue
            # Nu zitten we aan onze getallen 
            # Hier gaat het om deze lijnen:
            # 0.13481318392405361	0.1518190799237463	0.10441803963696514	0.11449534998528905	0.1563535194936834
            # Deze lijn gaan we dan splitsen omdat we alle getallen apart nodig hebben
            # In de split() methode geven we niets mee, dit is omdat de spaties niet overal hetzelfde
            for value in line.split():
                try:
                    # We gaan elk getal in onze intensity lijst stoppen 
                    intensity.append(float(value)) # We maken eerst een kommagetal van onze waarde, hij is anders van type string
                except ValueError: # Als we op een of andere manier toch geen getal lezen gooien we een fout
                    continue # We doen verder dan gwn door met het lezen van de waarden in de split() methode
        # We gaan nu eindelijk een plot tekenen
        plt.figure() # Hierdoor kunnen wij meerdere plots op scherm laten zien
        plt.plot(wavelengths, intensity) # We gaan hier de grafiek tekenen, x as is de golflengte en y as de intensiteit (zie word doc)
        plt.title(f"{self.name} spectrum") # We zetten er een mooi titeltje bij met de naam van de moleculle, nu weten wij over welke het gaat! 😉
        plt.xlabel('Wavelength (nm)') # Wat is de betekenis van de x as?
        plt.ylabel('Intensity') # Wat is de betekenis van de y as?
        plt.grid(True) # Mooie vakje achter de grafiek 😎
        
    # PART 4 FINISH