from globalvariables import *
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        self.image = pygame.image.load(join('..', 'graphics', 'characters', 'char1.png'))

        #rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        # movement
        self.direction = vector()
        self.speed = 200

        # collisions
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        # # Reacting to pressing/holding keys and setting direction of player
        input_vector = vector(0, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            input_vector.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            input_vector.y = 1
        else:
            input_vector.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            input_vector.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x = -1
        else:
            input_vector.x = 0

        if input_vector.magnitude() != 0:
            self.direction = input_vector.normalize()

        # movement
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right

                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                elif axis == 'vertical':
                    # top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # bottom

                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
