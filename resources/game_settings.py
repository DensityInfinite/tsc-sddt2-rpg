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
