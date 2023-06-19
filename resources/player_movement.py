import pygame
import math

class Game:
    def __init__(self, width=800, height=640, tile_size=32, player_speed=6):
        pygame.init()
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.player_speed = player_speed
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.player = self.Player(0, 0, self)
        self.running = True

    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y, game):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((game.tile_size, game.tile_size))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.target_x = x
            self.target_y = y
            self.speed = game.player_speed
            self.game = game

        def snap_to_grid(self):
            remainder_x = self.rect.x % self.game.tile_size
            remainder_y = self.rect.y % self.game.tile_size

            if remainder_x < self.game.tile_size / 2:
                self.target_x = self.rect.x - remainder_x
            else:
                self.target_x = self.rect.x + self.game.tile_size - remainder_x

            if remainder_y < self.game.tile_size / 2:
                self.target_y = self.rect.y - remainder_y
            else:
                self.target_y = self.rect.y + self.game.tile_size - remainder_y

        def update(self):
            error_x = self.target_x - self.rect.x
            error_y = self.target_y - self.rect.y

            distance = (error_x ** 2 + error_y ** 2) ** 0.5
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
            if self.rect.right > self.game.width:
                self.rect.right = self.game.width
                self.target_x = self.rect.x
            if self.rect.top < 0:
                self.rect.top = 0
                self.target_y = self.rect.y
            if self.rect.bottom > self.game.height:
                self.rect.bottom = self.game.height
                self.target_y = self.rect.y

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            if self.player.rect.x == self.player.target_x and self.player.rect.y == self.player.target_y:
                dx = 0
                dy = 0
                if keys[pygame.K_LEFT]:
                    dx = -self.tile_size
                elif keys[pygame.K_RIGHT]:
                    dx = self.tile_size
                elif keys[pygame.K_UP]:
                    dy = -self.tile_size
                elif keys[pygame.K_DOWN]:
                    dy = self.tile_size

                if dx != 0 or dy != 0:
                    self.player.target_x = self.player.rect.x + dx
                    self.player.target_y = self.player.rect.y + dy

            self.player.update()

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.player.image, self.player.rect)

            for y in range(0, self.height, self.tile_size):
                pygame.draw.line(self.screen, (255, 255, 255), (0, y), (self.width, y))

            for x in range(0, self.width, self.tile_size):
                pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, self.height))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        