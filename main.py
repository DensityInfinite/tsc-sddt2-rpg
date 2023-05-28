import pygame, json
from sys import exit

import resources.utils as utils


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.json_utils = utils.JsonUtils()

        # Screen
        self.screen = pygame.display.set_mode(
            (800, 600), pygame.HWSURFACE | pygame.SRCALPHA, vsync=1
        )

    def run_game(self) -> None:
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill(pygame.Color(255, 255, 255))

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    rpg = Game()
    rpg.run_game()
