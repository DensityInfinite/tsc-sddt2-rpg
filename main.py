import pygame, pygame_gui as pygui, json
from sys import exit

import resources.utils as utils
from resources.game_settings import GameSettings


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.json_utils = utils.JsonUtils()
        self.settings = GameSettings()

        # Screen
        self.screen = pygame.display.set_mode(
            self.settings.screen_size,
            pygame.HWSURFACE | pygame.SRCALPHA,
            self.settings.vsync,
        )
        pygame.display.set_caption(self.settings.title)
        self.manager = pygui.UIManager(self.settings.screen_size)

    def run_game(self) -> None:
        while 1:
            time_delta = self.clock.tick(self.settings.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.screen.fill(self.settings.background_colour)
            self.manager.draw_ui(self.screen)

            pygame.display.update()


if __name__ == "__main__":
    rpg = Game()
    rpg.run_game()
