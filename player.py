import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprite, can_interact):
        super().__init__(groups)
        self.image = pygame.image.load('char/Spirit/Look_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        # changing size of hitbox
        self.hitbox = self.rect.inflate(0, -11)

        self.direction = pygame.math.Vector2()
        self.speed = 4

        self.obstacle_sprite = obstacle_sprite

        # animations
        self.animation_speed = 0.08
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
        self.can_interact = can_interact

    # movement
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()     # changing velocity to normal in every direction

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
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
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        # checking vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

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

        # stats ##################ZMEN NA UKOL
        self.stats = {'health': 100}
        self.health = self.stats['health'] * 0.5
        self.exp = 1

    def update(self):
        self.input()
        self.move(self.speed)
        self.animate()
