from text import *
from idesprites import *


class IDE:
    def __init__(self, display_surface):

        self.display_surface = display_surface

        self.text = Text(display_surface)
        self.visible_sprites = IDESprites(self.display_surface)

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

    def logic(self):

        # mystery man
        if self.minigame_type == 0:
            # self.visible_sprites.update_mystery_man()

            if self.cutscene_frame >= 4:
                self.cutscene_on = False
            self.animate_cutscene()

        # wizard
        if self.minigame_type == 1:
            if self.you_win:
                self.visible_sprites.update_wizard_winning_scene()
            else:
                self.visible_sprites.update_wizard()

            # round 1
            if self.minigame_num == 0:
                pass
                # self.ui.show_dialog_window('Kill the wizard!', 950, 150, 500, 200, 40)

            # round 2
            elif self.minigame_num == 1:
                pass
                # self.ui.show_dialog_window('', 950, 150, 500, 200, 40)
                # self.ui.show_dialog_text('It has done nothing!?', 800, 100, 30, 'topleft')
                # self.ui.show_dialog_text('Try the ', 820, 160, 30, 'topleft')
                # self.ui.show_dialog_text('for cycle', 935, 157, 32, 'topleft', 'green')
                # self.ui.show_dialog_text('.', 1085, 160, 30, 'topleft')

            # round 3
            elif self.minigame_num == 2:
                pass
                # self.ui.show_dialog_window('', 950, 150, 500, 200, 40)
                # self.ui.show_dialog_text('The', 735, 100, 30, 'topleft')
                # self.ui.show_dialog_text('for cycle', 800, 100, 32, 'topleft', 'red')
                # self.ui.show_dialog_text('does not work!', 960, 100, 30, 'topleft')
                # self.ui.show_dialog_text('Try the', 805, 160, 30, 'topleft')
                # self.ui.show_dialog_text('while cycle', 920, 157, 32, 'topleft', 'green')
                # self.ui.show_dialog_text('.', 1105, 160, 30, 'topleft')

            # winning scene
            elif self.minigame_num == 3:
                pass
                # self.ui.show_dialog_window('You win!', 950, 150, 500, 200, 40)

        if self.current_time % 1000 < 500:
            self.text.blink_cursor()

        # self.ui.show_hint()
        self.text.render_preset_text()
        self.text.render_user_text()
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

    def animate_cutscene(self):
        pass
        # if self.cutscene_frame == 0:
        #     self.ui.show_dialog_window('Hey you!', 950, 150, 500, 200, 30)
        # elif self.cutscene_frame == 1:
        #     self.ui.show_dialog_window("There's no time to waste!", 950, 150, 500, 200, 30)
        # elif self.cutscene_frame == 2:
        #     self.ui.show_dialog_window('', 950, 150, 500, 200, 30)
        #     self.ui.show_dialog_text('You have to', 805, 110, 30, 'topleft')
        #     self.ui.show_dialog_text('STOP HIM', 985, 110, 30, 'topleft', 'red')
        #     self.ui.show_dialog_text("before it's too late!", 830, 150, 30, 'topleft')
        # elif self.cutscene_frame == 3:
        #     self.ui.show_dialog_window('Quickly!', 950, 150, 500, 200, 30)
        # elif self.cutscene_frame >= 4:
        #     self.ui.show_dialog_window('', 950, 150, 500, 200, 30)
        #     self.ui.show_dialog_text('Tell me your name and', 780, 90, 30, 'topleft')
        #     self.ui.show_dialog_text('GO!!!', 880, 130, 70, 'topleft', 'red')
        # else:
        #     return
        # self.skip_cutscene = False

    def goal(self):
        if self.minigame_type == 0:
            if self.minigame_num == 0:
                return ['name', "name = 'filip'"]

        if self.minigame_type == 1:
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
        if self.minigame_type == 0:
            if self.minigame_num == 0:
                if self.hint_request:
                    self.text.preset_text = ['# name = your_name']
                else:
                    self.text.preset_text = []

        if self.minigame_type == 1:
            if self.minigame_num == 0:
                if self.hint_request:
                    self.text.preset_text = ['# will he die with no health?', '', 'wizard_health = 10']
                else:
                    self.text.preset_text = ['wizard_health = 10']
            if self.minigame_num == 1:
                if self.hint_request:
                    self.text.preset_text = ['# for i in range(n):e', '', 'wizard_health = 10', 'my_damage = 1']
                else:
                    self.text.preset_text = ['wizard_health = 10', 'my_damage = 1']
            if self.minigame_num == 2:
                if self.hint_request:
                    self.text.preset_text = ['# while statement_a > statement_b:', 'wizard_health = 10', 'my_damage = 1']
                else:
                    self.text.preset_text = ['wizard_health = 10', 'my_damage = 1']
            if self.minigame_num == 3:
                self.text.preset_text = ['DEMO = False', 'GitHub = github.com/filipblaha', '', '',
                                         'Thank you for playing']
