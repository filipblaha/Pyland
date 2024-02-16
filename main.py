from overworld import *


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.SCALED)
        pygame.display.set_caption('Pyland')

        # objects
        self.over_world = OverWorld(self.screen)

        self.game_state = GameState.OVER_WORLD
        # self.game_state = GameState.IDE

        # Timing
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

    def input(self):
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            # user pressing ESC or X (CLOSE APP) to quit
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return ["QUIT", "QUIT"]
            # user pressing button to check
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return ["BUTTON_PRESSED", "BUTTON_PRESSED"]
            # user pressing keys
            elif event.type == pygame.KEYDOWN:
                return [keys, event.key]
        return [keys, None]

    def logic(self, action):
        if self.game_state == GameState.OVER_WORLD:
            self.over_world.logic(action[0])
        # elif self.game_state == GameState.IDE:
        #     self.ide.logic(action)

    def render(self):
        if self.game_state == GameState.OVER_WORLD:
            self.over_world.render()
        # elif self.game_state == GameState.IDE:
        #     self.ide.render()

        pygame.display.update()

    def game_loop(self):
        while True:
            action = self.input()
            self.logic(action)
            self.render()

            game.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.game_loop()




