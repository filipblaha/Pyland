import ast


def check_code(assignment, written_code):
    # Vytvoříme AST pro zadání
    assignment_ast = ast.parse(assignment)

    # Získáme názvy proměnných použitých v zadání
    assignment_vars = {node.id for node in ast.walk(assignment_ast) if isinstance(node, ast.Name)}

    # Pro každý řádek napsaného kódu
    for line in written_code:
        # Pokud je řádek prázdný nebo obsahuje jen bílé znaky, přeskočíme ho
        if not line.strip():
            continue

        # Vytvoříme AST pro daný řádek
        code_ast = ast.parse(line)

        # Projdeme AST a hledáme příkazy nastavení proměnných
        for node in ast.walk(code_ast):
            if isinstance(node, ast.Assign):
                # Získáme názvy proměnných nastavených v tomto příkazu
                assigned_vars = {target.id for target in node.targets if isinstance(target, ast.Name)}

                # Zkontrolujeme, zda je proměnná 'wizard' nastavena na 1
                if 'wizard' in assigned_vars:
                    # Pro každou proměnnou, která byla přiřazena, zkontrolujeme, zda se shoduje s hodnotou
                    for var in assigned_vars:
                        if var in assignment_vars:
                            print(f"Proměnná '{var}' se nastavuje na hodnotu v rámci úkolu, který jste obdrželi.")
                        else:
                            print(f"Proměnná '{var}' se nastavuje na hodnotu, která není součástí zadání.")
                            # Zde můžete přidat další logiku pro porovnání hodnoty s očekávanou hodnotou
                else:
                    print("Řádek neobsahuje přiřazení proměnné 'wizard'.")
            else:
                print("Řádek neobsahuje přiřazení.")


# Příklad použití
assignment = 'wizard = 0'
written_code = ['wizard = 3',
                'for i in range(2):',
                '   wizard -= 1']

check_code(assignment, written_code)