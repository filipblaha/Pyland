import pygame.sprite

from tile import *


class Sprites(pygame.sprite.Group):
    def __init__(self):
        # camera setup
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # making floor
    def draw_over_world(self, player):

        # getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # conditions for camera movement
        if self.offset.x < 0:
            self.offset.x = 0
        if self.offset.x > 64:
            self.offset.x = 64

        if self.offset.y < 0:
            self.offset.y = 0
        if self.offset.y > 94:
            self.offset.y = 94

        # drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite.rect == (1472, 608, 128, 64):
                offset_pos = sprite.rect.topleft - self.offset
                if player.can_interact:
                    self.display_surface.blit(sprite.image, offset_pos, (64, 0, 128, 64))
                else:
                    self.display_surface.blit(sprite.image, offset_pos, (0, 0, 64, 64))
            else:
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    @staticmethod
    def render_layers(tmx_data, sprite_group):
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x*16, y*16)
                    Tile(pos=pos, surf=surf, groups=sprite_group)

    @staticmethod
    def render_objects(tmx_data, sprite_group):
        for obj in tmx_data.objects:
            pos = obj.x, obj.y
            if obj.type in ('Tree', 'Rock', 'Bush', 'Log', 'Building'):
                Tile(pos=pos, surf=obj.image, groups=sprite_group)
            else:
                pass    # Shapes