import pygame
from settings import *

class Menu:
    def __init__(self, player):

        # General setup
        self.display_surface = pygame.display.get_surface()
        self.display_surface = self.display_surface.convert_alpha()  # Přidáno pro podporu alfa kanálu
        self.player = player

    def display(self):
        self.display_surface.fill((128, 128, 128, 200))

