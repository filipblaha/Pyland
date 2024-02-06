import pygame
import os
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from ui import UI
from menu import Menu

import pygame

# Nastavení rozlišení hry
NEW_WIDTH = WIDTH
NEW_HEIGHT = HEIGHT

# Inicializace Pygame
pygame.init()

# Nastavení velikosti obrazovky
screen = pygame.display.set_mode((NEW_WIDTH, NEW_HEIGHT))
pygame.display.set_caption("Your Game Title")

class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprite = pygame.sprite.Group()

        #sprite setup
        self.creat_map()

    #   user interface
        self.ui = UI()
        self.menu = Menu(self.player)

        self.zoom_level = 1.0  # Úroveň přiblížení


    def creat_map(self):
        layout = {
                'boundary': import_csv_layout('map/zelda_FloorBlocks.csv'),
                'grass': import_csv_layout('map/zelda_Grass.csv'),
                'object': import_csv_layout('map/zelda_Objects.csv'),
        }
        graphics = {
                'grass': import_folder('map/Grass'),
                'object': import_folder('map/Object')
        }

        for style,layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y),[self.obstacle_sprite],'invinsible')

                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y),[self.visible_sprites,self.obstacle_sprite],'grass',random_grass_image)

                        if style == 'object':
                            if int(col) == 222:
                                image_name = 'ListStrom.png'
                                image_path = os.path.join('map', 'Object', image_name)
                                surf = pygame.image.load(image_path).convert_alpha()
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'object', surf)

                            if int(col) == 26:
                                    image_name = 'JehlStrom.png'
                                    image_path = os.path.join('map', 'Object', image_name)
                                    surf = pygame.image.load(image_path).convert_alpha()
                                    Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'object', surf)

                            if int(col) == -2147482840:
                                    image_name = 'Ztrazce_cely.png'
                                    image_path = os.path.join('map', 'Object', image_name)
                                    surf = pygame.image.load(image_path).convert_alpha()
                                    Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'object', surf)


        self.player = Player((195, 170), [self.visible_sprites], self.obstacle_sprite)

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custum_draw(self.player)
        # update and draw the game
        # pause
        if self.game_paused:
            self.menu.display()
        else:
            self.visible_sprites.update()
            self.ui.display(self.player)
class YSortCameraGroup (pygame.sprite.Group):
    def __init__(self):

        # zakladni nastaveni - NASTAVENI KAMERY
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    #     vytvareni podlahy
        self.floor_surf = pygame.image.load('graphic/background.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    def custum_draw(self,player):

        # ziskani offsetu
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height


        # vykreslovani podlahy
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)