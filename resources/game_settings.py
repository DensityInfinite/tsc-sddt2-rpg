import pygame, os.path as path


class Screen:
    def __init__(self) -> None:
        self.title = "DensityInfinite & Peilin - Tile-Based RPG"
        self.screen_size = (800, 600)
        self.vsync = 1
        self.fps = 60


class GUI:
    def __init__(self) -> None:
        self.rounded_corner_radius = 5
        self.inner_corner_decrement = 2


class Fonts:
    def __init__(self) -> None:
        self.button_font_name = "optima bold"
        self.button_font = pygame.Font(
            pygame.font.match_font(self.button_font_name), 25
        )


class Colours:
    def __init__(self) -> None:
        self.white = pygame.Color(255, 255, 255)
        self.blue = pygame.Color(70, 223, 253)
        self.grey = pygame.Color(50, 50, 50)
        self.black = pygame.Color(0, 0, 0)

        self.background_colour = self.black
        self.button_text_colour = self.white


class Dev:
    def __init__(self) -> None:
        self.button_pressed_event = pygame.USEREVENT + 1
        self.cursor_sprite_size = 5
        self.cursor_sprite_as_cursor = False
