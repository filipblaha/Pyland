from globalvariables import *


class OverworldSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, name):
        super().__init__(group)
        self.name = name

        if self.name == 'wizard':
            self.animation = []
            for i in range(2):
                filename = f"wizard{i}.png"
                image = pygame.image.load(os.path.join('..', 'graphics', 'characters', "wizard", filename))
                image = pygame.Surface.convert_alpha(image)
                self.animation.append(image)

            self.counter = 0
            self.animation_speed = 0
            self.index = 0
            self.image = self.animation[0]
        else:
            self.image = surf

        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

    def wiz_animation(self, dt):
        if self.name == 'wizard':
            self.animation_speed = 1900 * dt
            self.counter += 1

            if self.counter >= self.animation_speed:
                self.counter = 0
                self.index += 1
                if self.index >= 2:
                    self.index = 0

                self.image = self.animation[self.index]

    def update(self, dt):
        self.wiz_animation(dt)


