import pygame.sprite
from text import *
from IDEsprites import *
from hud import *
from parse import *
from dialogwindow import *


class IDE:
    def __init__(self, glob, data):
        self.data = data
        self.globals = glob

        self.display_surface = pygame.display.get_surface()
        self.sprite_group = pygame.sprite.Group()
        self.sprites = IDESprites(glob, self.display_surface, self.sprite_group)
        self.text = Text()
        self.current_time = pygame.time.get_ticks()
        self.cutscene_frame = 0

        self.correct_answer = False
        self.you_win = False
        self.skip_cutscene = False
        self.cutscene_on = False
        self.hint_active = False

        self.wizard_health = 10
        self.banned_words = ''
        self.ordered_words = ''
        self.console_message = []

        # mouse
        pygame.mouse.set_visible(False)

        self.dialog_window = DialogWindow('', 50, (1350, 130), 1000, 200)
        self.parse = Parse(glob)
        self.hud = HUD(self.dialog_window)
        self.dialog_window.active = True

        self.data_assignment = None
        self.data_preset_words = None
        self.data_text = []
        self.task = 0
        self.setup()
        self.tasks = [[0, 1, 2, 3], [4, 9, 15, 13], [[1], [4, 7], [5, 7, 9, 13], [-1]]]

    def setup(self):
        for num, item in enumerate(self.data.data):
            if item['Type'] == 'Goal':
                self.data_assignment = item['Data']
            if item['Type'] == 'Preset words':
                self.data_preset_words = item['Data']
            if item['Type'] == 'Text':
                self.data_text.append(item['Text'])

    def logic(self, dt, event):
        # timing

        self.globals.MINIGAME_SCENE = 1
        self.current_time = pygame.time.get_ticks()
        if self.current_time % 1000 < 500:
            self.text.blink_cursor_active = True

        if self.hint_active:
            self.text.preset_text = self.data_preset_words[self.task]['Hint']
        else:
            self.text.preset_text = self.data_preset_words[self.task]['No Hint']

        self.user_input(event)
        self.parse.update_code(self.text.preset_text, self.text.user_text)

        for task in zip(*self.tasks):
            self.dialog_window_select_text(task[0], task[1])
            self.progress(*task)

        self.sprites.set_scene()

    def progress(self, minigame_num, max_frames, stop_frames):
        if self.you_win:
            self.you_win = False
            self.hint_active = False
            self.task += 1
            self.globals.change_game_stage('OVER_WORLD')

        if self.globals.MINIGAME_SCENE == minigame_num:
            if self.cutscene_frame <= max_frames:
                for frame in stop_frames:
                    if self.cutscene_frame == frame:
                        self.cutscene_on = False
                        break
                    else:
                        self.cutscene_on = True

                if self.correct_answer:
                    self.cutscene_frame += 1
                    self.correct_answer = False

            else:
                self.you_win = True
                self.cutscene_frame = 0
                self.globals.MINIGAME_SCENE += 1
                self.text.user_text = ['']
                self.hud.text = []

    def dialog_window_select_text(self, task_num, max_frames):
        if self.globals.MINIGAME_SCENE == task_num and self.cutscene_frame <= max_frames:
            self.dialog_window.change_text(self.data_text[self.globals.MINIGAME_SCENE][self.cutscene_frame], 50)

    def user_input(self, event):
        if event:
            # escaping IDE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.globals.change_game_stage('OVER_WORLD')

            # typing
            elif not self.cutscene_on:
                self.text.buttons_pressed(event)

            # hint color
            if not self.hint_active:
                if self.hud.hint_rect.collidepoint(pygame.mouse.get_pos()):
                    self.hud.hint_color = 'red'
                else:
                    self.hud.hint_color = 'black'

            # pressing
            if self.cutscene_on:
                # skipping cutscene
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.cutscene_frame += 1
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # clicking on hint
                    if self.hud.hint_rect.collidepoint(pygame.mouse.get_pos()):
                        self.hint_active = True
                        self.hud.hint_color = 'red'

                    # clicking on button
                    if self.sprites.check_button_sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        self.sprites.blink_button_active = True

                        if self.globals.MINIGAME_SCENE == 0:
                            self.parse.check_code(self.data_assignment[self.globals.MINIGAME_SCENE], True)
                        else:
                            self.parse.check_code(self.data_assignment[self.globals.MINIGAME_SCENE])

                        msg = self.parse.console_message
                        self.correct_answer = self.check_if_correct(msg)
                        self.hud.format_message(msg)
                    # clicking on text
                    else:
                        self.mouse_cursor()

    def check_if_correct(self, message):
        if message is not None:
            if message == 'Well done!':
                self.hud.text_color = 'green'
                return True
            elif message == 'Code is valid. Complete the task':
                self.hud.text_color = 'yellow'
                return False
            else:
                self.hud.text_color = 'red'
                return False

    def mouse_cursor(self):
        x, y = pygame.mouse.get_pos()
        text_width = 0
        text_height = 0
        self.text.cursor_index = len(max(self.text.user_text, key=len))
        self.text.cursor_row = len(self.text.user_text) - 1

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
        self.hud.display_hint()
        self.dialog_window.display()

        # displaying error window
        self.hud.display_console_window()

        # self.ui.show_hint()
        self.text.render_preset_text()
        self.text.render_user_text()
        self.text.blink_cursor()
        self.sprites.blink_button()

        self.display_surface.blit(self.sprites.cursor_sprite.image, pygame.mouse.get_pos())
