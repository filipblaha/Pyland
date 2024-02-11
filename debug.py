import pygame
import sys

# Inicializace Pygame
pygame.init()

# Nastavení rozměrů okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Textový editor")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Písmo pro text
font_name = pygame.font.get_default_font()
font_size = 36
font = pygame.font.SysFont(font_name, font_size)

# Textový řetězec (seznam řádků)
text = ['']  # Začneme s jedním prázdným řádkem
cursor_x, cursor_y = 0, 0  # Pozice kurzoru (pozice x, pozice y)

# Hlavní smyčka hry
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Vykreslení textu
    for i, line in enumerate(text):
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10 + i * font_size)
        screen.blit(text_surface, text_rect)

    # Vykreslení kursoru
    cursor_rect = pygame.Rect(10 + font.size(text[cursor_y][:cursor_x])[0], 10 + cursor_y * font_size, 2,
                              font_size)  # Šířka kursoru je 2px
    pygame.draw.rect(screen, BLACK, cursor_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Klávesa Enter
                text.insert(cursor_y + 1, '')
                cursor_y += 1
                cursor_x = 0
            elif event.key == pygame.K_BACKSPACE:
                if cursor_x == 0 and cursor_y > 0:
                    cursor_y -= 1
                    cursor_x = len(text[cursor_y])
                    text[cursor_y] += text.pop(cursor_y + 1)
                elif cursor_x > 0:
                    text[cursor_y] = text[cursor_y][:cursor_x - 1] + text[cursor_y][cursor_x:]
                    cursor_x -= 1
            elif event.key == pygame.K_DELETE:
                if cursor_x < len(text[cursor_y]):
                    text[cursor_y] = text[cursor_y][:cursor_x] + text[cursor_y][cursor_x + 1:]
                elif cursor_y < len(text) - 1:
                    text[cursor_y] += text.pop(cursor_y + 1)
            elif event.key == pygame.K_LEFT:
                if cursor_x > 0:
                    cursor_x -= 1
                elif cursor_y > 0:
                    cursor_y -= 1
                    cursor_x = len(text[cursor_y])
            elif event.key == pygame.K_RIGHT:
                if cursor_x < len(text[cursor_y]):
                    cursor_x += 1
                elif cursor_y < len(text) - 1:
                    cursor_y += 1
                    cursor_x = 0
            elif event.key == pygame.K_UP:
                if cursor_y > 0:
                    cursor_y -= 1
                    cursor_x = min(cursor_x, len(text[cursor_y]))
            elif event.key == pygame.K_DOWN:
                if cursor_y < len(text) - 1:
                    cursor_y += 1
                    cursor_x = min(cursor_x, len(text[cursor_y]))
            else:
                if event.unicode.isprintable():
                    text[cursor_y] = text[cursor_y][:cursor_x] + event.unicode + text[cursor_y][cursor_x:]
                    cursor_x += 1

    clock.tick(60)

# Ukončení Pygame
pygame.quit()
sys.exit()