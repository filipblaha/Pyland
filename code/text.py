from globalvariables import *


class Text:
    def __init__(self, display_surface):
        self.f = pygame.font.SysFont("Arial", 27)

        self.display_surface = display_surface
        self.user_text = []
        self.user_text.append("")
        self.preset_text = []
        self.preset_text_height = 0

        self.cursor_index = 0
        self.cursor_row = 0
        self.text_x = 140
        self.text_y = 110

    def render_preset_text(self):
        for i, row in enumerate(self.preset_text):
            text_surf = self.f.render(row, True, (50, 50, 50))
            text_width, self.preset_text_height = text_surf.get_size()
            self.display_surface.blit(text_surf, (self.text_x, self.text_y + i * self.preset_text_height))

    def render_user_text(self):
        for i, row in enumerate(self.user_text):
            text_surf = self.f.render(row, True, 'black')
            text_width, text_height = text_surf.get_size()
            self.display_surface.blit(text_surf, (self.text_x, len(self.preset_text) * self.preset_text_height + self.text_y + i * text_height))

    def blink_cursor(self):
        cursor_rect = pygame.Rect(self.text_x + self.f.size(self.user_text[self.cursor_row][:self.cursor_index])[0],
                                  len(self.preset_text) * self.preset_text_height + self.text_y + self.cursor_row * 31,
                                  2, 30)  # Cursor
        pygame.draw.rect(self.display_surface, 'black', cursor_rect)