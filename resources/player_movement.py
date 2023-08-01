import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        screen_width: int,
        screen_height: int,
        tile_size: int,
        player_speed: int,
    ):
        # Initialise the Player object.
        pygame.sprite.Sprite().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((255, 0, 0))
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_x = x
        self.target_y = y
        self.speed = player_speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self) -> None:
        if self.moving_right:
            self.target_x += self.speed
        elif self.moving_left:
            self.target_x -= self.speed
        else:
            self._snap_to_grid_x()
        if self.moving_down:
            self.target_y += self.speed
        elif self.moving_up:
            self.target_y -= self.speed
        else:
            self._snap_to_grid_y()
        if (
            not self.moving_right
            and not self.moving_left
            and not self.moving_up
            and not self.moving_down
        ):
            self._move_stop()
        # Update player's position based on the target position.
        error_x = self.target_x - self.rect.x
        error_y = self.target_y - self.rect.y

        distance = (error_x**2 + error_y**2) ** 0.5
        if distance < self.speed:
            self.rect.x = self.target_x
            self.rect.y = self.target_y
        else:
            theta = math.atan2(error_y, error_x)
            self.rect.x += round(self.speed * math.cos(theta))
            self.rect.y += round(self.speed * math.sin(theta))

        if self.rect.left < 0:
            self.rect.left = 0
            self.target_x = self.rect.x
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.target_x = self.rect.x
        if self.rect.top < 0:
            self.rect.top = 0
            self.target_y = self.rect.y
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
            self.target_y = self.rect.y

    def set_moving_right(self, condition: bool) -> None:
        self.moving_right = condition

    def set_moving_left(self, condition: bool) -> None:
        self.moving_left = condition

    def set_moving_up(self, condition: bool) -> None:
        self.moving_up = condition

    def set_moving_down(self, condition: bool) -> None:
        self.moving_down = condition

    def _move_stop(self) -> None:
        # Stop the player from moving.
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self._snap_to_grid_x()
        self._snap_to_grid_y()

    def _snap_to_grid_x(self) -> None:
        """Adjust player's x position to align with the grid."""
        remainder_x = self.rect.x % self.tile_size

        if remainder_x < self.tile_size / 2:
            self.target_x = self.rect.x - remainder_x
        else:
            self.target_x = self.rect.x + self.tile_size - remainder_x

    def _snap_to_grid_y(self) -> None:
        """Adjust player's y position to align with the grid."""
        remainder_y = self.rect.y % self.tile_size

        if remainder_y < self.tile_size / 2:
            self.target_y = self.rect.y - remainder_y
        else:
            self.target_y = self.rect.y + self.tile_size - remainder_y
