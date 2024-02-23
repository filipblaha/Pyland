import sys
from pytmx import load_pygame

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
        self.visible_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame('data/tmx/map.tmx')
        Sprites.render_layers(self.tmx_data,  self.visible_sprites)
        Sprites.render_objects(self.tmx_data,  self.visible_sprites)

        # user interface
        self.hud = DialogWindow()
        pygame.mouse.set_visible(False)

    def logic(self, action_key):

        # Turning the game off
        if action_key == "QUIT":
            pygame.quit()
            sys.exit()


        # self.player.can_interact = False
        #
        # # Reacting to pressing/holding keys and setting direction of player
        # if action_key[pygame.K_UP] or action_key[pygame.K_w]:
        #     self.player.direction.y = -1
        # elif action_key[pygame.K_DOWN] or action_key[pygame.K_s]:
        #     self.player.direction.y = 1
        # else:
        #     self.player.direction.y = 0
        #
        # if action_key[pygame.K_RIGHT] or action_key[pygame.K_d]:
        #     self.player.direction.x = 1
        # elif action_key[pygame.K_LEFT] or action_key[pygame.K_a]:
        #     self.player.direction.x = -1
        # else:
        #     self.player.direction.x = 0
        #
        # # Logic behind moving the player - position, hit boxes and collisions
        # self.player.move()
        #
        # # Interaction with characters on map
        # if self.player.can_interact:
        #
        #     if self.player.rect.x < 700:
        #         self.hud.set_dialog_window('Press E to interact.', 20,
        #                                    400 - self.visible_sprites.offset.x, 250 - self.visible_sprites.offset.y, 200, 100)
        #     else:
        #         self.hud.set_dialog_window('Press E to interact.', 20,
        #                                    1450 - self.visible_sprites.offset.x, 550 - self.visible_sprites.offset.y, 200, 100)

    def render(self):
        # update and draw the game
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()



