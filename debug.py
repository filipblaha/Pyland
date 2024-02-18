import pygame
import sys


class DialogWindow:
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 32)
        self.dialog_color = (200, 200, 200)
        self.text_color = (0, 0, 0)

    def show_dialog(self, text, font_size, pos_x, pos_y, width, height, highlight_words=None, highlight_font_size=None, highlight_color=None):
        """
        Call the function to create a dialog window.

         REQUIRED arguments: Text and font size. Position and size of the window.

         OPTIONAL arguments: You can highlight words from the text (change their size and color).

        :param text:
        :param pos_x:
        :param pos_y:
        :param width:
        :param height:
        :param font_size:
        :param highlight_words:
        :param highlight_font_size:
        :param highlight_color:
        :return:
        """

        # default settings for highlighted words
        if highlight_words is None:
            highlight_words = []
        if highlight_font_size is None:
            highlight_color = 'red'
        if highlight_color is None:
            highlight_color = 'red'

        # formatting the text string - splitting into rows, calculating heights
        # lines is list of segments of a line(words), font sizes and colors for each word
        lines, line_heights = self.split_lines(text, font_size, width - 50, highlight_words, highlight_color, highlight_font_size)

        # drawing dialog window
        dialog_rect = pygame.Rect(0, 0, width, height)
        dialog_rect.center = (pos_x, pos_y)
        pygame.draw.rect(self.screen, self.dialog_color, dialog_rect)

        dialog_height = sum(line_heights)

        # taking formatted string (lines) and using the for cycle goes through every row
        for i, (line, colors, sizes) in enumerate(lines):

            # calculating total width of a line for the offset
            total_width = (len(line) - 1) * self.font.size(" ")[0]
            for word, size in zip(line, sizes):
                self.font = pygame.font.Font(None, size)
                word_w, word_h = self.font.size(word)
                total_width += word_w

            # first x_offset in line
            x_offset = (width - total_width) // 2

            # goes through every word in line - setting size, color and offset
            for segment, color, size in zip(line, colors, sizes):

                # font size of each word
                self.font = pygame.font.Font(None, size)
                this_font_width, this_font_height = self.font.size(segment)

                # offsets to
                # offsets words to the center of a line, some words can be bigger than others
                y_offset = (height - dialog_height + line_heights[i] - this_font_height) // 2 + sum(line_heights[:i])

                # rendering words
                text_surface = self.font.render(segment, True, color)
                text_rect = text_surface.get_rect(topleft=(pos_x - width // 2 + x_offset, pos_y - height // 2 + y_offset))
                self.screen.blit(text_surface, text_rect)

                # adding spaces between the words
                if segment != line[-1]:
                    x_offset += self.font.size(segment)[0] + self.font.size(" ")[0]

    def split_lines(self, text, font_size, max_width, highlight_words, highlight_color, highlight_font):
        # splitting string into a list of words
        words = text.split()

        line_width = 0              # integer that watches if the line width isn't too long
        max_word_height = 0         # integer that watches the highest words
        line_heights = []           # list of max line heights for y_offset

        lines = []                  # list of words, font sizes, colors
        current_color = []            # list of colors
        current_line = []           # list of words
        current_font_size = []      # list of font sizes

        # goes through every word in the text
        for word in words:
            if word in highlight_words:
                word_color = highlight_color
                word_font_size = highlight_font
                self.font = pygame.font.Font(None, highlight_font)
            else:
                word_color = self.text_color
                word_font_size = font_size
                self.font = pygame.font.Font(None, font_size)

            # adding word width
            word_width, word_height = self.font.size(word)
            line_width += word_width

            # adding space width after every word except the first one to line_width
            if current_line:
                self.font = pygame.font.Font(None, font_size)
                space_w, space_h = self.font.size(' ')
                line_width += space_w

            # checking if the line width isn't too long
            if line_width < max_width:
                # adding word, color and size
                current_line.append(word)
                current_color.append(word_color)
                current_font_size.append(word_font_size)
            else:
                # adding lists to lines(final list with words, font sizes, colors) height of the biggest word
                lines.append((current_line[:], current_color[:], current_font_size[:]))
                # and height of the biggest word
                line_heights.append(max_word_height)

                # resetting current lists
                # adding word that exceeds max line width with its color and font size to the next row
                current_line = [word]
                current_color = [word_color]
                current_font_size = [word_font_size]
                # resetting line width and max word height
                line_width = 0
                max_word_height = 0

            # checking the highest word
            if word_height > max_word_height:
                max_word_height = word_height

        # adding each row to lines
        lines.append((current_line, current_color, current_font_size))
        # adding the biggest height to each row to lines heights
        line_heights.append(max_word_height)
        return lines, line_heights


def main():
    pygame.init()
    dialog = DialogWindow(1920, 1080)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dialog.screen.fill((255, 255, 255))
        dialog.show_dialog("Don't waste time and GO !!!", 1000, 500, 300, 200, 32, ["GO", "Don't"], 80, "red")

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
