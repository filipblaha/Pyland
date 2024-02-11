import pygame
from enum import Enum

from overworld import *


class Game:
    def __init__(self):
        pygame.init()

        width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN, pygame.SCALED)
        pygame.display.set_caption('Pyland')

        # objects
        self.over_world = OverWorld(self.screen)

        self.game_state = GameState.OVER_WORLD
        # self.game_state = GameState.IDE

        # Timing
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

    def input(self):
        return True

    def logic(self, action):
        if self.game_state == GameState.OVER_WORLD:
            self.over_world.logic(action)
        # elif self.game_state == GameState.IDE:
        #     self.ide.logic(action)

    def render(self):
        if self.game_state == GameState.OVER_WORLD:
            self.over_world.render()
        # elif self.game_state == GameState.IDE:
        #     self.ide.render()

        pygame.display.flip()

    def game_loop(self):
        while True:
            action = self.input()
            self.logic(action)
            self.render()


if __name__ == "__main__":
    game = Game()
    game.game_loop()




