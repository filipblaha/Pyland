import pygame
from screen import Screen
from settings import *

# class Object:
#     def __init__(self, png, width, height, x, y, speed):
#         self.sprite = pygame.image.load(png)
#         self.sprite = pygame.transform.scale(self.sprite, (width, height))
#         self.x = x
#         self.y = y
#         self.speed = speed
#
#     def movement(self, keys):
#         if keys[pygame.K_a]:
#             self.x -= self.speed
#         if keys[pygame.K_d]:
#             self.x += self.speed
#         if keys[pygame.K_w]:
#             self.y -= self.speed
#         if keys[pygame.K_s]:
#             self.y += self.speed



class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprite):
        super().__init__(groups)
        self.image = pygame.image.load('graphic/player.png').convert_alpha()
        self.hitbox = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprite = obstacle_sprite

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()     # NASTAVENÍ STEJNÉ RYCHLOSTI DO VŠECH SMĚRŮ

        self.hitbox.x += self.direction.x * speed
        self.hitbox.y += self.direction.y * speed
        #self.rect.center += self.direction * speed

    def collision (self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #pohyb vpravo
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # pohyb vlevo
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # pohyb dolu
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # pohyb nahoru
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)

