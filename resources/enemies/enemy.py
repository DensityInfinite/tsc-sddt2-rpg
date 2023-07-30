import pygame, math
from random import randint
import resources.game_settings as settings


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self, in_game_pos: tuple[int, int], movement: tuple[int, int], raw_speed: int
    ) -> None:
        """raw_speed: the speed of the enemy in pixels"""
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        self.colours = settings.Colours()
        self.screen_settings = settings.Screen()
        self.map_settings = settings.Map()
        self.enemy_settings = settings.Enemy()

        self.state = "alone"

        self.raw_speed = raw_speed
        self.movement = movement
        self.chase_time = self.enemy_settings.chase_time * self.screen_settings.fps
        self.tick_counter = 0
        self.in_game_pos = in_game_pos
        self.raw_pos = (
            in_game_pos[0] * self.map_settings.tile_size
            - (self.map_settings.tile_size // 2),
            in_game_pos[1] * self.map_settings.tile_size
            - (self.map_settings.tile_size // 2),
        )
        self.image = pygame.Surface(
            (self.map_settings.tile_size, self.map_settings.tile_size)
        )
        self.image.fill(self.colours.red)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = self.raw_pos

    def update(self, player_raw_pos: tuple[int, int]):
        error_x = 0
        error_y = 0
        if self.state == "alone":
            if self.tick_counter <= 0:
                self.tick_counter = randint(0, 300)
                self.state = self._reshuffle_state()
            self.tick_counter -= 1
            target_x, target_y = self._get_target(self.state, player_raw_pos)
            error_x = target_x - self.rect.centerx
            error_y = target_y - self.rect.centery
        else:
            target_x, target_y = self._get_target(self.state, player_raw_pos)
            error_x = target_x - self.rect.centerx
            error_y = target_y - self.rect.centery

            match self.state:
                case "moving":
                    if error_x == 0 and error_y == 0:
                        self.state = "returning"
                case "returning":
                    if error_x == 0 and error_y == 0:
                        self.state = "alone"
                case "chasing":
                    self.chase_time -= 1
                    if (
                        abs(math.hypot(error_x, error_y))
                        < self.enemy_settings.time_increment_dis
                    ):
                        self.chase_time += self.enemy_settings.time_increment
                    if self.chase_time < 0:
                        self.state = "alone"
                        self.chase_time = (
                            self.enemy_settings.chase_time * self.screen_settings.fps
                        )

        if abs(error_x) != 0:
            self.rect.centerx += int(
                math.copysign(1, error_x) * min(self.raw_speed, abs(error_x))
            )
        if abs(error_y) != 0:
            self.rect.centery += int(
                math.copysign(1, error_y) * min(self.raw_speed, abs(error_y))
            )

    def _reshuffle_state(self) -> str:
        new_state = randint(1, 100)
        if new_state <= 75:
            return "moving"
        elif new_state <= 100:
            return "chasing"
        return ""

    def _get_target(
        self, state: str, player_raw_pos: tuple[int, int]
    ) -> tuple[int, int]:
        target_x, target_y = self.rect.center

        if state == "alone":
            target_x = (
                self.rect.centerx // self.map_settings.tile_size
            ) * self.map_settings.tile_size + self.map_settings.tile_size // 2
            target_y = (
                self.rect.centery // self.map_settings.tile_size
            ) * self.map_settings.tile_size + self.map_settings.tile_size // 2
        elif state == "moving":
            target_x = (
                self.in_game_pos[0] + self.movement[0]
            ) * self.map_settings.tile_size - self.map_settings.tile_size // 2
            target_y = (
                self.in_game_pos[1] + self.movement[1]
            ) * self.map_settings.tile_size - self.map_settings.tile_size // 2
        elif state == "returning":
            target_x = self.raw_pos[0]
            target_y = self.raw_pos[1]
        elif state == "chasing":
            target_x = player_raw_pos[0]
            target_y = player_raw_pos[1]

        return (target_x, target_y)
