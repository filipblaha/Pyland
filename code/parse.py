import ast


class Parse:
    def __init__(self):
        self.error = None
        self.console_message = None
        self.code = None

    def check_code(self, assignment):
        globals_dict = {}

        try:
            ast.parse(self.code)
        except SyntaxError as error:
            self.log_errors(error)  # Return SyntaxError object with error information
            return
        try:
            # Execute assignment
            exec(assignment['Rule'], globals_dict)
            assignment_result = globals_dict.get(assignment['Keyword'])

            exec(self.code, globals_dict)
            written_result = globals_dict.get(assignment['Keyword'])
            # Compare results
            if not assignment_result >= written_result or self.code[-1] == ['']:
                self.log_errors('Code is valid. Complete the task')
                return
            else:
                self.log_errors('Well done!')
                return
        except Exception:
            self.log_errors('Code is valid. Complete the task')

    def banned_words(self, banned):
        for line in self.code:
            if banned in line:
                # there is not a banned word in the list
                self.console_message = ['You are using banned words:', banned]

    def ordered_word(self, ordered):
        for line in self.code:
            if ordered not in line:
                # there is not an ordered word in the list
                self.console_message = ['You are not using ordered words:', ordered]

    def log_errors(self, message):
        # The code is valid
        if message == 'Well done!':
            self.console_message = message
        elif message == 'Code is valid. Complete the task':
            self.console_message = message
        # The code is invalid
        else:
            self.console_message = "Error in Line " + str(message.lineno) + str(message.msg)

    def update_code(self, preset_text, user_text):
        if isinstance(preset_text, list):
            preset_text = ''.join(preset_text)
        self.code = preset_text + ''.join(user_text)
