import pygame


class Minigame:
    def __init__(self, screen, text, ui):

        self.text = text
        self.ui = ui
        self.screen = screen

        self.display_surface = pygame.display.get_surface()
        self.display_surface = self.display_surface.convert_alpha()  # added to support alpha channel
        self.visible_sprites = MinigameSprites()

        self.current_time = pygame.time.get_ticks()
        self.minigame_type = 0
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

    def run(self):

        # mystery man
        if self.minigame_type == 0:
            self.visible_sprites.update_mystery_man()

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
                self.ui.show_dialog_window('Kill the wizard!', 950, 150, 500, 200, 40)

            # round 2
            if self.minigame_num == 1:
                self.ui.show_dialog_window('', 950, 150, 500, 200, 40)
                self.ui.show_dialog_text('It has done nothing!?', 800, 100, 30, 'topleft')
                self.ui.show_dialog_text('Try the ', 820, 160, 30, 'topleft')
                self.ui.show_dialog_text('for cycle', 935, 157, 32, 'topleft', 'green')
                self.ui.show_dialog_text('.', 1085, 160, 30, 'topleft')

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

        if self.current_time % 1000 < 500:
            self.text.blink_cursor()

        self.ui.show_hint()
        self.text.render_preset_text()
        self.text.render_user_text()
        self.current_time = pygame.time.get_ticks()

        # displaying error window
        self.ui.show_error_window()
        if self.log:
            self.ui.show_error(self.error_message)
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
        if self.cutscene_frame == 0:
            self.ui.show_dialog_window('Hey you!', 950, 150, 500, 200, 30)
        elif self.cutscene_frame == 1:
            self.ui.show_dialog_window("There's no time to waste!", 950, 150, 500, 200, 30)
        elif self.cutscene_frame == 2:
            self.ui.show_dialog_window('', 950, 150, 500, 200, 30)
            self.ui.show_dialog_text('You have to', 805, 110, 30, 'topleft')
            self.ui.show_dialog_text('STOP HIM', 985, 110, 30, 'topleft', 'red')
            self.ui.show_dialog_text("before it's too late!", 830, 150, 30, 'topleft')
        elif self.cutscene_frame == 3:
            self.ui.show_dialog_window('Quickly!', 950, 150, 500, 200, 30)
        elif self.cutscene_frame >= 4:
            self.ui.show_dialog_window('', 950, 150, 500, 200, 30)
            self.ui.show_dialog_text('Tell me your name and', 780, 90, 30, 'topleft')
            self.ui.show_dialog_text('GO!!!', 880, 130, 70, 'topleft', 'red')
        else:
            return
        self.skip_cutscene = False

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


class MinigameSprites(pygame.sprite.Group):
    def __init__(self):
        # camera setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # making sprites for mystery man
        self.forest0_surf = pygame.image.load('graphic/minigame/forest0.png')
        self.enemy0_surf = pygame.image.load('graphic/minigame/mystery_man_closeup.png')

        self.forest0_rect = self.forest0_surf.get_rect(topleft=(0, 0))
        self.enemy0_rect = self.enemy0_surf.get_rect(topleft=(1080, 200))

        # making sprites for wizard
        self.forest1_surf = pygame.image.load('graphic/minigame/forest.png')
        self.enemy1_surf = pygame.image.load('graphic/minigame/wizard_closeup.png')
        self.enemy1_dead_surf = pygame.image.load('graphic/minigame/hat.png')

        self.forest1_rect = self.forest1_surf.get_rect(topleft=(0, 0))
        self.enemy1_rect = self.enemy1_surf.get_rect(topleft=(1080, 200))
        self.enemy1_dead_rect = self.enemy1_surf.get_rect(topleft=(1280, 570))

        # making sprites
        self.code_paper_surf = pygame.image.load('graphic/minigame/code_paper.png')
        self.check_button_surf = pygame.image.load('graphic/minigame/check_button.png')

        self.code_paper_rect = self.code_paper_surf.get_rect(topleft=(0, 0))
        self.check_button_rect = self.check_button_surf.get_rect(center=(850, 750))

    def update_mystery_man(self):
        self.display_surface.blit(self.forest0_surf, self.forest0_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)
        self.display_surface.blit(self.enemy0_surf, self.enemy0_rect.topleft)

    def update_wizard_winning_scene(self):
        self.display_surface.blit(self.forest1_surf, self.forest1_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)
        self.display_surface.blit(self.enemy1_dead_surf, self.enemy1_dead_rect.topleft)

    def update_wizard(self):
        self.display_surface.blit(self.forest1_surf, self.forest1_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)
        self.display_surface.blit(self.enemy1_surf, self.enemy1_rect.topleft)

    def blink_button(self):
        enlarged_image_surf = pygame.transform.scale(self.check_button_surf, (450, 180))
        self.display_surface.blit(enlarged_image_surf, (625, 660))
        pygame.display.flip()
        pygame.time.delay(200)  # waiting 200 ms
