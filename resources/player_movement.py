import pygame
import math

WIDTH = 800
HEIGHT = 640
TILE_SIZE = 32
PLAYER_SPEED = 6

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target_x = x
        self.target_y = y
        self.speed = PLAYER_SPEED

    def snap_to_grid(self):
        remainder_x = self.rect.x % TILE_SIZE
        remainder_y = self.rect.y % TILE_SIZE

        if remainder_x < TILE_SIZE / 2:
            self.target_x = self.rect.x - remainder_x
        else:
            self.target_x = self.rect.x + TILE_SIZE - remainder_x

        if remainder_y < TILE_SIZE / 2:
            self.target_y = self.rect.y - remainder_y
        else:
            self.target_y = self.rect.y + TILE_SIZE - remainder_y

    def update(self):
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y

        distance = (dx**2 + dy**2) ** 0.5
        if distance < self.speed:
            self.rect.x = self.target_x
            self.rect.y = self.target_y
        else:
            theta = math.atan2(dy, dx)
            self.rect.x += round(self.speed * math.cos(theta))
            self.rect.y += round(self.speed * math.sin(theta))

        if self.rect.left < 0:
            self.rect.left = 0
            self.target_x = self.rect.x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.target_x = self.rect.x
        if self.rect.top < 0:
            self.rect.top = 0
            self.target_y = self.rect.y
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.target_y = self.rect.y


player = Player(0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if player.rect.x == player.target_x and player.rect.y == player.target_y:
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx = -TILE_SIZE
        elif keys[pygame.K_RIGHT]:
            dx = TILE_SIZE
        elif keys[pygame.K_UP]:
            dy = -TILE_SIZE
        elif keys[pygame.K_DOWN]:
            dy = TILE_SIZE

        if dx != 0 or dy != 0:
            player.target_x = player.rect.x + dx
            player.target_y = player.rect.y + dy

    player.update()

    screen.fill((0, 0, 0))
    screen.blit(player.image, player.rect)

    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
