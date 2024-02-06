import os

WIDTH   = 1920
HEIGHT  = 1080
FPS     = 60
TILESIZE= 16


# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200


# Adresář, ve kterém se nachází váš skript
base_path = os.path.dirname(os.path.abspath(__file__))
# Název souboru s fontem
font_filename = 'Cabal-w5j3.ttf'
# Celá cesta k souboru
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
