import pygame

WIDTH = 800
HEIGHT = 600
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
    def check_collision(self, dx, dy):
        if dx < 0 and self.rect.left % TILE_SIZE == 0:
            self.rect.x -= TILE_SIZE
        elif dx > 0 and self.rect.right % TILE_SIZE == 0:
            self.rect.x += TILE_SIZE

        if dy < 0 and self.rect.top % TILE_SIZE == 0:
            self.rect.y -= TILE_SIZE
        elif dy > 0 and self.rect.bottom % TILE_SIZE == 0:
            self.rect.y += TILE_SIZE

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

        self.check_collision(dx, dy)

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

    screen.fill((0, 0, 0))
    screen.blit(player.image, player.rect)

    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
