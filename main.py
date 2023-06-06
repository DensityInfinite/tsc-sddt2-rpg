import pygame, json
from sys import exit

import resources.utils as utils
import resources.game_settings as game_settings
import resources.gui.gui as gui


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.json_utils = utils.JsonUtils()
        self.screen_settings = game_settings.Screen()
        self.colours = game_settings.Colours()
        self.dev_tools = game_settings.Dev()
        self.gui = gui

        # Screen
        self.screen = pygame.display.set_mode(
            self.screen_settings.screen_size,
            pygame.HWSURFACE | pygame.SRCALPHA,
            self.screen_settings.vsync,
        )
        self.screen_width, self.screen_height = self.screen_settings.screen_size
        self.screen_centre_pos = (self.screen_width // 2, self.screen_height // 2)
        pygame.display.set_caption(self.screen_settings.title)

        # Cursor
        pygame.mouse.set_visible(not self.dev_tools.cursor_sprite_as_cursor)
        self.cursor = pygame.sprite.GroupSingle()
        self.cursor.add(gui.Cursor())

    def run_game(self) -> None:
        gui_group = pygame.sprite.RenderUpdates()
        hello_button = self.gui.Button(
            pygame.Rect(self.screen_centre_pos, (300, 50)),
            "Hello!",
            self.colours.background_colour,
        )
        gui_group.add(hello_button)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor.sprite.register_click(True)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.cursor.sprite.register_click(False)

            gui_group.update(self.cursor)
            self.cursor.update(pygame.mouse.get_pos())

            self.screen.fill(self.colours.background_colour)
            gui_group.draw(self.screen)

            pygame.display.update()


if __name__ == "__main__":
    rpg = Game()
    rpg.run_game()
