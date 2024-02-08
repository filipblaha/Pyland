import pygame

class Object:
    def __init__(self, png, width, height, x, y):
        self.sprite = pygame.image.load(png).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height


class Minigame:
    def __init__(self, typing, screen):

        self.typing = typing
        self.screen = screen

        self.display_surface = pygame.display.get_surface()
        self.display_surface = self.display_surface.convert_alpha()  # added to support alpha channel

        self.visible_sprites = YSortCameraGroup()

        self.border_surf = Object('graphic/minigame/forest.png', 1180, 980, 700, 50)
        self.enemy_surf = Object('graphic/minigame/goblin.png', 250, 300, 1200, 600)
        self.code_surf = Object('graphic/minigame/code.png', 600, 750, 50, 50)
        self.button_surf = Object('graphic/minigame/check_button.png', 400, 150, 150, 83)

    def run(self):
        self.visible_sprites.draw_floor()
        self.visible_sprites.update()

        # self.display_surface.fill((100, 100, 100))
        # self.display_surface.blit(self.code_surf.sprite, self.code.rect)
        # self.display_surface.blit(self.border_surf.sprite, self.border.rect)
        # self.display_surface.blit(self.enemy_surf.sprite, self.enemy.rect)
        # self.display_surface.blit(self.button_surf.sprite, self.button.rect)
        self.typing.render_user_text(self.screen, 65, 55)


class YSortCameraGroup (pygame.sprite.Group):
    def __init__(self):

        # camera setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # making floor
        self.floor_surf = pygame.image.load('graphic/background.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def draw_floor(self):
        self.display_surface.blit(self.floor_surf, self.floor_rect.topleft)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
