import sys

import pytmx.pytmx

from sprites import Sprite
from player import *
from dialogwindow import *
from CameraGroup import *
from pytmx.pytmx import TileFlags



class OverWorld:
    def __init__(self, screen, tmx_map):

        # get the display surface
        self.display_surface = screen

        # sprite setup
        self.camera_group = CameraGroup()
        self.player = None
        self.barrier = None
        self.setup(tmx_map)
        # self.camera_group = CameraGroup()

        ####smazat
        pygame.mouse.set_visible(False)
        self.mouse = pygame.Surface((10, 10))
        self.mouse.fill((0, 0, 0))
        self.mouse_mask = pygame.mask.from_surface(self.mouse)

    def setup(self, tmx_map):
        for layer in ['Floor', 'Pavement', 'Vegetation', 'Cliffs3', 'Cliffs2', 'Cliffs1', 'FloorDarkShadow',
                      'FloorBrightShadow']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.camera_group, 'Tile')

        for obj in tmx_map.get_layer_by_name('Objects'):
            pos = obj.x, obj.y
            if obj.name == 'Player':
                self.player = Player(pos, self.camera_group, tmx_map, 'Player')
            else:
                sprite_image = obj.image
                if pytmx.pytmx.TileFlags(False, True, False):
                    sprite_image = pygame.transform.flip(sprite_image, True, False)
                Sprite(pos, sprite_image, self.camera_group, obj.name)

    def logic(self, dt):
        # update
        self.camera_group.update(dt)

    def render(self, dt):
        # draw
        self.camera_group.custom_draw(self.player)

        self.display_surface.blit(self.mouse, pygame.mouse.get_pos())

