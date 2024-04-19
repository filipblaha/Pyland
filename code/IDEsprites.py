from globalvariables import *


def create_sprite(image_filename, pos):
    image_path = os.path.join('../graphics/ide/', image_filename)
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load(image_path).convert_alpha()
    sprite.rect = sprite.image.get_rect(topleft=pos)
    return sprite


class IDESprites(pygame.sprite.Group):
    def __init__(self, glob, display_surface, sprite_group):
        # camera setup
        super().__init__()
        self.display_surface = display_surface
        self.sprite_group = sprite_group
        self.globals = glob

        self.blink_button_active = False

        # making sprites
        self.lake_sprite = create_sprite('lake.png', (0, 0))
        self.forest_sprite = create_sprite('forest.png', (0, 0))
        self.house_sprite = create_sprite('house.png', (0, 0))
        self.code_paper_sprite = create_sprite('code_paper.png', (0, 10))
        self.check_button_sprite = create_sprite('check_button.png', (850, 880))
        self.cursor_sprite = create_sprite('cursor.png', (0, 0))
        self.fisherman_sprite = create_sprite('fisherman_closeup.png', (1000, 200))
        self.wizard_sprite = create_sprite('wizard_closeup.png', (1300, 200))
        self.wizard_hat_sprite = create_sprite('hat.png', (1280, 570))
        self.knight_sprite = create_sprite('knight_closeup.png', (1300, 250))
        self.ghost_sprite = create_sprite('ghost_closeup.png', (1300, 250))

    def set_scene(self):
        self.sprite_group.empty()

        if self.globals.MINIGAME_SCENE == 0:
            self.sprite_group.add(self.lake_sprite)
            self.sprite_group.add(self.code_paper_sprite)
            self.sprite_group.add(self.check_button_sprite)
            self.sprite_group.add(self.fisherman_sprite)

        elif self.globals.MINIGAME_SCENE == 1:
            self.sprite_group.add(self.forest_sprite)
            self.sprite_group.add(self.code_paper_sprite)
            self.sprite_group.add(self.check_button_sprite)
            self.sprite_group.add(self.knight_sprite)

        elif self.globals.MINIGAME_SCENE == 2:
            self.sprite_group.add(self.forest_sprite)
            self.sprite_group.add(self.code_paper_sprite)
            self.sprite_group.add(self.check_button_sprite)
            self.sprite_group.add(self.wizard_sprite)

        elif self.globals.MINIGAME_SCENE == 3:
            self.sprite_group.add(self.forest_sprite)
            self.sprite_group.add(self.code_paper_sprite)
            self.sprite_group.add(self.check_button_sprite)
            self.sprite_group.add(self.ghost_sprite)

    def blink_button(self):
        if self.blink_button_active:
            enlarged_image_size = pygame.Vector2(self.check_button_sprite.image.get_size()) * 1.1
            enlarged_image_surf = pygame.transform.scale(self.check_button_sprite.image, enlarged_image_size)
            enlarged_image_rect = enlarged_image_surf.get_rect()
            enlarged_image_rect.center = self.check_button_sprite.rect.center
            self.display_surface.blit(enlarged_image_surf, enlarged_image_rect)
            pygame.display.flip()
            pygame.time.delay(250)  # waiting 200 ms

            self.blink_button_active = False
