import pygame

from globalvariables import *


class Text:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 40)
        a = pygame.KEYDOWN
        self.event = pygame.event.get()[0]

        self.display_surface = pygame.display.get_surface()
        self.user_text = []
        self.user_text.append("")
        self.user_text_height = 0
        self.preset_text = []
        self.preset_text_height = 0
        self.max_width = 470

        self.cursor_index = 0
        self.cursor_row = 0
        self.pos = pygame.Vector2(180, 272)
        self.blink_cursor_active = True

        self.key_repeated = (self.event, 0)
        self.repeat_delay = 400
        self.repeat_interval = 35

    def left_key(self, event):
        if self.cursor_index > 0:
            self.cursor_index -= 1
        elif self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = len(self.user_text[self.cursor_row])
        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def right_key(self, event):
        if self.cursor_index < len(self.user_text[self.cursor_row]):
            self.cursor_index += 1
        elif self.cursor_row < len(self.user_text) - 1:
            self.cursor_row += 1
            self.cursor_index = 0
        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def up_key(self, event):
        if self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = min(self.cursor_index, len(self.user_text[self.cursor_row]))
        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def down_key(self, event):
        if self.cursor_row < len(self.user_text) - 1:
            self.cursor_row += 1
            self.cursor_index = min(self.cursor_index, len(self.user_text[self.cursor_row]))
        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def enter(self, event):
        if len(self.user_text) + len(self.preset_text) <= 14:
            next_line = self.user_text[self.cursor_row][self.cursor_index:]
            self.user_text[self.cursor_row] = self.user_text[self.cursor_row][:self.cursor_index]
            self.user_text.insert(self.cursor_row + 1, next_line)

            self.cursor_row += 1
            self.cursor_index = 0

            self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def backspace(self, event):
        if self.cursor_index == 0 and self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = len(self.user_text[self.cursor_row])
            self.user_text[self.cursor_row] += self.user_text.pop(self.cursor_row + 1)

        elif self.cursor_index > 0:
            self.user_text[self.cursor_row] = (
                    self.user_text[self.cursor_row][:self.cursor_index - 1] + self.user_text[self.cursor_row][
                                                                              self.cursor_index:])
            self.cursor_index -= 1
        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def delete(self, event):
        if self.cursor_index < len(self.user_text[self.cursor_row]):
            self.user_text[self.cursor_row] = (
                    self.user_text[self.cursor_row][:self.cursor_index] + self.user_text[self.cursor_row][
                                                                          self.cursor_index + 1:])

        elif self.cursor_row < len(self.user_text) - 1:
            print(self.user_text[self.cursor_row][:] + self.user_text[self.cursor_row + 1][:])
            self.user_text[self.cursor_row] = (
                    self.user_text[self.cursor_row][:] + self.user_text[self.cursor_row + 1][:])
            self.user_text.pop(self.cursor_row + 1)
            print(0)
        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def space(self, event):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + ' ' + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 1

        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def tab(self, event):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + '    ' + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 4

        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def other_keys(self, event):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + event.unicode + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 1

        self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_delay)

    def buttons_pressed(self, event):
        if event:
            if event.type == pygame.KEYDOWN:
                self.event = event
            elif event.type == pygame.KEYUP:
                # self.key_repeated = (self.event, 0)

            if True in pygame.key.get_pressed():
                if self.event.key == pygame.K_LEFT:
                    self.left_key(self.event)

                elif self.event.key == pygame.K_RIGHT:
                    self.right_key(self.event)

                elif self.event.key == pygame.K_UP:
                    self.up_key(self.event)

                elif self.event.key == pygame.K_DOWN:
                    self.down_key(self.event)

                elif self.event.key == pygame.K_KP_ENTER or self.event.key == pygame.K_RETURN:
                    self.enter(self.event)

                elif self.event.key == pygame.K_BACKSPACE:
                    self.backspace(self.event)

                elif self.event.key == pygame.K_DELETE:
                    self.delete(self.event)

                elif self.event.key == pygame.K_SPACE:
                    self.space(self.event)

                elif self.event.key == pygame.K_TAB:
                    self.tab(self.event)

                else:
                    self.other_keys(self.event)
                # self.repeat_key(self.event)

    # def repeat_key(self, event):
    #     if pygame.time.get_ticks() > self.key_repeated[1]:
    #         if self.key_repeated[0].key == pygame.K_LEFT:
    #             self.left_key(event)
    #
    #         elif self.key_repeated[0].key == pygame.K_RIGHT:
    #             self.right_key(event)
    #
    #         elif self.key_repeated[0].key == pygame.K_UP:
    #             self.up_key(event)
    #
    #         elif self.key_repeated[0].key == pygame.K_DOWN:
    #             self.down_key(event)
    #
    #         elif self.key_repeated[0].key == pygame.K_KP_ENTER:
    #             self.enter(event)
    #
    #         elif self.key_repeated[0].key == pygame.K_BACKSPACE:
    #             self.backspace(event)
    #
    #         elif self.key_repeated[0].key == pygame.K_DELETE:
    #             self.delete(event)
    #
    #         elif self.key_repeated[0].key == pygame.K_SPACE:
    #             self.space(event)
    #
    #         elif self.key_repeated[0].key == pygame.K_TAB:
    #             self.tab(event)
    #         else:
    #             self.other_keys(event)
    #         self.key_repeated = (event, pygame.time.get_ticks() + self.repeat_interval)

    def check_bounding_box(self):
        width, height = self.font.size(self.user_text[self.cursor_row])
        if width >= self.max_width:
            return False
        else:
            return True

    def render_preset_text(self):
        if not self.preset_text == ['']:
            for i, row in enumerate(self.preset_text):
                text_surf = self.font.render(row, True, (200, 0, 200))
                text_width, self.preset_text_height = text_surf.get_size()

                text_x = self.pos.x
                text_y = self.pos.y + i * self.preset_text_height
                self.display_surface.blit(text_surf, (text_x, text_y))

    def render_user_text(self):
        for i, row in enumerate(self.user_text):
            text_surf = self.font.render(row, True, 'black')
            text_width, self.user_text_height = text_surf.get_size()

            text_x = self.pos.x
            text_y = self.pos.y + i * self.user_text_height + len(self.preset_text) * self.preset_text_height
            self.display_surface.blit(text_surf, (text_x, text_y))

    def blink_cursor(self):
        if self.blink_cursor_active:
            cursor_x = self.pos.x + self.font.size(self.user_text[self.cursor_row][:self.cursor_index])[0]
            cursor_y = self.pos.y + len(
                self.preset_text) * self.preset_text_height + self.cursor_row * self.user_text_height
            cursor_rect = pygame.Rect(cursor_x, cursor_y, 2, 40)
            pygame.draw.rect(self.display_surface, 'black', cursor_rect)

            self.blink_cursor_active = False
