import pygame
from settings import *


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.max_chars_in_row = 20

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat ti pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, current_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = 0 + 20
        text_rect = text_surf.get_rect(topright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(5, 5))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(5, 5), 3)

    def display(self, player, displayed):
        # self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        pass
        # self.show_exp(displayed)

    def show_dialog_window(self, message, x, y, width, height, font_size, pos='center', color='black'):

        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        dialog_window_surf = pygame.image.load('graphic/dialog_window.png').convert()
        dialog_window_surf = pygame.transform.scale(dialog_window_surf, rect.size)
        dialog_window_surf.set_alpha(200)  # alpha level
        self.display_surface.blit(dialog_window_surf, rect)

        if not message == '':
            self.show_dialog_text(message, x, y, font_size, pos, color)

    def show_dialog_text(self, message, x, y, font_size, pos='center', color='black'):

        self.font = pygame.font.Font(UI_FONT, font_size)
        text_surf = self.font.render(str(message), False, color)

        if pos == 'center':
            text_rect = text_surf.get_rect(center=(x, y))
        else:
            text_rect = text_surf.get_rect(topleft=(x, y))
        self.display_surface.blit(text_surf, text_rect)

    def show_error_window(self):
        pygame.draw.rect(self.display_surface, 'black', (680, 450, 335, 200))

        font = pygame.font.Font(UI_FONT, 18)
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

        font = pygame.font.Font(UI_FONT, 18)
        for i, row in enumerate(message):
            text_surf = font.render(row, True, color)
            text_width, text_text_height = text_surf.get_size()
            self.display_surface.blit(text_surf, (720, 490 + i * text_text_height))
