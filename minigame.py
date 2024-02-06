import pygame


class Minigame:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.display_surface = self.display_surface.convert_alpha()  # added to support alpha channel

        self.animation_frames_up = [
            pygame.image.load('graphic/minigame/blank_window.png').convert_alpha(),
            pygame.image.load('graphic/minigame/check_button.png').convert_alpha(),
            pygame.image.load('graphic/minigame/code.png').convert_alpha(),
            pygame.image.load('graphic/minigame/forest.png').convert_alpha(),
            pygame.image.load('graphic/minigame/goblin.png').convert_alpha(),
            pygame.image.load('graphic/minigame/hearth.png').convert_alpha(),
        ]
