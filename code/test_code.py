import ast


class Parse:
    def __init__(self):
        self.error = None
        self.code = None

    def check_code(self, assignment):
        code = '\n'.join(self.code)
        globals_dict = {}

        try:
            ast.parse(code)
        except SyntaxError as e:
            return e  # Return SyntaxError object with error information
        try:
            # Execute assignment
            exec(assignment[1], globals_dict)
            assignment_result = globals_dict.get(assignment[0])

            written_code_str = "\n".join(self.code)
            exec(written_code_str, globals_dict)
            written_result = globals_dict.get(assignment[0])
            # Compare results
            if not assignment_result >= written_result or self.code[-1] == ['']:
                return ['Code is valid', 'Complete the quest']
            else:
                return None
        except Exception:
            return ['Code is valid', 'Complete the quest']     # Return SyntaxError object with error information

    def banned_words(self, banned):
        for line in self.code:
            if banned in line:
                # there is a banned word in the list
                return True
            else:
                pass
        # there is not a banned word in the list
        return False

    def ordered_word(self, ordered):
        for line in self.code:
            if ordered in line:
                # there is an ordered word in the list
                return True
            else:
                pass
        # there is not an ordered word in the list
        return False

    def log_errors(self):
        # The code is valid
        if self.error is None:
            return ['Well done!']
        # The code is invalid
        if self.error == ['Code is valid', 'Complete the quest']:
            return self.error
        else:
            messages = ["Error in Line " + str(self.error.lineno), str(self.error.msg)]
            return messages

    def update_code(self, preset_text, user_text):
        self.code = preset_text + user_text
