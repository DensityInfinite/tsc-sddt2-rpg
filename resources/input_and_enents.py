import pygame

WIDTH = 800
HEIGHT = 640
TILE_SIZE = 32
PLAYER_SPEED = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def snap_to_grid(self):
        remainder_x = self.rect.x % TILE_SIZE
        remainder_y = self.rect.y % TILE_SIZE

        if remainder_x < TILE_SIZE / 2:
            self.rect.x -= remainder_x  # Move to the left grid
        else:
            self.rect.x += TILE_SIZE - remainder_x  # Move to the right grid

        if remainder_y < TILE_SIZE / 2:
            self.rect.y -= remainder_y  # Move to the upper grid
        else:
            self.rect.y += TILE_SIZE - remainder_y  # Move to the lower grid

    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

player = Player(0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_LEFT]:
        dx = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        dx = PLAYER_SPEED
    elif keys[pygame.K_UP]:
        dy = -PLAYER_SPEED
    elif keys[pygame.K_DOWN]:
        dy = PLAYER_SPEED

    player.update(dx, dy)

    # If no direction key is pressed, snap the player to the grid
    if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
        player.snap_to_grid()

    screen.fill((0, 0, 0))
    screen.blit(player.image, player.rect)

    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
