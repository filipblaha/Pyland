import sys

from sprites import Sprite
from player import *
from dialogwindow import *
from CameraGroup import *


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
            elif obj.name == 'barrier':
                self.barrier = obj.points
            else:
                Sprite(pos, obj.image, self.camera_group, obj.name)

    def render_objects(self, tmx_map):
        pass    # Shapes

    def logic(self):
        pass

    def render(self, dt):
        # update and draw the game
        self.camera_group.custom_draw(self.player)
        self.camera_group.update(dt)

        pos = pygame.mouse.get_pos()
        self.display_surface.blit(self.mouse, pos)
        # pygame.draw.polygon(self.display_surface, (0,0,0), self.barrier)

