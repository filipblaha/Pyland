import pygame

from globalvariables import *


class Text:
    def __init__(self):
        self.f = pygame.font.SysFont("Arial", 40)

        self.display_surface = pygame.display.get_surface()
        self.user_text = []
        self.user_text.append("")
        self.user_text_height = 0
        self.preset_text = []
        self.preset_text_height = 0

        self.cursor_index = 0
        self.cursor_row = 0
        self.pos = pygame.Vector2(200, 272)
        self.blink_cursor_active = True

    def buttons_pressed(self, event):
        # pressed LEFT KEY
        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.cursor_index > 0:
                    self.cursor_index -= 1
                elif self.cursor_row > 0:
                    self.cursor_row -= 1
                    self.cursor_index = len(self.user_text[self.cursor_row])

            # pressed RIGHT KEY
            elif event.key == pygame.K_RIGHT:
                if self.cursor_index < len(self.user_text[self.cursor_row]):
                    self.cursor_index += 1
                elif self.cursor_row < len(self.user_text) - 1:
                    self.cursor_row += 1
                    self.cursor_index = 0

            elif event.key == pygame.K_UP:
                if self.cursor_row > 0:
                    self.cursor_row -= 1
                    self.cursor_index = min(self.cursor_index, len(self.user_text[self.cursor_row]))
            elif event.key == pygame.K_DOWN:
                if self.cursor_row < len(self.user_text) - 1:
                    self.cursor_row += 1
                    self.cursor_index = min(self.cursor_index, len(self.user_text[self.cursor_row]))

            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                self.user_text.insert(self.cursor_row + 1, '')
                self.cursor_row += 1
                self.cursor_index = 0
            # pressed BACKSPACE
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_index == 0 and self.cursor_row > 0:
                    self.cursor_row -= 1
                    self.cursor_index = len(self.user_text[self.cursor_row])
                    self.user_text[self.cursor_row] += self.user_text.pop(self.cursor_row + 1)

                elif self.cursor_index > 0:
                    self.user_text[self.cursor_row] = (self.user_text[self.cursor_row][:self.cursor_index - 1]
                                                                 + self.user_text[self.cursor_row][self.cursor_index:])
                    self.cursor_index -= 1

            elif event.key == pygame.K_DELETE:
                if self.cursor_index < len(self.user_text[self.cursor_row]):
                    self.user_text[self.cursor_row] = (self.user_text[self.cursor_row][:self.cursor_index]
                                                                 + self.user_text[self.cursor_row][
                                                                   self.cursor_index + 1:])
                elif self.cursor_row < len(self.user_text) - 1:
                    self.user_text[self.cursor_row] = self.user_text.pop(self.cursor_row + 1)
                    # pressed SPACE
            elif event.key == pygame.K_SPACE:
                self.user_text[self.cursor_row] = (self.user_text[self.cursor_row][
                                                             :self.cursor_index] + ' ' +
                                                             self.user_text[self.cursor_row][
                                                             self.cursor_index:])
                self.cursor_index += 1
                pass
            elif event.key == pygame.K_TAB:
                self.user_text[self.cursor_row] = (self.user_text[self.cursor_row][
                                                         :self.cursor_index] + '    ' +
                                                         self.user_text[self.cursor_row][
                                                         self.cursor_index:])
                self.cursor_index += 4
            else:
                self.user_text[self.cursor_row] = (self.user_text[self.cursor_row][
                                                             :self.cursor_index] + event.unicode +
                                                             self.user_text[self.cursor_row][
                                                             self.cursor_index:])
                self.cursor_index += 1

    def render_preset_text(self):
        for i, row in enumerate(self.preset_text):
            text_surf = self.f.render(row, True, (50, 50, 50))
            text_width, self.preset_text_height = text_surf.get_size()

            text_x = self.pos.x
            text_y = self.pos.y + i * self.preset_text_height
            self.display_surface.blit(text_surf, (text_x, text_y))

    def render_user_text(self):
        for i, row in enumerate(self.user_text):
            text_surf = self.f.render(row, True, 'black')
            text_width, self.user_text_height = text_surf.get_size()

            text_x = self.pos.x
            text_y = self.pos.y + i * self.user_text_height + len(self.preset_text) * self.preset_text_height
            self.display_surface.blit(text_surf, (text_x, text_y))

    def blink_cursor(self):
        if self.blink_cursor_active:

            cursor_x = self.pos.x + self.f.size(self.user_text[self.cursor_row][:self.cursor_index])[0]
            cursor_y = self.pos.y + len(self.preset_text) * self.preset_text_height + self.cursor_row * self.user_text_height
            cursor_rect = pygame.Rect(cursor_x, cursor_y, 2, 40)
            pygame.draw.rect(self.display_surface, 'black', cursor_rect)

            self.blink_cursor_active = False
