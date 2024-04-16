import pygame

from globalvariables import *


class Text:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 40)

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

        self.key_repeat = (0, 0)
        self.repeat_delay = 400
        self.repeat_interval = 35

    def left_key(self):
        if self.cursor_index > 0:
            self.cursor_index -= 1
        elif self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = len(self.user_text[self.cursor_row])
        self.key_repeat = (pygame.K_LEFT, pygame.time.get_ticks() + self.repeat_delay)

    def right_key(self):
        if self.cursor_index < len(self.user_text[self.cursor_row]):
            self.cursor_index += 1
        elif self.cursor_row < len(self.user_text) - 1:
            self.cursor_row += 1
            self.cursor_index = 0
        self.key_repeat = (pygame.K_RIGHT, pygame.time.get_ticks() + self.repeat_delay)

    def up_key(self):
        if self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = min(self.cursor_index, len(self.user_text[self.cursor_row]))
        self.key_repeat = (pygame.K_UP, pygame.time.get_ticks() + self.repeat_delay)

    def down_key(self):
        if self.cursor_row < len(self.user_text) - 1:
            self.cursor_row += 1
            self.cursor_index = min(self.cursor_index, len(self.user_text[self.cursor_row]))
        self.key_repeat = (pygame.K_DOWN, pygame.time.get_ticks() + self.repeat_delay)

    def enter(self):
        if len(self.user_text) + len(self.preset_text) <= 14:
            next_line = self.user_text[self.cursor_row][self.cursor_index:]
            self.user_text[self.cursor_row] = self.user_text[self.cursor_row][:self.cursor_index]
            self.user_text.insert(self.cursor_row + 1, next_line)

            self.cursor_row += 1
            self.cursor_index = 0

            self.key_repeat = (pygame.K_KP_ENTER, pygame.time.get_ticks() + self.repeat_delay)

    def backspace(self):
        if self.cursor_index == 0 and self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = len(self.user_text[self.cursor_row])
            self.user_text[self.cursor_row] += self.user_text.pop(self.cursor_row + 1)

        elif self.cursor_index > 0:
            self.user_text[self.cursor_row] = (
                    self.user_text[self.cursor_row][:self.cursor_index - 1] + self.user_text[self.cursor_row][
                                                                              self.cursor_index:])
            self.cursor_index -= 1
        self.key_repeat = (pygame.K_BACKSPACE, pygame.time.get_ticks() + self.repeat_delay)

    def delete(self):
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
        self.key_repeat = (pygame.K_DELETE, pygame.time.get_ticks() + self.repeat_delay)

    def space(self):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + ' ' + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 1

        self.key_repeat = (pygame.K_SPACE, pygame.time.get_ticks() + self.repeat_delay)

    def tab(self):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + '    ' + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 4

        self.key_repeat = (pygame.K_TAB, pygame.time.get_ticks() + self.repeat_delay)

    def other_keys(self, key):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + pygame.key.name(key) + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 1

        self.key_repeat = (key, pygame.time.get_ticks() + self.repeat_delay)

    def buttons_pressed(self, event):
        ignored_keys = [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_CAPSLOCK,
                        pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_INSERT, pygame.K_HOME,
                        pygame.K_END, pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_PRINTSCREEN]

        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left_key()

            elif event.key == pygame.K_RIGHT:
                self.right_key()

            elif event.key == pygame.K_UP:
                self.up_key()

            elif event.key == pygame.K_DOWN:
                self.down_key()

            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.enter()

            elif event.key == pygame.K_BACKSPACE:
                self.backspace()

            elif event.key == pygame.K_DELETE:
                self.delete()

            elif event.key == pygame.K_SPACE:
                self.space()

            elif event.key == pygame.K_TAB:
                self.tab()
            # numpad
            elif event.key == pygame.K_KP0:
                self.other_keys(pygame.K_0)
            elif event.key == pygame.K_KP1:
                self.other_keys(pygame.K_1)
            elif event.key == pygame.K_KP2:
                self.other_keys(pygame.K_2)
            elif event.key == pygame.K_KP3:
                self.other_keys(pygame.K_3)
            elif event.key == pygame.K_KP4:
                self.other_keys(pygame.K_4)
            elif event.key == pygame.K_KP5:
                self.other_keys(pygame.K_5)
            elif event.key == pygame.K_KP6:
                self.other_keys(pygame.K_6)
            elif event.key == pygame.K_KP7:
                self.other_keys(pygame.K_7)
            elif event.key == pygame.K_KP8:
                self.other_keys(pygame.K_8)
            elif event.key == pygame.K_KP9:
                self.other_keys(pygame.K_9)
            elif event.key == pygame.K_KP_MINUS:
                self.other_keys(pygame.K_MINUS)
            elif event.key == pygame.K_KP_PLUS:
                self.other_keys(pygame.K_PLUS)
            elif event.key == pygame.K_KP_DIVIDE:
                self.other_keys(pygame.K_SLASH)
            elif event.key == pygame.K_KP_MULTIPLY:
                self.other_keys(pygame.K_ASTERISK)
            elif event.key == pygame.K_KP_PERIOD:
                self.other_keys(pygame.K_PERIOD)

            elif event.key == pygame.K_KP9:
                self.other_keys(pygame.K_9)

            elif event.key not in ignored_keys:
                self.other_keys(event.key)

            elif event.type == pygame.KEYUP:
                self.key_repeat = (0, 0)

        self.repeat_key()

    def repeat_key(self):
        if self.key_repeat[0] and pygame.time.get_ticks() > self.key_repeat[1]:
            if pygame.key.get_pressed()[self.key_repeat[0]]:
                if self.key_repeat[0] == pygame.K_LEFT:
                    self.left_key()

                elif self.key_repeat[0] == pygame.K_RIGHT:
                    self.right_key()

                elif self.key_repeat[0] == pygame.K_UP:
                    self.up_key()

                elif self.key_repeat[0] == pygame.K_DOWN:
                    self.down_key()

                elif self.key_repeat[0] == pygame.K_KP_ENTER:
                    self.enter()

                elif self.key_repeat[0] == pygame.K_BACKSPACE:
                    self.backspace()

                elif self.key_repeat[0] == pygame.K_DELETE:
                    self.delete()

                elif self.key_repeat[0] == pygame.K_SPACE:
                    self.space()

                elif self.key_repeat[0] == pygame.K_TAB:
                    self.tab()

                else:
                    self.other_keys(self.key_repeat[0])
                self.key_repeat = (self.key_repeat[0], pygame.time.get_ticks() + self.repeat_interval)

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
