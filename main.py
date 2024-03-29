import pygame
from sys import exit

import resources.utils as utils
import resources.game_settings as game_settings
import resources.gui.gui as gui
from resources.map.map import Grid
from resources.player import Player
from resources.enemies.enemy import Enemy
from resources.items.item import Inventory
from resources.combat.combat import Combat


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.json_utils = utils.JsonUtils()
        self.screen_settings = game_settings.Screen()
        self.colours = game_settings.Colours()
        self.cursor_settings = game_settings.Cursor()
        self.player_settings = game_settings.Player()
        self.events = game_settings.Events()
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
        self.player: Player = Player((8, 12))
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)
        self.last_damage_counter = self.player_settings.tile_damage_interval
        self.inventory = Inventory()

    def run_game(self) -> None:
        self.level()

    def level(self) -> None:
        map_surface, triggers_group, gui_group, enemy_group = self.init_level(-1)
        while 1:
            self.check_events(triggers_group, enemy_group)
            self.update(gui_group, enemy_group)
            self.render(map_surface, gui_group, enemy_group)
            self.clock.tick_busy_loop(self.screen_settings.fps)

    def init_level(self, level: int) -> tuple:
        grid = Grid(-1)
        triggers_group = pygame.sprite.Group(grid.triggers)
        gui_group = pygame.sprite.RenderUpdates()
        enemy_group = pygame.sprite.RenderUpdates(grid.enemies)
        return grid.image, triggers_group, gui_group, enemy_group

    def check_events(
        self,
        triggers,
        enemy_group: pygame.sprite.RenderUpdates,
        check_collision: bool = True,
    ):
        self._check_collision_events(triggers, enemy_group)
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

    def update(self, gui_group, enemy_group):
        gui_group.update(self.cursor)
        self.player_group.update()
        enemy_group.update(self.player.get_raw_pos())
        self.cursor.update(pygame.mouse.get_pos())

    def render(self, map: pygame.Surface, gui_group, enemy_group):
        self.screen.fill(self.colours.background_colour)
        self.screen.blit(map, (0, 0))

        enemy_group.draw(self.screen)
        self.player_group.draw(self.screen)
        gui_group.draw(self.screen)
        if self.cursor_settings.cursor_sprite_as_cursor:
            self.cursor.draw(self.screen)

        pygame.display.update()

    def combat(self, enemy) -> int:
        ended = False
        ended_render = False
        dead = -1
        tracker = Combat(self.player, enemy, self.inventory)
        gui_group = pygame.sprite.RenderUpdates()
        background = self._get_screen_as_surface()
        gui_group.add(
            gui.Overlay(
                pygame.Rect(
                    self.screen_width // 2,
                    self.screen_height // 2,
                    self.screen_width,
                    self.screen_height,
                ),
                0,
                self.colours.background_colour,
            ),
            gui.Text(
                "cochin",
                "Battle against the Void",
                (self.screen_width // 2, int(self.screen_height * 0.1)),
                self.colours.white,
                30,
            ),
            gui.Button(
                pygame.Rect(
                    self.screen_width * 0.33,
                    self.screen_height * 0.8,
                    200,
                    50,
                ),
                "Attack",
                self.colours.white,
                1,
            ),
            gui.Button(
                pygame.Rect(
                    self.screen_width * 0.66,
                    self.screen_height * 0.8,
                    200,
                    50,
                ),
                "Escape",
                self.colours.white,
                3,
            ),
        )
        gui_message = (
            gui.Text(
                "cochin",
                "",
                (self.screen_width // 2, int(self.screen_height * 0.9)),
                self.colours.white,
            ),
        )
        gui_player_health = (
            gui.Text(
                "cochin",
                "",
                (self.screen_width // 2, int(self.screen_height * 0.9)),
                self.colours.white,
            ),
        )
        gui_enemy_health = (
            gui.Text(
                "cochin",
                "",
                (self.screen_width // 2, int(self.screen_height * 0.9)),
                self.colours.white,
            ),
        )
        while not ended:
            # Collect Events
            button_pressed = -1
            combat_event = None
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
                elif event.type == self.events.button_pressed_event:
                    button_pressed = event.index
                elif event.type == self.events.combat:
                    combat_event = event

            # Update the combat
            self.cursor.update(pygame.mouse.get_pos())
            tracker.update(button_pressed)
            match tracker.get_state():
                case "enemy turn finished":  # Prepare player buttons
                    for sprite in gui_group:
                        sprite.kill()
                    gui_group.empty()
                    gui_group.add(
                        gui.Overlay(
                            pygame.Rect(
                                self.screen_width // 2,
                                self.screen_height // 2,
                                self.screen_width,
                                self.screen_height,
                            ),
                            0,
                            self.colours.background_colour,
                        ),
                        gui.Text(
                            "cochin",
                            "Battle against the Void",
                            (self.screen_width // 2, int(self.screen_height * 0.1)),
                            self.colours.white,
                            30,
                        ),
                        gui.Button(
                            pygame.Rect(
                                self.screen_width * 0.33,
                                self.screen_height * 0.8,
                                200,
                                50,
                            ),
                            "Attack",
                            self.colours.white,
                            1,
                        ),
                        gui.Button(
                            pygame.Rect(
                                self.screen_width * 0.66,
                                self.screen_height * 0.8,
                                200,
                                50,
                            ),
                            "Escape",
                            self.colours.white,
                            3,
                        ),
                    )
                case "ended":
                    if not ended_render:
                        gui_group.add(
                            gui.Overlay(
                                pygame.Rect(
                                    self.screen_width // 2,
                                    self.screen_height // 2,
                                    self.screen_width,
                                    self.screen_height,
                                ),
                                0,
                                self.colours.background_colour,
                            ),
                            gui.Text(
                                "cochin",
                                "Battle against the Void",
                                (self.screen_width // 2, int(self.screen_height * 0.1)),
                                self.colours.white,
                                30,
                            ),
                            gui.Button(
                                pygame.Rect(
                                    self.screen_width // 2,
                                    self.screen_height * 0.8,
                                    500,
                                    50,
                                ),
                                "End",
                                self.colours.white,
                                4,
                            ),
                        )
                        ended_render = True
                    else:
                        if button_pressed == 4:
                            ended = True

            gui_group.update(self.cursor)
            if combat_event is not None:
                message = ""
                actions = combat_event.dict
                if "dict" in actions.keys():
                    actions = actions["dict"]
                if "dead" in actions.keys():
                    if actions["dead"] == "player":
                        message = ""
                        dead = 1
                    elif actions["dead"] == "enemy":
                        message = "The Void is dead. Was it easy?"
                        dead = 2
                elif actions["turn"] == "enemy turn":
                    message = "Weird... The Void did nothing."
                    if "attack_success" in actions.keys():
                        if actions["attack_success"]:
                            message = "The Void damaged you."
                        else:
                            message = "The Void attempted to damage you, but failed."
                    elif "escape_success" in actions.keys():
                        if actions["escape_success"]:
                            message = "The Void escaped."
                        else:
                            message = "The Void attempted to escape, but failed."
                gui_group.remove(gui_message)
                gui_message = gui.Text(
                    "cochin",
                    message,
                    (self.screen_width // 2, int(self.screen_height * 0.9)),
                    self.colours.white,
                )
                gui_group.add(gui_message)
                gui_group.remove(gui_player_health)
                gui_player_health = gui.Text(
                    "cochin",
                    "Player Health: " + str(tracker.get_player_health()),
                    (self.screen_width // 2, int(self.screen_height * 0.475)),
                    self.colours.white,
                )
                gui_group.add(gui_player_health)
                gui_group.remove(gui_enemy_health)
                gui_enemy_health = gui.Text(
                    "cochin",
                    "Enemy Health: " + str(tracker.get_enemy_health()),
                    (self.screen_width // 2, int(self.screen_height * 0.525)),
                    self.colours.white,
                )
                gui_group.add(gui_enemy_health)

            # Render
            self.screen.fill(self.colours.background_colour)
            self.screen.blit(background, (0, 0))
            gui_group.draw(self.screen)
            if self.cursor_settings.cursor_sprite_as_cursor:
                self.cursor.draw(self.screen)

            pygame.display.update()
            self.clock.tick_busy_loop(self.screen_settings.fps)

        for sprite in gui_group:
            sprite.kill()

        self.screen.fill(self.colours.background_colour)
        self.screen.blit(background, (0, 0))
        gui_group.draw(self.screen)
        if self.cursor_settings.cursor_sprite_as_cursor:
            self.cursor.draw(self.screen)

        pygame.display.update()
        self.clock.tick_busy_loop(self.screen_settings.fps)

        return dead

    def death_screen(self) -> None:
        gui_group = pygame.sprite.RenderUpdates()
        gui_group.add(
            gui.Overlay(
                pygame.Rect(
                    self.screen_width // 2,
                    self.screen_height // 2,
                    self.screen_width,
                    self.screen_height,
                ),
                0,
                self.colours.red,
            ),
            gui.Text(
                "cochin",
                "Devoided.",
                (self.screen_width // 2, int(self.screen_height * 0.45)),
                self.colours.white,
                50,
            ),
            gui.Text(
                "cochin",
                "Restart the game to respawn.",
                (self.screen_width // 2, int(self.screen_height * 0.55)),
                self.colours.black,
            ),
        )
        background = self._get_screen_as_surface()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.cursor.update(pygame.mouse.get_pos())
            gui_group.update()

            self.screen.fill(self.colours.background_colour)
            self.screen.blit(background, (0, 0))
            gui_group.draw(self.screen)
            if self.cursor_settings.cursor_sprite_as_cursor:
                self.cursor.draw(self.screen)

            pygame.display.update()
            self.clock.tick_busy_loop(self.screen_settings.fps)

    def _get_screen_as_surface(self) -> pygame.Surface:
        surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        surface.blit(
            self.screen, pygame.Rect(0, 0, self.screen_width, self.screen_height)
        )
        return surface

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

    def _check_collision_events(self, triggers, enemy_group) -> None:
        for sprite in pygame.sprite.spritecollide(self.player, triggers, False):
            if sprite.get_type() == "damage":
                self.player.collision(False)
            elif sprite.get_type() == "neutral":
                self.player.collision(False)
            elif sprite.get_type() == "obstruction":
                self.player.collision(True)
            if self.last_damage_counter <= 0:
                self.player.damage(2)
            self.last_damage_counter = self.player_settings.tile_damage_interval

        for enemy, sprites in pygame.sprite.groupcollide(
            enemy_group, triggers, False, False
        ).items():
            modified = False
            for sprite in sprites:
                if not modified:
                    if sprite.get_type() == "damage":
                        if enemy.get_is_colliding():  # type: ignore
                            modified = True
                        enemy.collision(False)  # type: ignore
                    elif sprite.get_type() == "obstruction":
                        if not enemy.get_is_colliding():  # type: ignore
                            modified = True
                        enemy.collision(True)  # type: ignore
                    else:
                        if enemy.get_is_colliding():  # type: ignore
                            modified = True
                        enemy.collision(False)  # type: ignore

        for enemy in pygame.sprite.spritecollide(self.player, enemy_group, False):
            result = self.combat(enemy)
            if result == 1:
                self.death_screen()
            elif result == 2:
                enemy.kill()

        self.last_damage_counter -= 1 if self.last_damage_counter > 0 else 0


if __name__ == "__main__":
    rpg = Game()
    rpg.run_game()
