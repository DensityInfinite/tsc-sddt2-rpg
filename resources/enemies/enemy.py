import pygame, resources.game_settings as settings


class Enemy(pygame.sprite.Sprite):
    def __init__(self, in_game_pos: tuple[int, int], movement) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)

        self.raw_pos = (in_game_pos[0] * 100 - 75, in_game_pos[1] * 100 - 75)

    def update(self):
        pass