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

# Textový řetězec
text = []
cursor_index = 0  # Index aktuální pozice kursoru

# Hlavní smyčka hry
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Vykreslení textu
    rendered_text = ''.join(text)
    text_surface = font.render(rendered_text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (10, 10)
    screen.blit(text_surface, text_rect)

    # Vykreslení kursoru
    cursor_rect = pygame.Rect(text_rect.left, text_rect.top, 2, text_rect.height)  # Šířka kursoru je 2px
    if cursor_index <= len(text):
        cursor_rect.left += font.size(rendered_text[:cursor_index])[0]  # Posun kursoru za aktuální znak

    pygame.draw.rect(screen, BLACK, cursor_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if cursor_index > 0:
                    del text[cursor_index - 1]
                    cursor_index -= 1
            elif event.key == pygame.K_LEFT:
                if cursor_index > 0:
                    cursor_index -= 1
            elif event.key == pygame.K_RIGHT:
                if cursor_index < len(text):
                    cursor_index += 1
            else:
                if event.unicode.isprintable():
                    text.insert(cursor_index, event.unicode)
                    cursor_index += 1

    clock.tick(60)

# Ukončení Pygame
pygame.quit()
sys.exit()