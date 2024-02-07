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

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(5,5))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(5, 5), 3)

    def display(self, player, displayed):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        self.show_exp(displayed)

    def show_dialog_window(self, message, x, y, width, height):

        # text_surf = self.font.render(str(message), False, 'black')
        # text_rect = text_surf.get_rect(center=(x, y))
        # dialog_window_rect = text_rect.inflate((50, 50))
        #
        # dialog_window_surf = pygame.image.load('graphic/dialog_window.png').convert()
        # dialog_window_surf = pygame.transform.scale(dialog_window_surf, dialog_window_rect.size)
        # dialog_window_surf.set_alpha(200)  # alpha level
        # self.display_surface.blit(dialog_window_surf, text_rect)
        # self.display_surface.blit(text_surf, text_rect)

        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        dialog_window_surf = pygame.image.load('graphic/dialog_window.png').convert()
        dialog_window_surf = pygame.transform.scale(dialog_window_surf, rect.size)
        dialog_window_surf.set_alpha(200)  # alpha level
        self.display_surface.blit(dialog_window_surf, rect)

        text_surf = self.font.render(str(message), False, 'black')
        text_rect = text_surf.get_rect(center=(x, y))
        self.display_surface.blit(text_surf, text_rect)
