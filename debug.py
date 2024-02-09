# Zadání
zadani = """
wizard_health = 10
if wizard_health > 0:
    wizard_health -= 10
"""

# Napsaný kód (list s řádky kódu)
napsany_kod = [
    "wizard_health = 10",
    "if wizard_health > 0:",
    "    wizard_health -= 10"
]

# Funkce pro kontrolu výsledků
def kontrola_vysledku(zadani, napsany_kod):
    # Globální slovník pro vykonání kódu
    globals_dict = {}

    try:
        # Spustit zadání
        exec(zadani, globals_dict)
        zadani_vysledek = globals_dict.get('wizard_health')

        # Spustit napsaný kód
        napsany_kod_str = "\n".join(napsany_kod)
        exec(napsany_kod_str, globals_dict)
        napsany_vysledek = globals_dict.get('wizard_health')

        # Porovnat výsledky
        if zadani_vysledek == napsany_vysledek:
            print("Napsaný kód dosahuje stejného výsledku jako zadání.")
        else:
            print("Napsaný kód nedosahuje stejného výsledku jako zadání.")
    except Exception as e:
        print("Chyba při vykonávání kódu:", e)

# Zkontrolovat výsledky
kontrola_vysledku(zadani, napsany_kod)