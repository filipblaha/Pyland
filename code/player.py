import pygame

from globalvariables import *
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, tmx_map, name):
        super().__init__(group)
        self.name = name

        self.run_animation = []
        self.stand_animation = []
        self.frame_size = 32
        for i in range(8):
            filename = f"run{i}.png"
            image = pygame.image.load(os.path.join('..', 'graphics', 'characters', "player", filename))
            image = pygame.Surface.convert_alpha(image)
            dir_animation = []
            for j in range(6):
                frame = image.subsurface((j * self.frame_size, 0, self.frame_size, image.get_height()))
                dir_animation.append(frame)
            self.run_animation.append(dir_animation)

        for i in range(8):
            filename = f"stand{i}.png"
            image = pygame.image.load(os.path.join('..', 'graphics', 'characters', "player", filename))
            image = pygame.Surface.convert_alpha(image)
            dir_animation = []
            for j in range(2):
                frame = image.subsurface((j * self.frame_size, 0, self.frame_size, image.get_height()))
                dir_animation.append(frame)
            self.stand_animation.append(dir_animation)

        self.index = 0
        self.counter = 0
        self.animation_speed = 0
        # self.image = self.run_animation[self.index][1]
        self.image = self.stand_animation[self.index][0]

        # rects
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect
        self.old_rect = self.hitbox_rect.copy()

        # movement
        self.direction = vector()
        self.last_direction = vector(0, 1)
        self.speed = 100

        for obj in tmx_map.get_layer_by_name('Zones'):
            pos = obj.x, obj.y
            if obj.name == 'barrier':
                self.barrier = obj.points
            # if obj.name == 'wizard_zone'
            #     self.

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
        else:
            self.direction = input_vector
        if not self.direction == vector(0, 0):
            self.last_direction = self.direction

        # movement
    def move(self, dt):

        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.hitbox_rect.y += self.direction.y * self.speed * dt

        if self.polygon_collision_check(self.barrier):
            self.hitbox_rect.center = self.old_rect.center

    def polygon_collision_check(self, polygon_vertices):
        num_intersections = 0
        player_x = self.hitbox_rect.midbottom[0]
        player_y = self.hitbox_rect.midbottom[1]-10
        for i in range(len(polygon_vertices)):
            p1 = polygon_vertices[i]
            p2 = polygon_vertices[(i + 1) % len(polygon_vertices)]

            if (p1[1] > player_y) != (p2[1] > player_y) and \
                    player_x < (p2[0] - p1[0]) * (player_y - p1[1]) / (p2[1] - p1[1]) + p1[0]:
                num_intersections += 1

        if num_intersections % 2 == 1:
            return False
        else:
            return True

    def zone_collision_check(self, zone):
        player_x = self.hitbox_rect.centerx
        player_y = self.hitbox_rect.centery

        if zone.collidepoint((player_x, player_y)):
            return True
        else:
            return False

    def animation(self, dt):
        self.counter += 1
        if self.direction == vector(0, 0):
            if self.counter >= self.animation_speed:
                self.animation_speed = 900 * dt
                self.counter = 0
                self.index += 1
                if self.index >= 2:
                    self.index = 0

                if self.last_direction == vector(0, 1):
                    self.image = self.stand_animation[0][self.index]
                elif self.last_direction == vector(-1, 1).normalize():
                    self.image = self.stand_animation[1][self.index]
                elif self.last_direction == vector(-1, 0):
                    self.image = self.stand_animation[2][self.index]
                elif self.last_direction == vector(-1, -1).normalize():
                    self.image = self.stand_animation[3][self.index]
                elif self.last_direction == vector(0, -1):
                    self.image = self.stand_animation[4][self.index]
                elif self.last_direction == vector(1, -1).normalize():
                    self.image = self.stand_animation[5][self.index]
                elif self.last_direction == vector(1, 0):
                    self.image = self.stand_animation[6][self.index]
                elif self.last_direction == vector(1, 1).normalize():
                    self.image = self.stand_animation[7][self.index]

        else:
            self.animation_speed = 150 * dt
            if self.counter >= self.animation_speed:
                self.counter = 0
                self.index += 1
                if self.index >= 5:
                    self.index = 0

                if self.direction == vector(0, 1):
                    self.image = self.run_animation[0][self.index]
                elif self.direction == vector(-1, 1).normalize():
                    self.image = self.run_animation[1][self.index]
                elif self.direction == vector(-1, 0):
                    self.image = self.run_animation[2][self.index]
                elif self.direction == vector(-1, -1).normalize():
                    self.image = self.run_animation[3][self.index]
                elif self.direction == vector(0, -1):
                    self.image = self.run_animation[4][self.index]
                elif self.direction == vector(1, -1).normalize():
                    self.image = self.run_animation[5][self.index]
                elif self.direction == vector(1, 0):
                    self.image = self.run_animation[6][self.index]
                elif self.direction == vector(1, 1).normalize():
                    self.image = self.run_animation[7][self.index]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animation(dt)
        self.old_rect = self.hitbox_rect.copy()

