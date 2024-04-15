import pygame
import sys

# Inicializace Pygame
pygame.init()

# Nastavení rozlišení obrazovky
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Textový editor s kurzorem")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 32)

# Text
text = ""
cursor_pos = 0
offset = 50

# Funkce pro vykreslení textu a kurzoru
def draw_text(surface, text, font, color, rect):
    surface.fill(WHITE)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, rect)

def main():
    global text, cursor_pos

    clock = pygame.time.Clock()
    input_active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        if cursor_pos > 0:
                            text = text[:cursor_pos - 1] + text[cursor_pos:]
                            cursor_pos -= 1
                    elif event.key == pygame.K_LEFT:
                        if cursor_pos > 0:
                            cursor_pos -= 1
                    elif event.key == pygame.K_RIGHT:
                        if cursor_pos < len(text):
                            cursor_pos += 1
                    elif event.key == pygame.K_RETURN:
                        text = text[:cursor_pos] + '\n' + text[cursor_pos:]
                        cursor_pos += 1
                    else:
                        text = text[:cursor_pos] + event.unicode + text[cursor_pos:]
                        cursor_pos += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_active:
                    x, y = pygame.mouse.get_pos()
                    cursor_pos = len(text)
                    text_width = 0
                    for i in range(len(text)):
                        text_width += font.size(text[i])[0]
                        if text_width >= x - offset:
                            cursor_pos = i
                            break


        # Vykreslení textu a kurzoru
        draw_text(screen, text, font, BLACK, pygame.Rect(offset, 10, WIDTH - 20, HEIGHT - 20))

        # Vykreslení kurzoru
        if input_active:
            cursor_x = font.size(text[:cursor_pos])[0] + offset
            pygame.draw.line(screen, BLACK, (cursor_x, 12), (cursor_x, 38), 2)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
