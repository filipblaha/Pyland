import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprite):
        super().__init__(groups)

        self.image = pygame.image.load('char/Spirit/Look_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.speed = 0.35
        self.obstacle_sprite = obstacle_sprite

        # hitbox interaction
        self.hitbox = self.rect.inflate(0, -11)
        self.can_interact = False

        # animations
        self.animation_speed = 0.008
        self.animation_frames_up = [
            pygame.image.load('char/Spirit/Walk_up_1.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_up_2.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_up_3.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_up_4.png').convert_alpha(),
        ]
        self.animation_frames_down = [
            pygame.image.load('char/Spirit/Walk_down_1.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_down_2.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_down_3.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_down_4.png').convert_alpha(),
        ]
        self.animation_frames_right = [
            pygame.image.load('char/Spirit/Walk_right_1.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_right_2.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_right_3.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_right_4.png').convert_alpha(),
        ]
        self.animation_frames_left = [
            pygame.image.load('char/Spirit/Walk_left_1.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_left_2.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_left_3.png').convert_alpha(),
            pygame.image.load('char/Spirit/Walk_left_4.png').convert_alpha(),
        ]

        self.idle_frames_up = [
            pygame.image.load('char/Spirit/Look_up.png').convert_alpha()
        ]

        self.idle_frames_down = [
            pygame.image.load('char/Spirit/Look_down.png').convert_alpha()
        ]

        self.idle_frames_left = [
            pygame.image.load('char/Spirit/Look_left.png').convert_alpha()
        ]

        self.idle_frames_right = [
            pygame.image.load('char/Spirit/Look_right.png').convert_alpha()
        ]

        self.last_direction = None
        # actual index of a frame
        self.frame_index = 0

    # movement
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()     # changing velocity to normal in every direction

        self.pos.x += self.direction.x * self.speed
        self.pos.y += self.direction.y * self.speed

        self.hitbox.centerx = self.pos.x
        self.hitbox.centery = self.pos.y

        self.collision('vertical')
        self.collision('horizontal')
        self.rect.center = self.hitbox.center

        # animations
        if self.direction.x > 0:
            self.last_direction = 'right'
        elif self.direction.x < 0:
            self.last_direction = 'left'
        elif self.direction.y > 0:
            self.last_direction = 'down'
        elif self.direction.y < 0:
            self.last_direction = 'up'

    def collision(self, direction):
        # checking horizontal collisions
        if direction == 'horizontal':
            for sprite in self.obstacle_sprite:
                if sprite.zone.colliderect(self.hitbox):
                    self.can_interact = True
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.pos.x = self.hitbox.centerx

        # checking vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacle_sprite:
                if sprite.zone.colliderect(self.hitbox):
                    self.can_interact = True
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.pos.y = self.hitbox.centery
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.pos.y = self.hitbox.centery

    def animate(self):
        # conditions of deciding the direction of moving
        if self.direction.y < 0:
            animation = self.animation_frames_up
            self.last_direction = 'up'
        elif self.direction.y > 0:
            animation = self.animation_frames_down
            self.last_direction = 'down'
        elif self.direction.x < 0:
            animation = self.animation_frames_left
            self.last_direction = 'left'
        elif self.direction.x > 0:
            animation = self.animation_frames_right
            self.last_direction = 'right'
        else:
            # animations for standing still
            if self.last_direction == 'left':
                animation = self.idle_frames_left
            elif self.last_direction == 'right':
                animation = self.idle_frames_right
            elif self.last_direction == 'down':
                animation = self.idle_frames_down
            else:
                animation = self.idle_frames_up

        # updating the animation index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # settings of the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()
