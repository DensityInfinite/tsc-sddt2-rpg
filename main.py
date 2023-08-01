import pygame, json
from sys import exit

import resources.utils as utils
from resources.game_settings import GameSettings

from resources.player_movement import Player

player = Player(100, 100, 800, 600, 32, 5)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.json_utils = utils.JsonUtils()
        self.settings = GameSettings()
        self.player = Player(
            100, 100, self.settings.screen_size[0], self.settings.screen_size[1], 32, 5
        )

        # Screen
        self.screen = pygame.display.set_mode(
            self.settings.screen_size,
            pygame.HWSURFACE | pygame.SRCALPHA,
            self.settings.vsync,
        )
        pygame.display.set_caption(self.settings.title)

    def run_game(self) -> None:
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.player.set_moving_right(True)
                    elif event.key == pygame.K_UP:
                        self.player.set_moving_up(True)
                    elif event.key == pygame.K_DOWN:
                        self.player.set_moving_down(True)
                    elif event.key == pygame.K_LEFT:
                        self.player.set_moving_left(True)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player.set_moving_right(False)
                    elif event.key == pygame.K_LEFT:
                        self.player.set_moving_left(False)
                    elif event.key == pygame.K_UP:
                        self.player.set_moving_up(False)
                    elif event.key == pygame.K_DOWN:
                        self.player.set_moving_down(False)

            self.player.update()
            self.screen.fill(self.settings.background_colour)
            self.screen.blit(self.player.image, self.player.rect)

            pygame.display.update()
            self.clock.tick(self.settings.fps)


if __name__ == "__main__":
    rpg = Game()
    rpg.run_game()
