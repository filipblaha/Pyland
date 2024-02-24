from pytmx.util_pygame import load_pygame
from os.path import join
from overworld import *
from globalvariables import *


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((700, 200))
        pygame.display.set_caption('Pyland')

        # objects
        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'map.tmx'))}
        self.over_world = OverWorld(self.screen, self.tmx_maps[0])

    def run(self):
        while True:
            self.over_world.render(dt)
            pygame.display.update()



if __name__ == "__main__":
    game = Game()
    game.run()






