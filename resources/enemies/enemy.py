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
        self.raw_pos = (
            in_game_pos[0] * self.map_settings.tile_size
            - self.map_settings.tile_size // 2,
            in_game_pos[1] * self.map_settings.tile_size
            - self.map_settings.tile_size // 2,
        )
        self.image = pygame.Surface(
            (self.map_settings.tile_size, self.map_settings.tile_size)
        )
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = self.raw_pos

    def update(self, player_raw_pos: tuple[int, int]):
        if self.state == "alone":
            self.state = self._reshuffle_state()
        else:
            target_y, target_x = self._get_target(self.state, player_raw_pos)
            error_y = target_y - self.rect.centery
            error_x = target_x - self.rect.centerx

            match self.state:
                case "moving":
                    if error_y == 0 and error_x == 0:
                        self.state = "returning"
                case "returning":
                    if error_y == 0 and error_x == 0:
                        self.state = "alone"
                case "chasing":
                    self.chase_time -= 1
                    if (
                        abs(math.hypot(error_y, error_x))
                        < self.enemy_settings.time_increment_dis
                    ):
                        self.chase_time += self.enemy_settings.time_increment
                    if self.chase_time < 0:
                        self.state = "alone"
                        self.chase_time = self.enemy_settings.chase_time

            self.rect.centery += (error_y // error_y) * min(self.raw_speed, error_y)
            self.rect.centerx += (error_x // error_x) * min(self.raw_speed, error_x)

    def _reshuffle_state(self) -> str:
        new_state = randint(1, 100)
        if new_state <= 50:
            return "alone"
        elif new_state <= 80:
            return "moving"
        elif new_state <= 100:
            return "chasing"
        return ""

    def _get_target(
        self, state: str, player_raw_pos: tuple[int, int]
    ) -> tuple[int, int]:
        target_y, target_x = self.rect.center
        match state:
            case "moving":
                target_y = self.movement[0]
                target_x = self.movement[1]
            case "returning":
                target_y = self.raw_pos[0]
                target_x = self.raw_pos[1]
            case "chasing":
                target_y = player_raw_pos[0]
                target_x = player_raw_pos[1]
        return (target_y, target_x)
