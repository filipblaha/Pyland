import pygame.sprite
from text import *
from IDEsprites import *
from hud import *
from test_code import *
from dialogwindow import *


class IDE:
    def __init__(self, glob, data):
        self.data = data
        self.globals = glob

        self.display_surface = pygame.display.get_surface()
        self.sprite_group = pygame.sprite.Group()
        self.sprites = IDESprites(self.display_surface, self.sprite_group)
        self.text = Text()
        self.current_time = pygame.time.get_ticks()
        self.minigame_num = 0
        self.cutscene_frame = 0
        self.correct_answer = False
        self.you_win = False
        self.skip_cutscene = False
        self.cutscene_on = False
        self.hint_active = False

        pygame.mouse.set_visible(True)

        self.wizard_health = 10
        self.banned_words = ''
        self.ordered_words = ''

        # mouse
        pygame.mouse.set_visible(False)

        self.dialog_window = DialogWindow('', 50, (1300, 130), 800, 200)
        self.dialog_window.change_text('Try the for cycle !', 50, ['for', 'cycle'])
        self.parse = Parse()
        self.hud = HUD()
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

    def logic(self, dt, event):
        # timing
        self.current_time = pygame.time.get_ticks()
        if self.current_time % 1000 < 500:
            self.text.blink_cursor_active = True

        #
        if self.hint_active:
            self.text.preset_text = self.data_preset_words[self.globals.MINIGAME_SCENE]['Hint']
        else:
            self.text.preset_text = self.data_preset_words[self.globals.MINIGAME_SCENE]['No Hint']

        self.user_input(event)
        self.parse.update_code(self.text.preset_text, self.text.user_text)

        self.sprites.set_scene()

    def user_input(self, event):

        # text editor
        self.text.buttons_pressed(event)

        if event and event.type == pygame.MOUSEBUTTONDOWN:
            # escaping IDE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.globals.change_game_stage('OVER_WORLD')

            # checking code
            if self.sprites.check_button_sprite.rect.collidepoint(pygame.mouse.get_pos()):
                self.sprites.blink_button_active = True
                self.parse.check_code(self.data_assignment[self.globals.MINIGAME_SCENE])
            else:
                x, y = pygame.mouse.get_pos()
                text_width = 0
                text_height = 0
                self.text.cursor_index = len(max(self.text.user_text, key=len))
                self.text.cursor_row = len(self.text.user_text)-1

                for i in range(len(self.text.user_text)):
                    text_height += self.text.user_text_height
                    if text_height >= y - (self.text.pos.y + len(self.text.preset_text) * self.text.preset_text_height):
                        self.text.cursor_row = i
                        break

                for i in range(len(self.text.user_text[self.text.cursor_row])):
                    text_width += self.text.font.size(self.text.user_text[self.text.cursor_row][i])[0]
                    if text_width >= x - self.text.pos.x:
                        self.text.cursor_index = i
                        break
    def render(self):
        self.sprite_group.draw(self.display_surface)
        self.dialog_window.display()

        # displaying error window
        self.hud.display_error_window(self.parse.error_message)

        # self.ui.show_hint()
        self.text.render_preset_text()
        self.text.render_user_text()
        self.text.blink_cursor()
        self.sprites.blink_button()

        self.display_surface.blit(self.sprites.cursor_sprite.image, pygame.mouse.get_pos())
