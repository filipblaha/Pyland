import pygame
import sys

import level
from settings import *
from level import Level
from text import Text
from minigame import Minigame
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.SCALED)
        # self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Pyland')
        self.clock = pygame.time.Clock()

        self.can_interact = False
        self.level = Level(self.can_interact)
        self.minigame = Minigame()
        self.text = Text("Arial", 36)
        self.game_state = GameState.OVER_WORLD
        # self.game_state = GameState.MINIGAME

    def player_input(self):
        for event in pygame.event.get():
            # user pressing ESC or X (CLOSE APP) to quit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
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
                    # interaction
                    if event.key == pygame.K_e and self.can_interact and self.game_state == GameState.OVER_WORLD:
                        self.game_state = GameState.MINIGAME
                    if not self.text.user_text or event.key != pygame.K_KP_ENTER:
                        self.text.user_text[-1] += event.unicode
        return pygame.key.get_pressed()

    def logic(self, action_from_input):

        # OVER_WORLD
        if self.game_state == GameState.OVER_WORLD:
            self.can_interact = self.level.interact()
            if not action:
                pygame.quit()
                sys.exit()
            # pressed SPACE
            elif action == "SPACE":
                self.level.toggle_menu()

        # MINIGAME
        if self.game_state == GameState.MINIGAME:
            if not action:
                pygame.quit()
                sys.exit()
            if action == "ENTER":
                self.text.user_text.append("")
            # pressed BACKSPACE
            elif action == "BACKSPACE":
                if self.text.user_text:
                    self.text.user_text[-1] = self.text.user_text[-1][:-1]
            # pressed SPACE
            elif action == "SPACE":
                self.level.toggle_menu()
            elif action == "BUTTON_PRESSED":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game.minigame.button.rect.collidepoint(mouse_x, mouse_y):
                    pygame.time.set_timer(pygame.USEREVENT, 500)
            elif action == "ANIMATION":
                game.minigame.player.change_animation()

game = Game()

while True:
    action = game.player_input()
    game.logic(action)

    if game.game_state == GameState.OVER_WORLD:
        game.level.run()
    elif game.game_state == GameState.MINIGAME:
        game.minigame.run()

    pygame.display.update()
    game.clock.tick(FPS)

