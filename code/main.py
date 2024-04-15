import sys
from pytmx.util_pygame import load_pygame
from save_load_data import *
from overworld import *
from IDE import *


class Game:
    def __init__(self):
        pygame.init()

        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED).convert_alpha()
        pygame.display.set_caption('Pyland')

        # objects
        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'map.tmx'))}
        self.data = Data()

        self.over_world = OverWorld(self.tmx_maps[0], self.data)
        self.ide = IDE(self.data)

        self.game_stage = GameState.OVER_WORLD
        # self.game_stage = GameState.IDE

        # Timing
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

    def logic(self, dt):
        if self.game_stage == GameState.OVER_WORLD:
            self.over_world.logic(dt)
        elif self.game_stage == GameState.IDE:
            self.ide.logic(dt)

    def render(self, dt):
        if self.game_stage == GameState.OVER_WORLD:
            self.over_world.render(dt)
        elif self.game_stage == GameState.IDE:
            self.ide.render()

        pygame.display.update()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000

            # Turning the game off
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            self.logic(dt)
            self.render(dt)


if __name__ == "__main__":
    game = Game()
    game.run()




