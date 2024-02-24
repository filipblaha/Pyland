import pygame
from pytmx.util_pygame import load_pygame
from os.path import join
from overworld import *
from globalvariables import *


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.SCALED)
        pygame.display.set_caption('Pyland')

        # objects
        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'map.tmx'))}
        self.over_world = OverWorld(self.screen, self.tmx_maps[0])

        self.game_stage = GameState.OVER_WORLD
        # self.game_state = GameState.IDE

        # Timing
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

    def logic(self):
        if self.game_stage == GameState.OVER_WORLD:
            self.over_world.logic()
        # elif self.game_state == GameState.IDE:
        #     self.ide.logic()

    def render(self, dt):
        if self.game_stage == GameState.OVER_WORLD:
            self.over_world.render(dt)
        # elif self.game_state == GameState.IDE:
        #     self.ide.render()

        pygame.display.update()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000

            # Turning the game off
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.logic()
            self.render(dt)

if __name__ == "__main__":
    game = Game()
    game.run()




