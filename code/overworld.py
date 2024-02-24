import sys

from sprites import Sprite
from player import *
from dialogwindow import *


class OverWorld:
    def __init__(self, screen, tmx_map):

        # get the display surface
        self.display_surface = screen

        # sprite setup
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.setup(tmx_map)

    def setup(self, tmx_map):
        for layer in ['Floor', 'Pavement', 'Vegetation', 'Cliffs3', 'Cliffs2', 'Cliffs1', 'FloorDarkShadow',
                      'FloorBrightShadow']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Objects'):
            pos = obj.x, obj.y
            if obj.name == 'Player':
                Player(pos, self.all_sprites, self.collision_sprites)
            else:
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

    def render_objects(self, tmx_map):
        pass    # Shapes

    def logic(self):
        pass

    def render(self, dt):
        # update and draw the game
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)



