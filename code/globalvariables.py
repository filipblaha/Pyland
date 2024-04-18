from pygame.math import Vector2 as vector
import pygame
import sys
import os


class GlobalVariables:
    def __init__(self):
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.FPS = 40
        self.TILE_SIZE = 16
        self.MINIGAME_SCENE = 0

        # font setup
        self.FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'graphics', 'font', 'Cabal-w5j3.ttf')
        self.FONT_SIZE = 18

        # states in game
        self.GAME_STAGE = {
            'OVER_WORLD': False,
            'IDE': False
        }

    def change_game_stage(self, selected_stage):
        for stage in self.GAME_STAGE:
            if stage == selected_stage:
                self.GAME_STAGE[stage] = True
            else:
                self.GAME_STAGE[stage] = False
