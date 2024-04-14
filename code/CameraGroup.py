import pygame

from globalvariables import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2

        # zoom
        self.zoom_scale = 3
        self.internal_surf_size = (640, 360)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

        # box setup
        self.camera_borders = {'left': 800, 'right': 800, 'top': 480, 'bottom': 480}
        lft = self.camera_borders['left']
        tp = self.camera_borders['top']
        rgt = self.display_surface.get_size()[0] - self.camera_borders['left'] - self.camera_borders['right']
        btm = self.display_surface.get_size()[1] - self.camera_borders['top'] - self.camera_borders['bottom']
        self.camera_rect = pygame.Rect(lft, tp, rgt, btm)

        self.camera_rect.center = (600, 600)
        # self.camera_rect.center = (400, 240)

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, player):
        self.box_target_camera(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            if sprite.name == 'Tile' or sprite.name == 'bridge1' or sprite.name == 'bridge2':
                self.internal_surf.blit(sprite.image, offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.midbottom[1]):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            if sprite.name == 'Tile' or sprite.name == 'bridge1' or sprite.name == 'bridge2':
                pass
            else:
                self.internal_surf.blit(sprite.image, offset_pos)
        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)
