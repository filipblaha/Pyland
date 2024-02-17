from globalvariables import *


class HUD:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        self.max_chars_in_row = 20

        self.hint_rect = pygame.Rect(520, 40, 80, 30)

    def show_dialog(self, text, pos_x, pos_y, width, height):
        lines = self.split_lines(text, width - 40)
        dialog_height = len(lines) * 40 + 20
        dialog_rect = pygame.Rect(pos_x - width // 2, pos_y - dialog_height // 2, width, dialog_height)
        pygame.draw.rect(self.display_surface, self.dialog_color, dialog_rect)
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(pos_x, pos_y - dialog_height // 2 + 20 + i * 40))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def split_lines(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + ' ' + word if current_line != '' else word
            if self.font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def show_error_window(self):
        pygame.draw.rect(self.display_surface, 'black', (680, 450, 335, 200))

        font = pygame.font.Font(FONT, 18)
        text_surf_name = font.render('Log Console', False, 'white')
        text_rect_name = text_surf_name.get_rect(topleft=(690, 460))
        self.display_surface.blit(text_surf_name, text_rect_name)

    def show_error(self, message):
        if message == ['Well done!']:
            color = 'green'
        elif message == ['Code is valid', 'Complete the quest']:
            color = 'yellow'
        else:
            color = 'red'

        font = pygame.font.Font(FONT, 18)
        for i, row in enumerate(message):
            text_surf = font.render(row, True, color)
            text_width, text_text_height = text_surf.get_size()
            self.display_surface.blit(text_surf, (720, 490 + i * text_text_height))

    def show_hint(self):
        font = pygame.font.Font(FONT, 25)
        text_surf_name = font.render('Hint', False, 'black')
        self.display_surface.blit(text_surf_name, self.hint_rect)
