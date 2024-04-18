import pygame

from globalvariables import *


class Text:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 40)
        self.index = 0
        self.event = pygame.event.get()[0]
        self.event_key = 0

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

        self.repeat_delay = 1000
        self.repeat_interval = 40
        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def left_key(self):
        if self.cursor_index > 0:
            self.cursor_index -= 1
        elif self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = len(self.user_text[self.cursor_row])

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def right_key(self):
        if self.cursor_index < len(self.user_text[self.cursor_row]):
            self.cursor_index += 1
        elif self.cursor_row < len(self.user_text) - 1:
            self.cursor_row += 1
            self.cursor_index = 0

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def up_key(self):
        if self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = min(self.cursor_index, len(self.user_text[self.cursor_row]))

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def down_key(self):
        if self.cursor_row < len(self.user_text) - 1:
            self.cursor_row += 1
            self.cursor_index = min(self.cursor_index, len(self.user_text[self.cursor_row]))

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def enter(self):
        if len(self.user_text) + len(self.preset_text) <= 14:
            next_line = self.user_text[self.cursor_row][self.cursor_index:]
            self.user_text[self.cursor_row] = self.user_text[self.cursor_row][:self.cursor_index]
            self.user_text.insert(self.cursor_row + 1, next_line)

            self.cursor_row += 1
            self.cursor_index = 0

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def backspace(self):
        if self.cursor_index == 0 and self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_index = len(self.user_text[self.cursor_row])
            self.user_text[self.cursor_row] += self.user_text.pop(self.cursor_row + 1)

        elif self.cursor_index > 0:
            self.user_text[self.cursor_row] = (self.user_text[self.cursor_row][:self.cursor_index - 1] + self.user_text[self.cursor_row][self.cursor_index:])
            self.cursor_index -= 1

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

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

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def space(self):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + ' ' + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 1

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def tab(self):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + '    ' + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 4

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def other_keys(self):
        text = (self.user_text[self.cursor_row][:self.cursor_index] + self.event.unicode + self.user_text[self.cursor_row][self.cursor_index:])
        if self.check_bounding_box():
            self.user_text[self.cursor_row] = text
            self.cursor_index += 1

        self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_delay

    def buttons_pressed(self, event):
        if event:
            if event.type == pygame.KEYDOWN:
                self.event = event
                self.event_key = event.key
            if event.type == pygame.KEYUP:
                self.event = None
                self.event_key = None
                self.key_repeat_interval = 0

            if self.event_key == pygame.K_LEFT:
                self.left_key()

            elif self.event_key == pygame.K_RIGHT:
                self.right_key()

            elif self.event_key == pygame.K_UP:
                self.up_key()

            elif self.event_key == pygame.K_DOWN:
                self.down_key()

            elif self.event_key == pygame.K_KP_ENTER or self.event_key == pygame.K_RETURN:
                self.enter()

            elif self.event_key == pygame.K_BACKSPACE:
                self.backspace()

            elif self.event_key == pygame.K_DELETE:
                self.delete()

            elif self.event_key == pygame.K_SPACE:
                self.space()

            elif self.event_key == pygame.K_TAB:
                self.tab()

            elif self.event_key:
                self.other_keys()

        if self.event_key:
            self.repeat(event)

    def repeat(self, event):
        if self.event_key and pygame.time.get_ticks() > self.key_repeat_interval:
            if self.event_key == pygame.K_LEFT:
                self.left_key()

            elif self.event_key == pygame.K_RIGHT:
                self.right_key()

            elif self.event_key == pygame.K_UP:
                self.up_key()

            elif self.event_key == pygame.K_DOWN:
                self.down_key()

            elif self.event_key == pygame.K_KP_ENTER or self.event_key == pygame.K_RETURN:
                self.enter()

            elif self.event_key == pygame.K_BACKSPACE:
                self.backspace()

            elif self.event_key == pygame.K_DELETE:
                self.delete()

            elif self.event_key == pygame.K_SPACE:
                self.space()

            elif self.event_key == pygame.K_TAB:
                self.tab()

            else:
                self.other_keys()
            self.key_repeat_interval = pygame.time.get_ticks() + self.repeat_interval

    def check_bounding_box(self):
        width, height = self.font.size(self.user_text[self.cursor_row])
        if width >= self.max_width:
            return False
        else:
            return True

    def render_preset_text(self):
        if not self.preset_text == ['']:
            for i, row in enumerate(self.preset_text):
                text_surf = self.font.render(row, True, (255, 50, 50))
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
