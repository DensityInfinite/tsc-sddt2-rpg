import pygame, os.path as path


class Screen:
    def __init__(self) -> None:
        self.title = "DensityInfinite & Peilin - Tile-Based RPG"
        self.screen_size = (800, 600)
        self.vsync = 1
        self.fps = 60


class Player:
    def __init__(self) -> None:
        self.speed = 6
        self.initial_position = (0, 0)
        self.colour = (255, 0, 0)
        self.max_heath = 100
        self.base_damage = 10
        self.base_defence = 0.2
        self.attack_consistency = 0.8
        self.escape_chance = 0.3


class Enemy:
    def __init__(self) -> None:
        self.chase_time = 5
        self.time_increment = 2
        self.time_increment_dis = 50
        self.default_health = 50
        self.default_defence = 0.1
        self.attack_consistency = 0.6


class Map:
    def __init__(self) -> None:
        self.tile_size = 50
        self.grids_master_path = path.join(
            path.dirname(__file__), "resources/map/grids/grids_master.json"
        )
        self.textures_path = path.join(path.dirname(__file__), "resources/textures")


class GUI:
    def __init__(self) -> None:
        self.rounded_corner_radius = 2
        self.inner_corner_decrement = 1


class Fonts:
    def __init__(self) -> None:
        self.button_font_name = "cochin"
        self.button_font = pygame.Font(
            pygame.font.match_font(self.button_font_name, bold=True), 19
        )


class Colours:
    def __init__(self) -> None:
        self.white = pygame.Color(255, 255, 255)
        self.blue = pygame.Color(70, 223, 253)
        self.red = pygame.Color(136, 8, 8)
        self.grey = pygame.Color(50, 50, 50)
        self.black = pygame.Color(0, 0, 0)

        self.background_colour = self.black
        self.button_text_colour = self.white


class Cursor:
    def __init__(self) -> None:
        self.cursor_sprite_size = 1
        self.cursor_sprite_as_cursor = False
        self.cursor_offset = (-1, -1)


class Dev:
    def __init__(self) -> None:
        self.button_pressed_event = pygame.USEREVENT + 1
