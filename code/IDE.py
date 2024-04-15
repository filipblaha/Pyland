import pygame.sprite
from text import *
from IDEsprites import *
from hud import *
from test_code import *
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
        self.dialog_window.active = True

        self.data_assignment = None
        self.data_preset_words = None
        self.setup()

    def setup(self):
        for item in self.data.data:
            if item['Type'] == 'Goal':
                self.data_assignment = item['Data']
            if item['Type'] == 'Preset words':
                self.data_preset_words = item['Data']

    def logic(self, dt):

        self.text.preset_text = self.data_preset_words[self.minigame_type]

        # error = check_code(code, goal)
        #
        # self.minigame.error_message = test_code.log_errors(code, error)
        # if not test_code.ordered_word(self.text.user_text, self.minigame.ordered_words):
        #     self.minigame.error_message = ['You are not using ordered words:', self.minigame.ordered_words]
        # if test_code.banned_words(self.text.user_text,
        #                           self.minigame.banned_words) and not self.minigame.banned_words == '':
        #     self.minigame.error_message = ['You are using banned words:', self.minigame.banned_words]

        if self.correct_answer:
            self.minigame_num += 1
            self.hint_request = False
            if self.minigame_num == 3:
                self.you_win = True
                self.correct_answer = False
            else:
                self.correct_answer = False

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

        if self.current_time % 1000 < 500:
            self.text.blink_cursor()
        self.current_time = pygame.time.get_ticks()

        # displaying error window
        # self.ui.show_error_window()
        if self.log:
            # self.ui.show_error(self.error_message)
            pass

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
