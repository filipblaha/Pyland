def check_results(assignment, written_code):
    if not written_code:
        print("No code provided for comparison.")
        return

    globals_dict = {}

    try:
        exec(assignment, globals_dict)
        assignment_result = globals_dict.get('wizard_health')

        for line in written_code:
            if line.strip():  # Zkontroluje, zda je řádek neprázdný po odstranění bílých znaků
                exec(line, globals_dict)

        written_result = globals_dict.get('wizard_health')

        if assignment_result == written_result:
            print("The written code achieves the same result as the assignment.")
        else:
            print("The written code does not achieve the same result as the assignment.")
    except Exception as e:
        print("Error executing code:", e)

# Příklad použití
assignment = 'wizard_health = 0'

written_code = ["wizard_health = 1", " "]

check_results(assignment, written_code)
