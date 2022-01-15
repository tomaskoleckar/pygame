import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
class Stone(pygame.sprite.Sprite):
    def __init__(self):
        super(Stone, self).__init__()
        self.surf = pygame.image.load("stone.png").convert()
        self.surf = pygame.transform.scale(self.surf, (100, 20))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                -20,
            )
        )
        self.speed = 5

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0, +self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("python.png").convert()
        self.surf = pygame.transform.scale(self.surf, (70,70))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.left = SCREEN_WIDTH/2-(self.rect.right-self.rect.left)/2
        self.rect.bottom = SCREEN_HEIGHT
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH





pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDSTONE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDSTONE, 500)

player = Player()

stones = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDSTONE:
            # Create the new enemy and add it to sprite groups
            new_stone = Stone()
            stones.add(new_stone)
            all_sprites.add(new_stone)

    pressed_keys = pygame.key.get_pressed()

    clock = pygame.time.Clock()


    player.update(pressed_keys)

    screen.fill((0, 0, 0))

    if pygame.sprite.spritecollideany(player, stones):
        player.kill()


    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    stones.update()

    pygame.display.flip()

    clock.tick(60)