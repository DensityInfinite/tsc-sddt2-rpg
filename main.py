import pygame
from sys import exit


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()

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
