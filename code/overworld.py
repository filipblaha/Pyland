from overworldsprites import *
from player import *
from dialogwindow import *
from CameraGroup import *


class OverWorld:
    def __init__(self, tmx_map, data):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.data = data

        # zones
        self.fisherman_zone = []
        self.wizard_zone = []
        self.knight_zone = []
        self.house_entry_zone = []

        # dialog windows
        self.fisherman_dialog_window = None
        self.wizard_dialog_window = None
        self.knight_dialog_window = None
        self.house_entry_dialog_window = None
        self.hint_dialog_window = None

        # sprite setup
        self.camera_group = CameraGroup()
        self.player = None
        self.sprites = {}
        self.barrier = None
        self.setup(tmx_map)

        # mouse
        pygame.mouse.set_visible(False)
        self.mouse = pygame.Surface((10, 10))
        self.mouse.fill((0, 0, 0))
        self.mouse_mask = pygame.mask.from_surface(self.mouse)

        # progress
        self.task_done = {'Fisherman': False,
                          'Knight': False,
                          'Wizard': False,
                          'Ghost': False}

    def setup(self, tmx_map):
        # tmx
        for layer in ['Floor', 'Pavement', 'Vegetation', 'Cliffs3', 'Cliffs2', 'Cliffs1', 'FloorDarkShadow',
                      'FloorBrightShadow']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                OverworldSprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.camera_group, 'Tile')

        for obj in tmx_map.get_layer_by_name('Objects'):
            pos = obj.x, obj.y
            if obj.name == 'Player':
                self.player = Player(pos, self.camera_group, tmx_map, 'Player')
            else:
                self.sprites[obj.name] = OverworldSprite(pos, obj.image, self.camera_group, obj.name)

        for obj in tmx_map.get_layer_by_name('Zones'):
            pos = obj.x, obj.y
            if obj.name == 'wizard_zone':
                self.wizard_zone = pygame.Rect(pos[0], pos[1], obj.width, obj.height)
            if obj.name == 'knight_zone':
                self.knight_zone = pygame.Rect(pos[0], pos[1], obj.width, obj.height)
            if obj.name == 'fisherman_zone':
                self.fisherman_zone = pygame.Rect(pos[0], pos[1], obj.width, obj.height)
            if obj.name == 'house_entry_zone':
                self.house_entry_zone = pygame.Rect(pos[0], pos[1], obj.width, obj.height)

        # dialog windows

        self.fisherman_dialog_window = DialogWindow('', 34, self.sprites['fisherman'].rect.center, 450, 150, self.camera_group)
        self.wizard_dialog_window = DialogWindow('', 34, self.sprites['wizard'].rect.center, 450, 150, self.camera_group)
        self.knight_dialog_window = DialogWindow('', 34, self.sprites['knight'].rect.center, 450, 150, self.camera_group)
        self.house_entry_dialog_window = DialogWindow('', 34, (360, 640), 250, 150, self.camera_group)
        self.hint_dialog_window = DialogWindow('Press E to interact.', 34, (1650, 100), 450, 150, self.camera_group, True, ['Press', 'E'])

    def logic(self, dt):
        # zones
        if self.task_done['Fisherman']:
            self.fisherman_dialog_window.active = self.player.zone_collision_check(self.fisherman_zone)
        else:
            self.fisherman_dialog_window.active = True
        self.hint_dialog_window.active = self.player.zone_collision_check(self.fisherman_zone)
        self.wizard_dialog_window.active = self.player.zone_collision_check(self.wizard_zone)
        self.knight_dialog_window.active = self.player.zone_collision_check(self.knight_zone)
        self.house_entry_dialog_window.active = self.player.zone_collision_check(self.house_entry_zone)

        # update
        self.camera_group.update(dt)
        self.fisherman_dialog_window.update(self.player.rect.center)
        self.wizard_dialog_window.update(self.player.rect.center)
        self.knight_dialog_window.update(self.player.rect.center)
        self.house_entry_dialog_window.update(self.player.rect.center)

        # dialog windows
        self.fisherman_dialog_window.change_text('Hey You! I need to tell you something!')

        if self.task_done['Fisherman']:
            self.knight_dialog_window.change_text('Yes')

    def render(self, dt):
        # draw
        self.camera_group.custom_draw(self.player)
        self.fisherman_dialog_window.display()
        self.hint_dialog_window.display()
        self.wizard_dialog_window.display()
        self.knight_dialog_window.display()
        self.house_entry_dialog_window.display()
