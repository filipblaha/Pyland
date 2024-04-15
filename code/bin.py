import pygame
import sys

# Inicializace Pygame
pygame.init()

# Velikost okna
WIDTH, HEIGHT = 800, 600

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

# Proměnné pro zpracování opakovaného stisku kláves
key_repeat = (0, 0)
repeat_delay = 400
repeat_interval = 35

# Hlavní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
                key_repeat = (pygame.K_BACKSPACE, pygame.time.get_ticks() + repeat_delay)
            elif event.key == pygame.K_DELETE:
                text = text[:-1] if len(text) > 0 else text
                key_repeat = (pygame.K_DELETE, pygame.time.get_ticks() + repeat_delay)
            elif event.key == pygame.K_RETURN:
                text += '\n'
                key_repeat = (pygame.K_RETURN, pygame.time.get_ticks() + repeat_delay)
            elif event.key == pygame.K_SPACE:
                text += ' '
                key_repeat = (pygame.K_SPACE, pygame.time.get_ticks() + repeat_delay)
            else:
                text += event.unicode
                key_repeat = (event.key, pygame.time.get_ticks() + repeat_delay)
        elif event.type == pygame.KEYUP:
            key_repeat = (0, 0)

    # Zpracování opakovaného stisku kláves
    if key_repeat[0] and pygame.time.get_ticks() > key_repeat[1]:
        if pygame.key.get_pressed()[key_repeat[0]]:
            if key_repeat[0] == pygame.K_BACKSPACE:
                text = text[:-1]
            elif key_repeat[0] == pygame.K_DELETE:
                text = text[:-1] if len(text) > 0 else text
            elif key_repeat[0] == pygame.K_RETURN:
                text += '\n'
            elif key_repeat[0] == pygame.K_SPACE:
                text += ' '
            else:
                text += pygame.key.name(key_repeat[0])
            key_repeat = (key_repeat[0], pygame.time.get_ticks() + repeat_interval)

    # Renderování textu
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, text_area, 2)
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (text_area.x + 5, text_area.y + 5))

    # Renderování kurzoru
    if pygame.time.get_ticks() % 1000 > 500:  # Blikání kurzoru
        pygame.draw.rect(screen, BLACK, cursor)
    pygame.display.flip()

pygame.quit()
sys.exit()
