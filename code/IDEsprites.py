import pygame.display

from globalvariables import *


def create_sprite(image_filename, pos):
    image_path = os.path.join('../graphics/ide/', image_filename)
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load(image_path).convert_alpha()
    sprite.rect = sprite.image.get_rect(topleft=pos)
    return sprite


class IDESprites(pygame.sprite.Group):
    def __init__(self, display_surface, sprite_group):
        # camera setup
        super().__init__()
        self.display_surface = display_surface
        self.sprite_group = sprite_group

        # making sprites
        self.forest_sprite = create_sprite('forest0.png', (0, 0))
        self.wizard_sprite = create_sprite('wizard_closeup.png', (1300, 200))
        self.wizard_hat_sprite = create_sprite('hat.png', (1280, 570))
        self.code_paper_sprite = create_sprite('code_paper.png', (0, 10))
        self.check_button_sprite = create_sprite('check_button.png', (850, 880))

    def set_wizard_winning_scene(self):
        self.sprite_group.empty()

        self.sprite_group.add(self.forest_sprite)
        self.sprite_group.add(self.code_paper_sprite)
        self.sprite_group.add(self.check_button_sprite)
        self.sprite_group.add(self.wizard_hat_sprite)

    def set_wizard(self):
        self.sprite_group.empty()

        self.sprite_group.add(self.forest_sprite)
        self.sprite_group.add(self.code_paper_sprite)
        self.sprite_group.add(self.check_button_sprite)
        self.sprite_group.add(self.wizard_sprite)

    def blink_button(self):
        enlarged_image_surf = pygame.transform.scale(self.check_button_sprite.image, (450, 180))
        self.display_surface.blit(enlarged_image_surf, (625, 660))
        pygame.display.flip()
        pygame.time.delay(200)  # waiting 200 ms
