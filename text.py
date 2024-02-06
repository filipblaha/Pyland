import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, font_name, size, *groups):
        super().__init__(*groups)
        self.f = pygame.font.SysFont(font_name, size)
        self.user_text = []
        self.user_text.append("")

    def render(self, render_to, text_to_render, x, y):
        text_surf = self.f.render(text_to_render, True, (255, 255, 255))
        render_to.display.blit(text_surf, (x - text_surf.get_width() // 2, y - text_surf.get_height() // 2))

    def render_user_text(self, render_to, x, y):
        text_height = 0
        for i, row in enumerate(self.user_text):
            text_surf = self.f.render(row, True, (0, 0, 0))
            text_width, text_text_height = text_surf.get_size()
            render_to.display.blit(text_surf, (x, y + i * text_text_height))
            text_height = text_text_height

