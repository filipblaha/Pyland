import pygame
import sys

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Testování polygonu")

# Definice barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definice polygonu
polygon_vertices = [(100, 100), (200, 50), (300, 150), (250, 300), (150, 300), (300, 150), (250, 300), (150, 300), (100, 100), (200, 50), (300, 150), (250, 300),]

def barrier_check():
    num_intersections = 0
    for i in range(len(polygon_vertices)):
        p1 = polygon_vertices[i]
        p2 = polygon_vertices[(i + 1) % len(polygon_vertices)]

        if (p1[1] > mouse_pos[1]) != (p2[1] > mouse_pos[1]) and \
                mouse_pos[0] < (p2[0] - p1[0]) * (mouse_pos[1] - p1[1]) / (p2[1] - p1[1]) + p1[0]:
            num_intersections += 1

    if num_intersections % 2 == 1:
        return True
    else:
        return False

# Hlavní smyčka programu
running = True
while running:
    screen.fill(WHITE)

    # Nakreslení polygonu
    pygame.draw.polygon(screen, BLACK, polygon_vertices)

    # Získání pozice myši
    mouse_pos = pygame.mouse.get_pos()

    # Kontrola zda je myš uvnitř polygonu
    if pygame.mouse.get_pressed()[0]:
        if barrier_check():
            print("Myš je uvnitř polygonu!")
        else:
            print("Myš není uvnitř polygonu!")

    # Události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()