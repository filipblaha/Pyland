from globalvariables import *


class DialogWindow:
    def __init__(self, text, font_size, pos: tuple, width, height, highlight_words=None, highlight_font_size=None, highlight_color=None):
        """
            REQUIRED arguments: Text and font size. Position and size of the window.

            OPTIONAL arguments: You can highlight words from the text (change their size and color).

            :param text:
            :param font_size:
            :param pos:
            :param width:
            :param height:
            :param highlight_words:
            :param highlight_font_size:
            :param highlight_color:
        """

        self.display_surface = pygame.display.get_surface()
        self.dialog_color = (200, 200, 200)
        self.text_color = (0, 0, 0)
        self.lines = []
        self.line_heights = []
        self.fonts = []

        self.text = text
        self.font_size = font_size
        self.pos = pygame.Vector2(pos)
        self.width = width
        self.height = height
        self.max_width = width - 50

        # highlighted words
        if highlight_words is None or highlight_words == []:
            self.highlight_words = []
        else:
            self.highlight_words = highlight_words

        # font
        if highlight_font_size is None or highlight_words == 0:
            self.highlight_font_size = 0
        else:
            self.highlight_font_size = highlight_font_size

        if highlight_color is None or highlight_words == (0, 0, 0):
            self.highlight_color = (0, 0, 0)
            self.lines, self.line_heights = self.split_lines()
        else:
            self.highlight_color = highlight_color

    def display(self):
        """
        Display of the dialog window.
        """

        # drawing dialog window
        dialog_rect = pygame.Rect(0, 0, self.width, self.height)
        dialog_rect.center = (self.pos.x, self.pos.y)
        pygame.draw.rect(self.display_surface, self.dialog_color, dialog_rect)

        dialog_height = sum(self.line_heights)

        # taking formatted string (lines) and using the for cycle goes through every row
        for i, (line, fonts, surfaces) in enumerate(self.lines):

            # calculating total width of a line for the offset
            total_width = (len(line) - 1) * fonts[0].size(" ")[0]
            for word, font in zip(line, fonts):
                word_w, word_h = font.size(word)
                total_width += word_w

            # first x_offset in line
            x_offset = (self.width - total_width) // 2

            # goes through every word in line - setting size, color and offset
            for word, font, surface in zip(line, fonts, surfaces):

                # font size of each word
                this_font_width, this_font_height = font.size(word)

                # offsets to
                # offsets words to the center of a line, some words can be bigger than others
                y_offset = (self.height - dialog_height + self.line_heights[i] - this_font_height) // 2 + sum(self.line_heights[:i])

                # rendering words
                text_rect = surface.get_rect(topleft=(self.pos.x - self.width // 2 + x_offset, self.pos.y - self.height // 2 + y_offset))
                self.display_surface.blit(surface, text_rect)

                # adding spaces between the words
                if word != line[-1]:
                    x_offset += font.size(word)[0] + font.size(" ")[0]

    def split_lines(self):
        # splitting string into a list of words with its properties
        words = self.text.split()

        line_width = 0              # integer that watches if the line width isn't too long
        max_word_height = 0         # integer that watches the highest words
        line_heights = []           # list of max line heights for y_offset

        lines = []                  # list of words, fonts and surfaces
        current_line = []           # list of words
        current_font = []           # list of fonts
        current_surf = []           # list of surfaces

        # goes through every word in the text
        for word in words:
            if word in self.highlight_words:
                word_color = self.highlight_color
                font = pygame.font.Font(FONT, self.highlight_font_size)
                word_surf = font.render(word, True, word_color)
            else:
                word_color = self.text_color
                font = pygame.font.Font(FONT, self.font_size)
                word_surf = font.render(word, True, word_color)

            # adding word width
            word_width, word_height = font.size(word)
            line_width += word_width

            # adding space width after every word except the first one to line_width
            if current_line:
                font_space = pygame.font.Font(FONT, self.font_size)
                space_w, space_h = font_space.size(' ')
                line_width += space_w

            # checking if the line width isn't too long
            if line_width < self.max_width:
                # adding word, font and surface
                current_line.append(word)
                current_font.append(font)
                current_surf.append(word_surf)
            else:
                # adding lists to lines(final list with words, fonts, surfaces)
                lines.append((current_line[:], current_font[:], current_surf[:]))
                # and height of the biggest word
                line_heights.append(max_word_height)

                # resetting current lists
                # adding word that exceeds max line width with its properties to the next row
                current_line = [word]
                current_font = [font]
                current_surf = [word_surf]
                # resetting line width and max word height
                line_width = 0
                max_word_height = 0

            # checking the highest word
            if word_height > max_word_height:
                max_word_height = word_height

        # adding each row to lines
        lines.append((current_line, current_font, current_surf))
        # adding the biggest height to each row to lines heights
        line_heights.append(max_word_height)
        return lines, line_heights
