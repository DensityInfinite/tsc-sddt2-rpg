import pygame


class GameSettings:
    def __init__(self) -> None:
        # Screen
        self.title = "DensityInfinite & Peilin - Tile-Based RPG"
        self.screen_size = (800, 600)
        self.vsync = 1
        self.fps = 60

        # Colours
        self.background_colour = pygame.Color(255, 255, 255)


class PlayerSettings:
    def __init__(self) -> None:
        # Player
        self.speed = 6
        self.initial_position = (0, 0)
        self.colour = (255, 0, 0)


class GridSettings:
    def __init__(self) -> None:
        # Grid
        self.colour = pygame.Color(0, 0, 0)


class TileSettings:
    def __init__(self) -> None:
        # Tile
        self.size = 32
