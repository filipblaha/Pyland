from tile import *
from sprites import *
from random import choice

from player import *
from support import *


class OverWorld:
    def __init__(self, screen):

        # get the display surface
        self.display_surface = screen
        self.game_paused = False

        # sprite setup
        self.visible_sprites = Sprites()
        self.obstacle_sprite = pygame.sprite.Group()
        self.create_map()

        # user interface
        self.player = Player((380, 600), [self.visible_sprites], self.obstacle_sprite)
        pygame.mouse.set_visible(False)

    def create_map(self):
        layout = {
            'boundary': import_csv_layout('map/zelda_FloorBlocks.csv'),
            'grass': import_csv_layout('map/zelda_Grass.csv'),
            'object': import_csv_layout('map/zelda_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('map/Grass'),
            'object': import_folder('map/Object')
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprite], 'invisible')

                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'grass', random_grass_image)

                        if style == 'object':
                            if int(col) == 222:
                                image_name = 'ListStrom.png'
                                image_path = os.path.join('map', 'Object', image_name)
                                surf = pygame.image.load(image_path).convert_alpha()
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'object', surf)

                            if int(col) == 26:
                                image_name = 'JehlStrom.png'
                                image_path = os.path.join('map', 'Object', image_name)
                                surf = pygame.image.load(image_path).convert_alpha()
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'object', surf)

                            if int(col) == -2147482840:
                                image_name = 'Ztrazce_cely.png'
                                image_path = os.path.join('map', 'Object', image_name)
                                surf = pygame.image.load(image_path).convert_alpha()
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'object', surf)

                            if int(col) == 500:
                                image_name = 'Mystery_man.png'
                                image_path = os.path.join('map', 'Object', image_name)
                                surf = pygame.image.load(image_path).convert_alpha()

                                Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'object', surf, 1)

                            if int(col) == 10000:
                                image_name = 'Wizard.png'
                                image_path = os.path.join('map', 'Object', image_name)
                                surf = pygame.image.load(image_path).convert_alpha()

                                Tile((x, y), [self.visible_sprites, self.obstacle_sprite], 'object', surf, 0)

    def logic(self, action):
        self.player.can_interact = False

    def render(self):
        # update and draw the game
        self.visible_sprites.draw_over_world(self.player)
        self.visible_sprites.update()

