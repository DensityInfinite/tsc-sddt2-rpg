import pygame
from random import randint
import resources.game_settings as settings


class Enemy(pygame.sprite.Sprite):
    def __init__(self, in_game_pos: tuple[int, int], movement: tuple[int, int]) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        self.map_settings = settings.Map()

        self.state = "alone"

        self.raw_pos = (
            in_game_pos[0] * self.map_settings.tile_size
            - self.map_settings.tile_size // 2,
            in_game_pos[1] * self.map_settings.tile_size
            - self.map_settings.tile_size // 2,
        )
        self.image = pygame.Surface(
            (self.map_settings.tile_size, self.map_settings.tile_size)
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.raw_pos

    def update(self, player_pos: tuple[int, int]):
        if self.state == "alone":
            self.state = self._reshuffle_state()

    def _reshuffle_state(self) -> str:
        new_state = randint(1, 3)
        match new_state:
            case 1:
                return "alone"
            case 2:
                return "moving"
            case 3:
                return "chasing"