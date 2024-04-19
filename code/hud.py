from dialogwindow import *


class HUD:
    def __init__(self, dialog_window):
        # general
        self.globals = GlobalVariables()
        self.dialog_window = dialog_window

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(self.globals.FONT, self.globals.FONT_SIZE)
        self.dialog_color = (200, 200, 200)
        self.text_color = 'red'
        self.pos = pygame.Vector2(870, 600)
        self.width = 400
        self.height = 200
        self.text = []
        self.lines = None
        self.line_heights = 0

        self.hint_rect = pygame.Rect(650, 55, 100, 60)
        self.hint_color = 'black'

    def display_console_window(self):
        """
        Calling the function will display the console error window. Argument msg can display an error message.

        :param msg:
        :return:
        """
        console_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        pygame.draw.rect(self.display_surface, 'black', console_rect)

        font = pygame.font.Font(self.globals.FONT, 30)
        text_surf_name = font.render('Log Console', False, 'white')
        text_rect_name = pygame.Rect(self.pos.x + 10, self.pos.y + 10, self.width, self.height)
        self.display_surface.blit(text_surf_name, text_rect_name)

        self.display_message()

    def display_message(self):
        if not self.text == []:
            font = pygame.font.Font(self.globals.FONT, 26)
            for i, row in enumerate(self.text):
                text_surf = font.render(row[0], True, self.text_color)
                text_width, text_text_height = text_surf.get_size()
                self.display_surface.blit(text_surf, (self.pos.x + 30, self.pos.y + 55 + i * text_text_height))

    def display_hint(self):
        font = pygame.font.Font(self.globals.FONT, 50)
        text_surf_name = font.render('Hint', False, self.hint_color)
        self.display_surface.blit(text_surf_name, self.hint_rect)

    def format_message(self, message):

        lines, self.line_heights = self.dialog_window.split_lines(message, 600)

        self.text = [[' '.join(row[0])] for row in lines]

