import sys
from random import choice


from tile import *
from sprites import *
from player import *
from dialogwindow import *
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
        self.hud = DialogWindow()
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

    def logic(self, action_key):
        self.player.can_interact = False

        # Turning the game off
        if action_key == "QUIT":
            pygame.quit()
            sys.exit()

        # Reacting to pressing/holding keys and setting direction of player
        if action_key[pygame.K_UP] or action_key[pygame.K_w]:
            self.player.direction.y = -1
        elif action_key[pygame.K_DOWN] or action_key[pygame.K_s]:
            self.player.direction.y = 1
        else:
            self.player.direction.y = 0

        if action_key[pygame.K_RIGHT] or action_key[pygame.K_d]:
            self.player.direction.x = 1
        elif action_key[pygame.K_LEFT] or action_key[pygame.K_a]:
            self.player.direction.x = -1
        else:
            self.player.direction.x = 0

        # Logic behind moving the player - position, hit boxes and collisions
        self.player.move()

        # Interaction with characters on map
        if self.player.can_interact:

            if self.player.rect.x < 700:
                self.hud.set_dialog_window('Press E to interact.', 20, 400 - self.visible_sprites.offset.x,
                                           250 - self.visible_sprites.offset.y, 200, 100)
            else:
                self.hud.set_dialog_window('Press E to interact.', 20, 1450 - self.visible_sprites.offset.x,
                                           550 - self.visible_sprites.offset.y, 200, 100)

    def render(self):
        # update and draw the game
        self.visible_sprites.draw_over_world(self.player)
        self.visible_sprites.update()
        if self.player.can_interact:
            self.hud.display_dialog_window()



