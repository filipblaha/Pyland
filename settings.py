import os
from enum import Enum

# global variables
WIDTH = 1920
HEIGHT = 1080
FPS = 60
TILE_SIZE = 32


# states in game
class GameState(Enum):
    MENU = 0
    OVER_WORLD = 1
    MINIGAME = 2

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200

# path to script
base_path = os.path.dirname(os.path.abspath(__file__))
# name of font
font_filename = 'Cabal-w5j3.ttf'
# full path to file
UI_FONT = os.path.join(base_path, 'graphic', 'font', font_filename)

UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
