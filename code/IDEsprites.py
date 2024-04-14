from globalvariables import *


class IDESprites(pygame.sprite.Group):
    def __init__(self, display_surface):
        # camera setup
        super().__init__()
        self.display_surface = display_surface

        # # making sprites for mystery man
        # self.enemy0_surf = pygame.image.load('graphic/minigame/mystery_man_closeup.png').convert_alpha()
        #
        # self.enemy0_rect = self.enemy0_surf.get_rect(topleft=(1080, 200))

        # making sprites for wizard
        self.forest0_surf = pygame.image.load('../graphics/ide/forest0.png').convert_alpha()
        self.enemy1_surf = pygame.image.load('../graphics/ide/wizard_closeup.png').convert_alpha()
        self.enemy1_dead_surf = pygame.image.load('../graphics/ide/hat.png').convert_alpha()

        self.forest0_rect = self.forest0_surf.get_rect(topleft=(0, 0))
        self.enemy1_rect = self.enemy1_surf.get_rect(topleft=(1080, 200))
        self.enemy1_dead_rect = self.enemy1_surf.get_rect(topleft=(1280, 570))

        # making sprites
        self.code_paper_surf = pygame.image.load('../graphics/ide/code_paper.png').convert_alpha()
        self.check_button_surf = pygame.image.load('../graphics/ide/check_button.png').convert_alpha()

        self.code_paper_rect = self.code_paper_surf.get_rect(topleft=(0, 0))
        self.check_button_rect = self.check_button_surf.get_rect(center=(850, 750))

    # def update_mystery_man(self):
    #     self.display_surface.blit(self.forest0_surf, self.forest0_rect.topleft)
    #     self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
    #     self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)
    #     self.display_surface.blit(self.enemy0_surf, self.enemy0_rect.topleft)

    def update_wizard_winning_scene(self):
        self.display_surface.blit(self.forest0_surf, self.forest0_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)
        self.display_surface.blit(self.enemy1_dead_surf, self.enemy1_dead_rect.topleft)

    def update_wizard(self):
        self.display_surface.blit(self.forest0_surf, self.forest0_rect.topleft)
        self.display_surface.blit(self.code_paper_surf, self.code_paper_rect.topleft)
        self.display_surface.blit(self.check_button_surf, self.check_button_rect.topleft)
        self.display_surface.blit(self.enemy1_surf, self.enemy1_rect.topleft)

    def blink_button(self):
        enlarged_image_surf = pygame.transform.scale(self.check_button_surf, (450, 180))
        self.display_surface.blit(enlarged_image_surf, (625, 660))
        pygame.display.flip()
        pygame.time.delay(200)  # waiting 200 ms
