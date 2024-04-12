from globalvariables import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, name):
        super().__init__(group)

        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.name = name


