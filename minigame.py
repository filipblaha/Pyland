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
        self.visible_sprites = MinigameSprites()

        pygame.mouse.set_visible(True)

    def run(self):
        self.visible_sprites.draw_floor()
        self.visible_sprites.update()

        self.typing.render_user_text(self.screen, 140, 110)


class MinigameSprites (pygame.sprite.Group):
    def __init__(self):

        # camera setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # making sprites
        self.forest_surf = pygame.image.load('graphic/minigame/forest.png')
        self.enemy_surf = pygame.image.load('graphic/minigame/wizard_closeup.png')
        self.code_paper_surf = pygame.image.load('graphic/minigame/code_paper.png')
        self.check_button_surf = pygame.image.load('graphic/minigame/check_button.png')

        self.forest_rect = self.forest_surf.get_rect(topleft=(0, 0))
        self.enemy_rect = self.forest_surf.get_rect(topleft=(850, 200))
        self.code_paper_rect = self.forest_surf.get_rect(topleft=(0, 0))
        self.check_button_rect = self.forest_surf.get_rect(topleft=(650, 700))

    def draw_floor(self):

        self.display_surface.blit(self.forest_surf, self.forest_rect.topleft)
        self.display_surface.blit(self.enemy_surf, self.enemy_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)

