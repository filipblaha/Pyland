import pygame
import sys

from settings import *
from text import Text
from level import Level
from minigame import Minigame


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.SCALED)
        pygame.display.set_caption('Pyland')
        self.clock = pygame.time.Clock()
        self.can_interact = False

        self.text = Text("Arial", 27)
        self.level = Level(self.can_interact)
        self.minigame = Minigame(self.text, self.screen)
        self.game_state = GameState.OVER_WORLD
        # self.game_state = GameState.MINIGAME

    def player_input(self):
        for event in pygame.event.get():
            # user pressing ESC or X (CLOSE APP) to quit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "QUIT"
            # user pressing button to check
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return "BUTTON_PRESSED"
            # the code is right
            elif event.type == pygame.USEREVENT:
                return "ANIMATION"
            # user pressing keys
            elif event.type == pygame.KEYDOWN:
                # pressed ENTER
                if event.key == pygame.K_RETURN:
                    return "ENTER"
                # pressed BACKSPACE
                elif event.key == pygame.K_BACKSPACE:
                    if self.text.user_text:
                        return "BACKSPACE"
                # pressed SPACE
                elif event.key == pygame.K_SPACE:
                    return "SPACE"
                # pressed other keys
                else:
                    return event
        return "PASS"

    def logic(self, action_from_input):

        # OVER_WORLD
        if self.game_state == GameState.OVER_WORLD:
            self.can_interact = self.level.interact()
            if action_from_input == "QUIT":
                pygame.quit()
                sys.exit()
            # pressed SPACE
            elif action_from_input == "SPACE":
                self.level.toggle_menu()
            elif action_from_input == "PASS":
                pass
                # pressed e for interaction
            elif self.can_interact and action_from_input.key == pygame.K_e:
                self.game_state = GameState.MINIGAME
                return

        # MINIGAME
        if self.game_state == GameState.MINIGAME:
            if action_from_input == "QUIT":
                pygame.quit()
                sys.exit()
            if action_from_input == "ENTER":
                self.text.user_text.append("")
            # pressed BACKSPACE
            elif action_from_input == "BACKSPACE":
                if self.text.user_text and len(self.text.user_text[0]) > 0:
                    if self.text.user_text[-1] == '':
                        self.text.user_text.pop()
                    self.text.user_text[-1] = self.text.user_text[-1][:-1]
            # pressed SPACE
            elif action_from_input == "SPACE":
                self.level.toggle_menu()
            elif action_from_input == "BUTTON_PRESSED":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game.minigame.button.rect.collidepoint(mouse_x, mouse_y):
                    pygame.time.set_timer(pygame.USEREVENT, 500)
            elif action_from_input == "ANIMATION":
                game.minigame.player.change_animation()
            elif action_from_input == "PASS":
                pass
            else:
                self.text.user_text[-1] += action_from_input.unicode


game = Game()

step = 0
while True:
    step = step + 1
    action = game.player_input()
    game.logic(action)

    if game.game_state == GameState.OVER_WORLD:
        game.level.run()
    elif game.game_state == GameState.MINIGAME:
        game.minigame.run()

    pygame.display.update()
    game.clock.tick(FPS)

