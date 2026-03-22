import pygame

# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size=40, speed=4):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def handle_input(self):
        keys = pygame.key.get_pressed()

        dx = dy = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        return dx, dy


# PACMAN AI
class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, size=30, speed=2):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def get_movement(self, player):
        dx = dy = 0

        # Move AWAY from player (your original logic)
        direction = pygame.math.Vector2(
            self.rect.x - player.rect.x,
            self.rect.y - player.rect.y
        )

        if direction.length_squared() > 0:
            direction = direction.normalize()

        dx = direction.x * self.speed
        dy = direction.y * self.speed

        return dx, dy


# GAME OVER FUNCTION 
def check_game_over(player, pacman):
    return player.rect.colliderect(pacman.rect)
      
