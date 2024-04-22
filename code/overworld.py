from overworldsprites import *
from player import *
from CameraGroup import *
from dialogwindow import *
from globalvariables import *


class OverWorld:
    def __init__(self, glob, tmx_map, data):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.globals = glob

        # zones
        self.zones = []
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

    def setup(self, tmx_map):
        # tmx
        for layer in ['Floor', 'Pavement', 'Vegetation', 'Cliffs3', 'Cliffs2', 'Cliffs1', 'FloorDarkShadow',
                      'FloorBrightShadow']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                OverworldSprite((x * self.globals.TILE_SIZE, y * self.globals.TILE_SIZE), surf, self.camera_group,
                                'Tile')

        for obj in tmx_map.get_layer_by_name('Objects'):
            pos = obj.x, obj.y
            if obj.name == 'Player':
                self.player = Player(pos, self.camera_group, tmx_map, 'Player')
            else:
                self.sprites[obj.name] = OverworldSprite(pos, obj.image, self.camera_group, obj.name)

        for obj in tmx_map.get_layer_by_name('Zones'):
            pos = obj.x, obj.y
            if obj.name == 'fisherman_zone':
                self.fisherman_zone = pygame.Rect(pos[0], pos[1], obj.width, obj.height)
            if obj.name == 'knight_zone':
                self.knight_zone = pygame.Rect(pos[0], pos[1], obj.width, obj.height)
            if obj.name == 'wizard_zone':
                self.wizard_zone = pygame.Rect(pos[0], pos[1], obj.width, obj.height)
            if obj.name == 'house_entry_zone':
                self.house_entry_zone = pygame.Rect(pos[0], pos[1], obj.width, obj.height)

        self.zones.append(self.fisherman_zone)
        self.zones.append(self.knight_zone)
        self.zones.append(self.wizard_zone)
        self.zones.append(self.house_entry_zone)

        # dialog windows
        self.fisherman_dialog_window = DialogWindow('', 34, self.sprites['fisherman'].rect.center, 450, 150,
                                                    self.camera_group)
        self.wizard_dialog_window = DialogWindow('', 34, self.sprites['wizard'].rect.center, 450, 150,
                                                 self.camera_group)
        self.knight_dialog_window = DialogWindow('', 34, self.sprites['knight'].rect.center, 450, 150,
                                                 self.camera_group)
        self.house_entry_dialog_window = DialogWindow('', 34, (360, 620), 250, 150, self.camera_group)
        self.hint_dialog_window = DialogWindow('Press E to interact.', 34, (1650, 100), 450, 150, self.camera_group,
                                               True, ['Press', 'E'])

    def logic(self, dt, event):
        if event:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        self.dialog_windows_active()
        self.dialog_windows_pos_update(dt)
        self.dialog_windows_select_text()

        if self.start_dialog(event):
            self.globals.change_game_stage('IDE')

    def dialog_windows_pos_update(self, dt):
        self.camera_group.update(dt)
        self.fisherman_dialog_window.update(self.player.rect.center)
        self.wizard_dialog_window.update(self.player.rect.center)
        self.knight_dialog_window.update(self.player.rect.center)
        self.house_entry_dialog_window.update(self.player.rect.center)

    def dialog_windows_active(self):
        for zone in self.zones:
            if self.player.zone_collision_check(zone):
                self.hint_dialog_window.active = True
                break
            else:
                self.hint_dialog_window.active = False

        if self.globals.MINIGAME_SCENE == 0:
            self.fisherman_dialog_window.active = True
        else:
            self.fisherman_dialog_window.active = self.player.zone_collision_check(self.fisherman_zone)
        self.wizard_dialog_window.active = self.player.zone_collision_check(self.wizard_zone)
        self.knight_dialog_window.active = self.player.zone_collision_check(self.knight_zone)
        self.house_entry_dialog_window.active = self.player.zone_collision_check(self.house_entry_zone)

    def dialog_windows_select_text(self):
        if self.globals.MINIGAME_SCENE == 0:
            self.fisherman_dialog_window.change_text('Hey you! You must help us!', 34, ['Hey', 'you!'])
            self.knight_dialog_window.change_text('First, talk with the fisherman.')
            self.wizard_dialog_window.change_text('Get lost you nameless entity.')
            self.house_entry_dialog_window.change_text('Locked')
        elif self.globals.MINIGAME_SCENE == 1:
            self.fisherman_dialog_window.change_text(self.globals.PLAYER_NAME + ' go talk to sir Arnold.')
            self.knight_dialog_window.change_text('Quickly, before he escapes!')
            self.wizard_dialog_window.change_text('Do you even know what are cycles, ' + self.globals.PLAYER_NAME + '?')
            self.house_entry_dialog_window.change_text('Locked')
        elif self.globals.MINIGAME_SCENE == 2:
            self.fisherman_dialog_window.change_text('What are we gonna do?')
            self.knight_dialog_window.change_text('Quickly, before he escapes!')
            self.wizard_dialog_window.change_text('STOP RIGHT THERE!')
            self.house_entry_dialog_window.change_text('Locked')
        else:
            self.fisherman_dialog_window.change_text(self.globals.PLAYER_NAME + ' is it over or will it return?.')
            self.knight_dialog_window.change_text('I bow before you ' + self.globals.PLAYER_NAME + '.')
            self.wizard_dialog_window.change_text('He escaped, but he shall return.')
            self.house_entry_dialog_window.change_text('Locked')

    def start_dialog(self, event):
        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if self.globals.MINIGAME_SCENE == 0 and self.player.zone_collision_check(self.fisherman_zone):
                    return True
                elif self.globals.MINIGAME_SCENE == 1 and self.player.zone_collision_check(self.knight_zone):
                    return True
                elif self.globals.MINIGAME_SCENE == 2 and self.player.zone_collision_check(self.wizard_zone):
                    return True

    def render(self, dt):
        # draw
        self.camera_group.custom_draw(self.player)
        self.fisherman_dialog_window.display()
        self.hint_dialog_window.display()
        self.wizard_dialog_window.display()
        self.knight_dialog_window.display()
        self.house_entry_dialog_window.display()
