import pygame
import math
import resources.game_settings as game_settings


class Player(pygame.sprite.Sprite):
    def __init__(self, in_game_pos: tuple[int, int]):
        # Initialise the Player object.
        pygame.sprite.Sprite.__init__(self)

        self.player_settings = game_settings.Player()
        self.screen_settings = game_settings.Screen()
        self.map_settings = game_settings.Map()
        self.colours = game_settings.Colours()

        self.raw_pos = (
            in_game_pos[0] * self.map_settings.tile_size
            - (self.map_settings.tile_size // 2),
            in_game_pos[1] * self.map_settings.tile_size
            - (self.map_settings.tile_size // 2),
        )
        x = self.raw_pos[0]
        y = self.raw_pos[1]
        self.target_x = x
        self.target_y = y
        self.speed = self.player_settings.speed
        self.screen_width = self.screen_settings.screen_size[0]
        self.screen_height = self.screen_settings.screen_size[1]
        self.tile_size = self.map_settings.tile_size

        self.dx = 0
        self.dy = 0
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.is_colliding = False
        self.health = self.player_settings.max_heath
        self.defence = 0.2

        self.image = pygame.Surface((self.tile_size, self.tile_size))
        self.image.fill(self.colours.white)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = (x, y)

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
            self.move_stop()
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
        self.dx = self.tile_size // 4

    def set_moving_left(self, condition: bool) -> None:
        self.moving_left = condition
        self.dx = -self.tile_size // 4

    def set_moving_up(self, condition: bool) -> None:
        self.moving_up = condition
        self.dy = -self.tile_size // 4

    def set_moving_down(self, condition: bool) -> None:
        self.moving_down = condition
        self.dy = self.tile_size // 4

    def is_moving_x(self) -> bool:
        return True if not self.moving_up and not self.moving_down else False

    def is_moving_y(self) -> bool:
        return True if not self.moving_left and not self.moving_right else False

    def get_stats(self) -> tuple:
        return self.health, self.defence

    def damage(self, damage) -> None:
        self.health -= damage

    def collision(self, is_colliding: bool) -> None:
        self.is_colliding = is_colliding
        if is_colliding:
            self.move_stop()

    def move_stop(self) -> None:
        # Stop the player from moving.
        self._snap_to_grid_x()
        self._snap_to_grid_y()

    def _snap_to_grid_x(self) -> None:
        """Adjust player's x position to align with the grid."""
        remainder_x = self.rect.x % self.tile_size
        if self.is_colliding:
            self.dx = 0
        if not self.moving_right and not self.moving_left:
            self.rect.x += self.dx
            self.dx = 0

        if remainder_x < self.tile_size / 2:
            self.target_x = self.rect.x - remainder_x
        else:
            self.target_x = self.rect.x + self.tile_size - remainder_x

    def _snap_to_grid_y(self) -> None:
        """Adjust player's y position to align with the grid."""
        remainder_y = self.rect.y % self.tile_size
        if self.is_colliding:
            self.dy = 0
        if not self.moving_up and not self.moving_down:
            self.rect.y += self.dy
            self.dy = 0

        if remainder_y < self.tile_size / 2:
            self.target_y = self.rect.y - remainder_y
        else:
            self.target_y = self.rect.y + self.tile_size - remainder_y
