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
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_x = x
        self.target_y = y
        self.speed = player_speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size

    def snap_to_grid(self) -> None:
        # Adjust player's position to align with the grid.
        remainder_x = self.rect.x % self.tile_size
        remainder_y = self.rect.y % self.tile_size

        if remainder_x < self.tile_size / 2:
            self.target_x = self.rect.x - remainder_x
        else:
            self.target_x = self.rect.x + self.tile_size - remainder_x

        if remainder_y < self.tile_size / 2:
            self.target_y = self.rect.y - remainder_y
        else:
            self.target_y = self.rect.y + self.tile_size - remainder_y

    def update(self) -> None:
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

    def move_right(self) -> None:
        # Move the player right.
        self.rect.x += self.speed

    def move_left(self) -> None:
        # Move the player left.
        self.rect.x -= self.speed

    def move_up(self) -> None:
        # Move the player up.
        self.rect.y -= self.speed

    def move_down(self) -> None:
        # Move the player down.
        self.rect.y += self.speed
