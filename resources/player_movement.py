import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, tile_size, player_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_x = x
        self.target_y = y
        self.speed = player_speed
        self.width = width
        self.height = height
        self.tile_size = tile_size

    def snap_to_grid(self):
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

    def update(self):
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
        if self.rect.right > self.width:
            self.rect.right = self.width
            self.target_x = self.rect.x
        if self.rect.top < 0:
            self.rect.top = 0
            self.target_y = self.rect.y
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
            self.target_y = self.rect.y

    def move_right(self):
        self.rect.x += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed
