import ast


class Parse:
    def __init__(self):
        self.error = None
        self.error_message = None
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
            exec(assignment['Rule'], globals_dict)
            assignment_result = globals_dict.get(assignment['Keyword'])

            written_code_str = "\n".join(self.code)
            exec(written_code_str, globals_dict)
            written_result = globals_dict.get(assignment['Keyword'])
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
                # there is not a banned word in the list
                self.error_message = ['You are using banned words:', banned]

    def ordered_word(self, ordered):
        for line in self.code:
            if ordered not in line:
                # there is not an ordered word in the list
                self.error_message = ['You are not using ordered words:', ordered]

    def log_errors(self):
        # The code is valid
        if self.error is None:
            return ['Well done!']
        # The code is invalid
        if self.error == ['Code is valid', 'Complete the quest']:
            return self.error
        else:
            self.error_message = ["Error in Line " + str(self.error.lineno), str(self.error.msg)]

    def update_code(self, preset_text, user_text):
        if isinstance(preset_text, list):
            preset_text = ''.join(preset_text)
        self.code = preset_text + ''.join(user_text)
