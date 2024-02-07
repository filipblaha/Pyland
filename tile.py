import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE)), name=0):

        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.zone = pygame.Rect(0, 0, 0, 0)

        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
            self.hitbox = self.rect.inflate(0, -3)
            if not name == 0:
                self.zone = self.rect.inflate(150, 150)
        else:
            self.rect = self.image.get_rect(topleft=pos)
        # changing the size of tiles
            self.hitbox = self.rect.inflate(0, -3)
