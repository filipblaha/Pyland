import pygame

from globalvariables import *
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, tmx_map, name):
        super().__init__(group)

        self.image = pygame.image.load(join('..', 'graphics', 'characters', 'char1.png'))
        self.name = name

        # rects
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect
        self.old_rect = self.hitbox_rect.copy()

        # movement
        self.direction = vector()
        self.speed = 150

        for obj in tmx_map.get_layer_by_name('Objects'):
            pos = obj.x, obj.y
            if obj.name == 'barrier':
                self.barrier = obj.points

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

        # movement
    def move(self, dt):

        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.hitbox_rect.y += self.direction.y * self.speed * dt

        if self.collision_check(self.barrier):
            self.hitbox_rect.center = self.old_rect.center

    def collision_check(self, polygon_vertices):
        num_intersections = 0
        player_x = self.hitbox_rect.midbottom[0]
        player_y = self.hitbox_rect.midbottom[1]-5
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

    def update(self, dt):
        self.input()
        self.move(dt)
        self.old_rect = self.hitbox_rect.copy()
