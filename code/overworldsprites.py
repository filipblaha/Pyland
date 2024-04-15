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
        elif self.name == 'knight':
            self.animation = []
            for i in range(2):
                filename = f"knight{i}.png"
                image = pygame.image.load(os.path.join('..', 'graphics', 'characters', "knight", filename))
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

    def animate(self, dt, name, speed):
        if self.name == name:
            self.animation_speed = speed * dt
            self.counter += 1

            if self.counter >= self.animation_speed:
                self.counter = 0
                self.index += 1
                if self.index >= 2:
                    self.index = 0

                self.image = self.animation[self.index]

    def update(self, dt):
        self.animate(dt, 'wizard', 1900)
        self.animate(dt, 'knight', 1600)


