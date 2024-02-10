import pygame
import sys

from settings import *
from text import Text
from ui import UI
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
        self.ui = UI()
        self.level = Level(self.can_interact, self.ui)
        self.minigame = Minigame(self.screen, self.text, self.ui)
        self.minigame_sprites = MinigameSprites()
        self.game_state = GameState.OVER_WORLD
        # self.game_state = GameState.MINIGAME

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
                elif event.key == pygame.K_UP:
                    return "UP"
                elif event.key == pygame.K_DOWN:
                    return "DOWN"
                # pressed ENTER
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return "ENTER"
                # pressed BACKSPACE
                elif event.key == pygame.K_BACKSPACE:
                    if self.text.user_text:
                        return "BACKSPACE"
                elif event.key == pygame.K_DELETE:
                    if self.text.user_text:
                        return "DELETE"
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
                if self.level.player.rect.x <= 700:
                    self.minigame.minigame_type = 0
                    if self.minigame.cutscene_frame < 4:
                        self.minigame.cutscene_on = True
                    else:
                        self.minigame.cutscene_on = False
                else:
                    self.minigame.minigame_type = 1
                pygame.mouse.set_visible(True)
                return

        # MINIGAME
        if self.game_state == GameState.MINIGAME:
            # cutscene
            if self.minigame.cutscene_on:
                if not action_from_input == 'PASS':
                    self.minigame.skip_cutscene = True
                    self.minigame.cutscene_frame += 1
            elif action_from_input == "QUIT":
                self.game_state = GameState.OVER_WORLD
                pygame.mouse.set_visible(False)
                return
            # pressed LEFT KEY
            elif action_from_input == "LEFT":
                if self.text.cursor_index > 0:
                    self.text.cursor_index -= 1
                elif self.text.cursor_row > 0:
                    self.text.cursor_row -= 1
                    self.text.cursor_index = len(self.text.user_text[self.text.cursor_row])
            # pressed RIGHT KEY
            elif action_from_input == "RIGHT":
                if self.text.cursor_index < len(self.text.user_text[self.text.cursor_row]):
                    self.text.cursor_index += 1
                elif self.text.cursor_row < len(self.text.user_text) - 1:
                    self.text.cursor_row += 1
                    self.text.cursor_index = 0
            elif action_from_input == "UP":
                if self.text.cursor_row > 0:
                    self.text.cursor_row -= 1
                    self.text.cursor_index = min(self.text.cursor_index, len(self.text.user_text[self.text.cursor_row]))
            elif action_from_input == "DOWN":
                if self.text.cursor_row < len(self.text.user_text) - 1:
                    self.text.cursor_row += 1
                    self.text.cursor_index = min(self.text.cursor_index, len(self.text.user_text[self.text.cursor_row]))

            elif action_from_input == "ENTER":
                self.text.user_text.insert(self.text.cursor_row + 1, '')
                self.text.cursor_row += 1
                self.text.cursor_index = 0
            # pressed BACKSPACE
            elif action_from_input == "BACKSPACE":
                if self.text.cursor_index == 0 and self.text.cursor_row > 0:
                    self.text.cursor_row -= 1
                    self.text.cursor_index = len(self.text.user_text[self.text.cursor_row])
                    self.text.user_text[self.text.cursor_row] += self.text.user_text.pop(self.text.cursor_row + 1)

                elif self.text.cursor_index > 0:
                    self.text.user_text[self.text.cursor_row] = (self.text.user_text[self.text.cursor_row][:self.text.cursor_index - 1]
                         + self.text.user_text[self.text.cursor_row][self.text.cursor_index:])
                    self.text.cursor_index -= 1

            elif action_from_input == "DELETE":
                if self.text.cursor_index < len(self.text.user_text[self.text.cursor_row]):
                    self.text.user_text[self.text.cursor_row] = (self.text.user_text[self.text.cursor_row][:self.text.cursor_index]
                         + self.text.user_text[self.text.cursor_row][self.text.cursor_index + 1:])
                elif self.text.cursor_row < len(self.text.user_text) - 1:
                    self.text.user_text[self.text.cursor_row] = self.text.user_text.pop(self.text.cursor_row + 1)
                    # pressed SPACE
            elif action_from_input == "SPACE":
                self.text.user_text[self.text.cursor_row] = (self.text.user_text[self.text.cursor_row][
                                                             :self.text.cursor_index] + ' ' +
                                                             self.text.user_text[self.text.cursor_row][
                                                             self.text.cursor_index:])
                self.text.cursor_index += 1
                pass
            elif action_from_input == "TAB":
                self.text.user_text[self.text.cursor_row] = (self.text.user_text[self.text.cursor_row][
                                                             :self.text.cursor_index] + '    ' +
                                                             self.text.user_text[self.text.cursor_row][
                                                             self.text.cursor_index:])
                self.text.cursor_index += 4
            elif action_from_input == "BUTTON_PRESSED":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game.minigame_sprites.check_button_rect.collidepoint(mouse_x, mouse_y):
                    self.minigame_sprites.blink_button()

                    goal = self.minigame.goal()
                    code = self.text.preset_text + self.text.user_text
                    error = test_code.check_code(code, goal)

                    self.minigame.error_message = test_code.log_errors(code, error)
                    if not test_code.ordered_word(self.text.user_text, self.minigame.ordered_words):
                        self.minigame.error_message = ['You are not using ordered words:', self.minigame.ordered_words]
                    if test_code.banned_words(self.text.user_text, self.minigame.banned_words) and not self.minigame.banned_words == '':
                        self.minigame.error_message = ['You are using banned words:', self.minigame.banned_words]

                    if self.minigame.error_message:
                        self.minigame.log = True
                        if self.minigame.error_message == ['Well done!']:
                            self.minigame.correct_answer = True
                    else:
                        self.minigame.log = False

            elif action_from_input == "PASS":
                pass
            else:
                self.text.user_text[self.text.cursor_row] = (self.text.user_text[self.text.cursor_row][:self.text.cursor_index] + action_from_input.unicode +
                                                             self.text.user_text[self.text.cursor_row][self.text.cursor_index:])
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
