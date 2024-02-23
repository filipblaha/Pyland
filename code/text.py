import pygame
class Text(pygame.sprite.Sprite):
    def __init__(self, font_name, size, screen, *groups):
        super().__init__(*groups)