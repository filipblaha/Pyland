import pygame


class Screen:
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.name = name
        self.display = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption(self.name)