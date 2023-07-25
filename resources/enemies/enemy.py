import pygame, resources.game_settings as settings


class Enemy(pygame.sprite.Sprite):
    def __init__(self, in_game_pos: tuple[int, int], movement: tuple[int, int]) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        self.map_settings = settings.Map()

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

    def update(self):
        pass
