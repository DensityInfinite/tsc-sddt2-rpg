import pygame, json
from sys import exit

import resources.utils as utils
import resources.game_settings as game_settings
import resources.gui.gui as gui

from resources.player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.json_utils = utils.JsonUtils()
        self.screen_settings = game_settings.Screen()
        self.colours = game_settings.Colours()
        self.cursor_settings = game_settings.Cursor()
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
        pygame.mouse.set_visible(not self.cursor_settings.cursor_sprite_as_cursor)
        self.cursor = pygame.sprite.GroupSingle()
        self.cursor.add(gui.Cursor())

        # Player
        self.player = Player((8, 12))
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

    def run_game(self) -> None:
        gui_group = pygame.sprite.RenderUpdates()
        while 1:
            self.check_events()
            self.update(gui_group)
            self.render(gui_group)
            self.clock.tick_busy_loop(self.screen_settings.fps)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.cursor.sprite.register_click(True)  # type: ignore
            elif event.type == pygame.MOUSEBUTTONUP:
                self.cursor.sprite.register_click(False)  # type: ignore

    def update(self, gui_group):
        gui_group.update(self.cursor)
        self.player_group.update()
        self.cursor.update(pygame.mouse.get_pos())

    def render(self, gui_group):
        self.screen.fill(self.colours.background_colour)
        gui_group.draw(self.screen)
        self.player_group.draw(self.screen)
        if self.cursor_settings.cursor_sprite_as_cursor:
            self.cursor.draw(self.screen)

        pygame.display.update()

    def _check_keydown_events(self, event) -> None:
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.player.set_moving_up(True)
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.player.set_moving_down(True)
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.player.set_moving_left(True)
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.player.set_moving_right(True)

    def _check_keyup_events(self, event) -> None:
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.player.set_moving_up(False)
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.player.set_moving_down(False)
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.player.set_moving_left(False)
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.player.set_moving_right(False)


if __name__ == "__main__":
    rpg = Game()
    rpg.run_game()
