import pygame
import sys

# Inicializace pygame
pygame.init()

# Nastavení velikosti okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Editor")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 32)

# Textová proměnná pro ukládání vstupu od uživatele
user_input = ""

# Proměnná pro sledování, zda je klávesa stisknutá
key_held = False
key_repeat_timer = 0
key_initial_delay = 500  # Zpoždění před opakováním (v milisekundách)
key_repeat_interval = 30  # Interval pro opakování stisku klávesy (v milisekundách)
pressing_event = None

# Hlavní smyčka hry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Pokud uživatel stiskne Enter, můžeme vytisknout text
                print("Uživatelský vstup:", user_input)
                # Můžete zde provést jakoukoliv další akci s uživatelským vstupem
                user_input = ""  # Vyčistíme vstup pro další zadávání
            elif event.key == pygame.K_BACKSPACE:
                # Pokud uživatel stiskne Backspace, odstraníme poslední znak
                user_input = user_input[:-1]
                # Nastavíme proměnnou pro sledování držení klávesy
                key_held = True
                key_repeat_timer = pygame.time.get_ticks() + key_initial_delay
                pressing_event = event
            else:
                # Jinak přidáme stisknutý znak do uživatelského vstupu
                user_input += event.unicode
                # Nastavíme proměnnou pro sledování držení klávesy
                key_held = True
                key_repeat_timer = pygame.time.get_ticks() + key_initial_delay
                pressing_event = event

    # Pokud je klávesa stále držena a uplynulo zpoždění před opakováním
    if key_held and pygame.time.get_ticks() > key_repeat_timer:

        if pressing_event.key == pygame.K_e:
            pass
        if pygame.key.get_pressed()[pressing_event.key]:
            if pressing_event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += pressing_event.unicode
            key_repeat_timer = pygame.time.get_ticks() + key_repeat_interval


    # Vyčištění obrazovky
    screen.fill(WHITE)

    # Vykreslení textu na obrazovku
    text_surface = font.render("Textový editor - Zadejte text:", True, BLACK)
    screen.blit(text_surface, (20, 20))
    input_surface = font.render(user_input, True, BLACK)
    screen.blit(input_surface, (20, 60))

    # Obnovení obrazovky
    pygame.display.flip()

# Ukončení pygame
pygame.quit()
sys.exit()
