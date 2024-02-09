import ast


def check_code(code_lines, assignment):
    code = '\n'.join(code_lines)
    globals_dict = {}

    try:
        ast.parse(code)
    except SyntaxError as e:
        return e  # Return SyntaxError object with error information
    try:
        # Execute assignment
        exec(assignment[1], globals_dict)
        assignment_result = globals_dict.get(assignment[0])

        # Execute written code
        written_code_str = "\n".join(code_lines)
        exec(written_code_str, globals_dict)
        written_result = globals_dict.get(assignment[0])

        # Compare results
        if not assignment_result == written_result or code_lines == ['']:
            return ['Code is valid', 'Complete the quest']
        else:
            return None
    except Exception:
        return ['Code is valid', 'Complete the quest']     # Return SyntaxError object with error information


def log_errors(code_lines, error):
    # The code is valid
    if error is None:
        return  ['Well done!']
    # The code is invalid
    if error == ['Code is valid', 'Complete the quest']:
        return error
    else:
        messages = ["Error in Line " + str(error.lineno), str(error.msg)]
        return messages
