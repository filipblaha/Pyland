from globalvariables import *


class HUD:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        self.dialog_color = (200, 200, 200)
        self.text_color = (0, 0, 0)
        self.pos = pygame.Vector2(680, 700)

        self.hint_rect = pygame.Rect(520, 40, 80, 30)

    def display_error_window(self, msg=None, msg_color=None):
        """
        Calling the function will display the console error window. Argument msg can display an error message.

        :param msg:
        :param msg_color:
        :return:
        """
        pygame.draw.rect(self.display_surface, 'black', (self.pos.x, self.pos.y, 335, 200))

        font = pygame.font.Font(FONT, 18)
        text_surf_name = font.render('Log Console', False, 'white')
        text_rect_name = text_surf_name.get_rect(topleft=(self.pos.x + 10, self.pos.x + 10))
        self.display_surface.blit(text_surf_name, text_rect_name)

        if msg is not None:
            self.show_error(msg, msg_color)

    def show_error(self, msg, msg_color):

        font = pygame.font.Font(FONT, 18)
        for i, row in enumerate(msg):
            text_surf = font.render(row, True, msg_color)
            text_width, text_text_height = text_surf.get_size()
            self.display_surface.blit(text_surf, (self.pos.x + 40, self.pos.x + 40 + i * text_text_height))

    def show_hint(self):
        font = pygame.font.Font(FONT, 25)
        text_surf_name = font.render('Hint', False, 'black')
        self.display_surface.blit(text_surf_name, self.hint_rect)
