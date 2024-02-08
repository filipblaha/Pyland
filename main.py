import pygame
import sys

from settings import *
from text import Text
from level import Level
from minigame import *
import test_code


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.SCALED)
        pygame.display.set_caption('Pyland')
        self.can_interact = False

        self.text = Text("Arial", 27, self.screen)
        self.level = Level(self.can_interact)
        self.minigame = Minigame(self.text, self.screen)
        self.minigame_sprites = MinigameSprites()
        # self.game_state = GameState.OVER_WORLD
        self.game_state = GameState.MINIGAME

        # Timing
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

    def player_input(self):
        for event in pygame.event.get():
            # user pressing ESC or X (CLOSE APP) to quit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "QUIT"
            # user pressing button to check
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return "BUTTON_PRESSED"
            # user pressing keys
            elif event.type == pygame.KEYDOWN:

                # pressed LEFT KEY
                if event.key == pygame.K_LEFT:
                    return "LEFT"
                # pressed RIGHT KEY
                elif event.key == pygame.K_RIGHT:
                    return "RIGHT"
                # pressed ENTER
                elif event.key == pygame.K_RETURN:
                    return "ENTER"
                # pressed BACKSPACE
                elif event.key == pygame.K_BACKSPACE:
                    if self.text.user_text:
                        return "BACKSPACE"
                # pressed SPACE
                elif event.key == pygame.K_SPACE:
                    return "SPACE"
                # pressed TAB
                elif event.key == pygame.K_TAB:
                    return "TAB"
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
                self.game_state = GameState.OVER_WORLD
                return
            # pressed LEFT KEY
            elif action_from_input == "LEFT":
                if self.text.cursor_index > 0:
                    self.text.cursor_index -= 1
            # pressed RIGHT KEY
            elif action_from_input == "RIGHT":
                if self.text.cursor_index < len(self.text.user_text):
                    self.text.cursor_index += 1
            elif action_from_input == "ENTER":
                self.text.user_text.append("")
                self.text.cursor_row += 1
            # pressed BACKSPACE
            elif action_from_input == "BACKSPACE":
                if self.text.user_text and len(self.text.user_text[0]) > 0:
                    # if self.text.user_text[-1] == '':
                    #     self.text.user_text.pop()
                    #     self.text.cursor_row -= 1
                    # else:
                    #     self.text.user_text[-1] = self.text.user_text[-1][:-1]
                    #     self.text.cursor_index -= 1
                    if self.text.cursor_index > 0:
                        self.text.user_text[0] = (self.text.user_text[0][:self.text.cursor_index - 1]
                                                  + self.text.user_text[0][self.text.cursor_index:])
                        self.text.cursor_index -= 1
            # pressed SPACE
            elif action_from_input == "SPACE":
                self.text.user_text[-1] += " "
                self.text.cursor_index += 1
            elif action_from_input == "TAB":
                self.text.user_text[-1] += "    "
                self.text.cursor_index += 4
            elif action_from_input == "BUTTON_PRESSED":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game.minigame_sprites.check_button_rect.collidepoint(mouse_x, mouse_y):
                    self.minigame_sprites.blink_button()
                    error = test_code.check_code(self.text.user_text)
                    if error is None:
                        print("bum")
                    else:
                        test_code.log_errors(self.text.user_text, error)

            elif action_from_input == "PASS":
                pass
            else:
                self.text.user_text[0] = (self.text.user_text[0][:self.text.cursor_index] + action_from_input.unicode +
                                          self.text.user_text[0][self.text.cursor_index:])
                self.text.cursor_index += 1


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

