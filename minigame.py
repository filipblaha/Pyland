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
    def __init__(self, screen, text,ui):

        self.text = text
        self.ui = ui
        self.screen = screen

        self.display_surface = pygame.display.get_surface()
        self.display_surface = self.display_surface.convert_alpha()  # added to support alpha channel
        self.visible_sprites = MinigameSprites()

        self.current_time = pygame.time.get_ticks()
        self.minigame_num = 0
        self.log = False
        self.error_message = ['']

        pygame.mouse.set_visible(True)

        self.wizard_health = 10

    def run(self):
        self.current_time = pygame.time.get_ticks()
        self.visible_sprites.draw_floor()
        self.visible_sprites.update()

        if self.current_time % 1000 < 500:
            self.text.blink_cursor()
        self.text.render_user_text()

        if self.minigame_num == 0:
            self.ui.show_error_window()
            if self.log:
                self.ui.show_error(self.error_message)

    def goal(self):
        if self.minigame_num == 0:
            return ['wizard_health', 'wizard_health = 1']


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
        self.enemy_rect = self.enemy_surf.get_rect(topleft=(1080, 200))
        self.code_paper_rect = self.code_paper_surf.get_rect(topleft=(0, 0))
        self.check_button_rect = self.check_button_surf.get_rect(center=(850, 750))

    def draw_floor(self):

        self.display_surface.blit(self.forest_surf, self.forest_rect.topleft)
        self.display_surface.blit(self.enemy_surf, self.enemy_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)

    def blink_button(self):
        enlarged_image_surf = pygame.transform.scale(self.check_button_surf, (450, 180))
        self.display_surface.blit(enlarged_image_surf, (625, 660))
        pygame.display.flip()
        pygame.time.delay(200)  # Počkejme 400 milisekund
