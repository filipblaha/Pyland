import pygame

import test_code


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
    def __init__(self, screen, text, ui):

        self.text = text
        self.ui = ui
        self.screen = screen

        self.display_surface = pygame.display.get_surface()
        self.display_surface = self.display_surface.convert_alpha()  # added to support alpha channel
        self.visible_sprites = MinigameSprites()

        self.current_time = pygame.time.get_ticks()
        self.minigame_num = 3
        self.log = False
        self.error_message = []
        self.correct_answer = False
        self.you_win = True

        pygame.mouse.set_visible(True)
        self.insert_preset_text()

        self.wizard_health = 10
        self.banned_words = ''
        self.ordered_words = ''

    def run(self):
        self.current_time = pygame.time.get_ticks()
        if self.you_win:
            self.visible_sprites.update_winning_scene()
        else:
            self.visible_sprites.update()

        if self.current_time % 1000 < 500:
            self.text.blink_cursor()

        self.text.render_preset_text()
        self.text.render_user_text()

        # round 1
        if self.minigame_num == 0:
            self.ui.show_dialog_window('Kill the wizard!', 950, 150, 500, 200, 40)

        # round 2
        if self.minigame_num == 1:
            self.ui.show_dialog_window('', 950, 150, 500, 200, 40)
            self.ui.show_dialog_text('Now try it while using', 800, 100, 30, 'topleft')
            self.ui.show_dialog_text('the ', 850, 160, 30, 'topleft')
            self.ui.show_dialog_text('for cycle', 915, 157, 32, 'topleft', 'green')
            self.ui.show_dialog_text('.', 1060, 160, 30, 'topleft')

        # round 3
        if self.minigame_num == 2:
            self.ui.show_dialog_window('', 950, 150, 500, 200, 40)
            self.ui.show_dialog_text('The', 735, 100, 30, 'topleft')
            self.ui.show_dialog_text('for cycle', 800, 100, 32, 'topleft', 'red')
            self.ui.show_dialog_text('does not work!', 960, 100, 30, 'topleft')
            self.ui.show_dialog_text('Try the', 805, 160, 30, 'topleft')
            self.ui.show_dialog_text('while cycle', 920, 157, 32, 'topleft', 'green')
            self.ui.show_dialog_text('.', 1105, 160, 30, 'topleft')

        # winning scene
        if self.minigame_num == 3:
            self.ui.show_dialog_window('You win!', 950, 150, 500, 200, 40)

        # displaying error window
        self.ui.show_error_window()
        if self.log:
            self.ui.show_error(self.error_message)
        if self.correct_answer:
            self.minigame_num += 1
            if self.minigame_num == 2:
                self.you_win = True
            else:
                self.correct_answer = False
                self.insert_preset_text()

    def goal(self):
        if self.minigame_num == 0:
            return ['wizard_health', 'wizard_health = 0']
        if self.minigame_num == 1:
            self.ordered_words = 'for'
            return ['wizard_health', 'wizard_health = 0']
        if self.minigame_num == 2:
            self.banned_words = 'for'
            self.ordered_words = 'while'
            return ['wizard_health', 'wizard_health = 0']
        if self.minigame_num == 3:
            self.banned_words = 'for'
            self.ordered_words = 'while'
            return ['Thank you for playing the demo', 'wizard_health = 0']

    def insert_preset_text(self):
        if self.minigame_num == 0:
            self.text.preset_text = ['wizard_health = 10']
        if self.minigame_num == 1:
            self.text.preset_text = ['wizard_health = 10', 'my_damage = 1']
        if self.minigame_num == 2:
            self.text.preset_text = ['wizard_health = 10', 'my_damage = 1']
        if self.minigame_num == 3:
            self.text.preset_text = ['DEMO = False', 'GitHub = github.com/filipblaha', '', '', 'Thank you for playing']

class MinigameSprites(pygame.sprite.Group):
    def __init__(self):
        # camera setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # making sprites
        self.forest_surf = pygame.image.load('graphic/minigame/forest.png')
        self.enemy_surf = pygame.image.load('graphic/minigame/wizard_closeup.png')
        self.code_paper_surf = pygame.image.load('graphic/minigame/code_paper.png')
        self.check_button_surf = pygame.image.load('graphic/minigame/check_button.png')
        self.enemy_dead_surf = pygame.image.load('graphic/minigame/hat.png')

        self.forest_rect = self.forest_surf.get_rect(topleft=(0, 0))
        self.enemy_rect = self.enemy_surf.get_rect(topleft=(1080, 200))
        self.code_paper_rect = self.code_paper_surf.get_rect(topleft=(0, 0))
        self.check_button_rect = self.check_button_surf.get_rect(center=(850, 750))
        self.enemy_dead_rect = self.enemy_dead_surf.get_rect(center=(1280, 620))

    def update_winning_scene(self):
        self.display_surface.blit(self.forest_surf, self.forest_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)
        self.display_surface.blit(self.enemy_dead_surf, self.enemy_dead_rect.topleft)

    def update(self):
        self.display_surface.blit(self.forest_surf, self.forest_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)
        self.display_surface.blit(self.enemy_surf, self.enemy_rect.topleft)

    def blink_button(self):
        enlarged_image_surf = pygame.transform.scale(self.check_button_surf, (450, 180))
        self.display_surface.blit(enlarged_image_surf, (625, 660))
        pygame.display.flip()
        pygame.time.delay(200)  # waiting 200 ms
