import pygame.sprite
from text import *
from IDEsprites import *
from hud import *
from dialogwindow import *


class IDE:
    def __init__(self, data):

        self.display_surface = pygame.display.get_surface()
        self.sprite_group = pygame.sprite.Group()
        self.sprites = IDESprites(self.display_surface, self.sprite_group)
        self.text = Text()
        self.data = data

        self.current_time = pygame.time.get_ticks()
        self.minigame_type = 1
        self.minigame_num = 0
        self.cutscene_frame = 0
        self.log = False
        self.error_message = []
        self.correct_answer = False
        self.you_win = False
        self.skip_cutscene = False
        self.cutscene_on = False
        self.hint_request = False

        pygame.mouse.set_visible(True)
        self.insert_preset_text()

        self.wizard_health = 10
        self.banned_words = ''
        self.ordered_words = ''

        # mouse
        pygame.mouse.set_visible(False)
        self.mouse = pygame.Surface((10, 10))
        self.mouse.fill((0, 0, 0))
        self.mouse_mask = pygame.mask.from_surface(self.mouse)

        self.dialog_window = DialogWindow('', 50, (1300, 120), 800, 200)
        self.dialog_window.change_text('')

    def logic(self, dt):
        # mystery man
        if self.minigame_type == 0:
            # self.visible_sprites.update_mystery_man()

            if self.cutscene_frame >= 4:
                self.cutscene_on = False

        # wizard
        if self.minigame_type == 1:
            if self.you_win:
                self.sprites.set_wizard_winning_scene()
            else:
                self.sprites.set_wizard()

            # round 1
            if self.minigame_num == 0:
                self.dialog_window.active = True

            # round 2
            elif self.minigame_num == 1:
                pass

            # round 3
            elif self.minigame_num == 2:
                pass

            # winning scene
            elif self.minigame_num == 3:
                pass

        if self.current_time % 1000 < 500:
            self.text.blink_cursor()
        self.current_time = pygame.time.get_ticks()

        # displaying error window
        # self.ui.show_error_window()
        if self.log:
            # self.ui.show_error(self.error_message)
            pass
        if self.correct_answer:
            self.minigame_num += 1
            self.hint_request = False
            if self.minigame_num == 3:
                self.you_win = True
                self.correct_answer = False
            else:
                self.correct_answer = False
                self.insert_preset_text()

    def render(self):
        self.sprite_group.draw(self.display_surface)
        self.dialog_window.display()

        # self.ui.show_hint()
        self.text.render_preset_text()
        self.text.render_user_text()

    def goal(self):
        pass
        # if self.minigame_type == 0:
        #     if self.minigame_num == 0:
        #         return ['name', "name = 'filip'"]
        #
        # if self.minigame_type == 1:
        #     if self.minigame_num == 0:
        #         return ['wizard_health', 'wizard_health = 0']
        #     if self.minigame_num == 1:
        #         self.ordered_words = 'for'
        #         return ['wizard_health', 'wizard_health = 0']
        #     if self.minigame_num == 2:
        #         self.banned_words = 'for'
        #         self.ordered_words = 'while'
        #         return ['wizard_health', 'wizard_health = 0']
        #     if self.minigame_num == 3:
        #         self.banned_words = 'for'
        #         self.ordered_words = 'while'
        #         return ['Thank you for playing the demo', 'wizard_health = 0']

    def insert_preset_text(self):
        pass
        # if self.minigame_type == 0:
        #     if self.minigame_num == 0:
        #         if self.hint_request:
        #             self.text.preset_text = ['# name = your_name']
        #         else:
        #             self.text.preset_text = []
        #
        # if self.minigame_type == 1:
        #     if self.minigame_num == 0:
        #         if self.hint_request:
        #             self.text.preset_text = ['# will he die with no health?', '', 'wizard_health = 10']
        #         else:
        #             self.text.preset_text = ['wizard_health = 10']
        #     if self.minigame_num == 1:
        #         if self.hint_request:
        #             self.text.preset_text = ['# for i in range(n):e', '', 'wizard_health = 10', 'my_damage = 1']
        #         else:
        #             self.text.preset_text = ['wizard_health = 10', 'my_damage = 1']
        #     if self.minigame_num == 2:
        #         if self.hint_request:
        #             self.text.preset_text = ['# while statement_a > statement_b:', 'wizard_health = 10', 'my_damage = 1']
        #         else:
        #             self.text.preset_text = ['wizard_health = 10', 'my_damage = 1']
        #     if self.minigame_num == 3:
        #         self.text.preset_text = ['DEMO = False', 'GitHub = github.com/filipblaha', '', '',
        #                                  'Thank you for playing']
