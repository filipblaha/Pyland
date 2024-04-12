from pygame.math import Vector2 as vector
import pygame
import os
from enum import Enum

WIDTH = 1920
HEIGHT = 1080
FPS = 40
TILE_SIZE = 16

# font setup
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphic', 'font', 'Cabal-w5j3.ttf')
FONT_SIZE = 18


# states in game
class GameState(Enum):
    MENU = 0
    OVER_WORLD = 1
    IDE = 2



