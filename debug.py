import ast


def find_syntax_errors(code_lines):
    code = '\n'.join(code_lines)
    try:
        ast.parse(code)
        return None  # No errors found
    except SyntaxError as e:
        return e  # Return SyntaxError object with error information


def log_errors(error):
    if error is None:
        print("Code is valid.")
        # You can perform further checks and run the player's code here
    else:
        print("Code contains a syntax error:")
        print("On line", error.lineno, "there is an error:", error.msg)
        print("Code snippet near the error:", example_code_lines[error.lineno - 1])
        print(" " * (error.offset + 10) + "^")  # Show where the error starts with a caret


# Example code lines
example_code_lines = [
    "wizard_lives = 10",
    "my_damage = 1",
    "",
    "for i in range(10):s",
    "   wizard_lives - hurt_wizard",
    ""
]

errors = find_syntax_errors(example_code_lines)
log_errors(errors)

