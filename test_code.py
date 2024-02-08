import ast


def check_code(code_lines):
    code = '\n'.join(code_lines)
    try:
        ast.parse(code)
        return None  # No errors found
    except SyntaxError as e:
        return e  # Return SyntaxError object with error information


def log_errors(code_lines, error):
    # The code is valid
    if error is None:
        return True

    # The code is invalid
    else:
        print("Code contains a syntax error:")
        print("On line", error.lineno, "there is an error:", error.msg)
        print("Code snippet near the error:", code_lines[error.lineno - 1])
        print(" " * (error.offset + 10) + "^")  # Show where the error starts with a caret
