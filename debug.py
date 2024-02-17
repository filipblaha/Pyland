import pygame
import sys

class DialogWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 32)
        self.dialog_color = (200, 200, 200)
        self.text_color = (0, 0, 0)

    def show_dialog(self, text, font_size, pos_x, pos_y, width, height, highlight_words=None, highlight_font=32, highlight_color=None):
        if highlight_words is None:
            highlight_words = []
        if highlight_color is None:
            highlight_color = (255, 0, 0)  # Default color is red

        lines, line_heights = self.split_lines(text, font_size, width - 50, highlight_words, highlight_color, highlight_font)
        dialog_height = sum(line_heights)
        dialog_rect = pygame.Rect(0, 0, width, height)
        dialog_rect.center = (pos_x, pos_y)
        pygame.draw.rect(self.screen, self.dialog_color, dialog_rect)

        y_offset = (height - dialog_height) // 2   # Calculate y_offset for vertical centering
        for i, (line, colors, sizes) in enumerate(lines):
            total_width = sum(self.font.size(word)[0] for word in line) + (len(line) - 1) * self.font.size(" ")[0]
            x_offset = (width - total_width) // 2
            for segment, color, size in zip(line, colors, sizes):
                text_surface = self.font.render(segment, True, color)
                text_rect = text_surface.get_rect(topleft=(pos_x - width // 2 + x_offset, pos_y - height // 2 + y_offset))
                self.screen.blit(text_surface, text_rect)
                if segment != line[-1]:
                    x_offset += self.font.size(segment)[0] + self.font.size(" ")[0]  # Add space width to x_offset
            y_offset += line_heights[i]

        pygame.display.flip()

    def split_lines(self, text, font_size, max_width, highlight_words, highlight_color, highlight_font):
        words = text.split()
        max_word_height = 0
        lines = []
        line_width = 0
        line_heights = []
        current_line = []
        line_colors = []
        current_font_size = []

        for word in words:
            if word in highlight_words:
                word_color = highlight_color
                word_font_size = highlight_font
                self.font = pygame.font.Font(None, highlight_font)
            else:
                word_color = self.text_color
                word_font_size = font_size
                self.font = pygame.font.Font(None, font_size)

            word_width, word_height = self.font.size(word)
            line_width += word_width
            if current_line:
                self.font = pygame.font.Font(None, font_size)
                space_w, space_h = self.font.size(' ')
                line_width += space_w

            if line_width < max_width:
                current_line.append(word)
                line_colors.append(word_color)
                current_font_size.append(word_font_size)
            else:
                lines.append((current_line[:], line_colors[:], current_font_size[:]))
                line_heights.append(max_word_height)
                line_colors = [word_color]
                current_line = [word]
                current_font_size = [word_font_size]
                line_width = 0
                max_word_height = 0
            if word_height > max_word_height:
                max_word_height = word_height

        lines.append((current_line, line_colors, current_font_size))
        line_heights.append(max_word_height)
        return lines, line_heights

def main():
    pygame.init()
    dialog = DialogWindow(1920, 1080)
    # print(pygame.font.Font(None, 32).size("p"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dialog.screen.fill((255, 255, 255))
        dialog.show_dialog(
            "Don't waste time and GO to the park", 32,
            1000, 500, 300, 200, highlight_words=["GO", "park"], highlight_font=40, highlight_color=(255, 0, 0))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
