import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, font_name, size, screen, *groups):
        super().__init__(*groups)
        self.f = pygame.font.SysFont(font_name, size)
        self.user_text = []
        self.user_text.append("")
        self.cursor_index = 0
        self.cursor_row = 0
        self.screen = screen
        self.text_x = 140
        self.text_y = 110

        # self.curs_pos = pygame.math.Vector2
        # self.curs_pos = (140, 105)

    def render(self, text_to_render, x, y):
        text_surf = self.f.render(text_to_render, True, (255, 255, 255))
        self.screen.blit(text_surf, (x - text_surf.get_width() // 2, y - text_surf.get_height() // 2))

    def render_user_text(self):
        for i, row in enumerate(self.user_text):
            text_surf = self.f.render(row, True, (0, 0, 0))
            text_width, text_text_height = text_surf.get_size()
            self.screen.blit(text_surf, (self.text_x, self.text_y + i * text_text_height))

    def blink_cursor(self):
        cursor_rect = pygame.Rect(self.text_x, self.text_y, 2, 30)  # Cursor
        if self.cursor_index <= len(self.user_text[0]):
            cursor_rect.left += self.f.size(self.user_text[0][:self.cursor_index])[0]  # Moving cursor

        pygame.draw.rect(self.screen, 'black', cursor_rect)
        text_surf = self.f.render('|', True, (0, 0, 0))
        # render_to.blit(text_surf, self.curs_pos)

