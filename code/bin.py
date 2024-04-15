import pygame
import sys

# Inicializace Pygame
pygame.init()

# Velikost okna
WIDTH, HEIGHT = 800, 600

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Velikost fontu a typ fontu
FONT_SIZE = 24
font = pygame.font.Font(None, FONT_SIZE)

# Vytvoření okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Editor")

# Textová plocha
text_area = pygame.Rect(10, 10, WIDTH - 20, HEIGHT - 20)
text = ""
cursor = pygame.Rect(10, 10, 1, FONT_SIZE)
selection = None

# Hlavní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if selection:
                    start, end = sorted(selection)
                    text = text[:start] + text[end:]
                    cursor.topleft = (text_area.left + font.size(text[:start])[0], text_area.top)
                    selection = None
                else:
                    text = text[:-1]
            elif event.key == pygame.K_RETURN:
                text += '\n'
            else:
                text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cursor.topleft = event.pos
                selection = event.pos, event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selection = None
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:  # Pokud tlačítko myši je stisknuto
                selection = selection[0], event.pos

    # Renderování textu
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, text_area, 2)
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (text_area.x + 5, text_area.y + 5))

    # Renderování vybraného textu
    if selection:
        start, end = sorted((cursor.topleft, selection[0]))
        selection_surface = pygame.Surface((end[0] - start[0], FONT_SIZE))
        selection_surface.set_alpha(100)
        selection_surface.fill(GRAY)
        screen.blit(selection_surface, start)

    # Renderování kurzoru
    if pygame.time.get_ticks() % 1000 > 500:  # Blikání kurzoru
        pygame.draw.rect(screen, BLACK, cursor)
    pygame.display.flip()

pygame.quit()
sys.exit()
