import os
import pygame
from CHARACTER_ASSETS import Player, Pacman, check_game_over

pygame.init()

# -----------------------------
# FILE SEARCH FUNCTION (optional)
# -----------------------------
def find_file(filename, start_dir="."):
    filename = filename.lower()
    for root, _, files in os.walk(start_dir):
        for f in files:
            if f.lower() == filename:
                return os.path.join(root, f)
    raise FileNotFoundError(f"{filename} not found in {start_dir}")

# -----------------------------
# BASIC SETUP
# -----------------------------
BASE_WIDTH, BASE_HEIGHT = 1000, 800
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Pacman")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

tile_size = 40
offset_x, offset_y = 50, 50

# -----------------------------
# FIXED MAZE
# -----------------------------
bg = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W..................W",
    "W..WWW......WWW....W",
    "W..................W",
    "W..WWWW....WWWW....W",
    "W..................W",
    "W..WWW......WWW....W",
    "W..................W",
    "W..................W",
    "WWWWWWWWWWWWWWWWWWWW",
]

score = 0
lives = 3

# -----------------------------
# WALL AND DOT SETUP
# -----------------------------
walls = []
dots = []

for y, line in enumerate(bg):
    for x, char in enumerate(line):
        draw_x = offset_x + x * tile_size
        draw_y = offset_y + y * tile_size
        if char == "W":
            walls.append(pygame.Rect(draw_x, draw_y, tile_size, tile_size))
        elif char == ".":
            dots.append(pygame.Rect(draw_x, draw_y, tile_size, tile_size))

# -----------------------------
# LOAD ASSETS
# -----------------------------
try:
    ASSET_DIR = "Pac-Man/code/Assets/Pacmanlives.png"
    player_img_path = os.path.join(ASSET_DIR, "player.jpg")
    pacman_img_path = os.path.join(ASSET_DIR, "pacman.png")
    lives_img_path = os.path.join(ASSET_DIR, "Pacmanlives.png")
    player_img_path_abs = os.path.abspath(player_img_path)
    player_img = pygame.image.load(player_img_path).convert_alpha()
    pacman_img = pygame.image.load(pacman_img_path).convert_alpha()
    pacman_lives_img = pygame.image.load(lives_img_path).convert_alpha()

except (FileNotFoundError, pygame.error) as e:
    print(f"Asset missing: {e}")

    player_img = pygame.Surface((tile_size, tile_size))
    player_img.fill((0, 255, 0))

    pacman_img = pygame.Surface((tile_size, tile_size))
    pacman_img.fill((255, 255, 0))

    pacman_lives_img = pygame.Surface((30, 30))
    pacman_lives_img.fill((255, 0, 0))

# Scale images
player_img = pygame.transform.scale(player_img, (tile_size, tile_size))
pacman_img = pygame.transform.scale(pacman_img, (tile_size, tile_size))
pacman_lives_img = pygame.transform.scale(pacman_lives_img, (30, 30))

# -----------------------------
# PLAYER + PACMAN
# -----------------------------
player = Player(offset_x + tile_size, offset_y + tile_size)
pacman = Pacman(offset_x + tile_size * 5, offset_y + tile_size * 5)

player.image = player_img
pacman.image = pacman_img

# -----------------------------
# DOT EATING (Pacman only)
# -----------------------------
def eat_dots(pacman, dots):
    global score
    for dot in dots[:]:
        if pacman.rect.colliderect(dot):
            dots.remove(dot)
            score += 10

# -----------------------------
# COLLISION HELPER
# -----------------------------
def move_with_walls(sprite, dx, dy, walls):
    sprite.rect.x += dx
    for wall in walls:
        if sprite.rect.colliderect(wall):
            if dx > 0:
                sprite.rect.right = wall.left
            if dx < 0:
                sprite.rect.left = wall.right

    sprite.rect.y += dy
    for wall in walls:
        if sprite.rect.colliderect(wall):
            if dy > 0:
                sprite.rect.bottom = wall.top
            if dy < 0:
                sprite.rect.top = wall.bottom

# -----------------------------
# UI FUNCTIONS
# -----------------------------
def scoreboard(x, y, score):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))

def draw_lives(lives):
    for i in range(lives):
        screen.blit(pacman_lives_img, (10 + i * 35, 60))

# -----------------------------
# GAME LOOP
# -----------------------------
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if not game_over:
        # Player input (ghost)
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed

        # Move player (ghost)
        move_with_walls(player, dx, dy, walls)

        # Move Pacman
        dx_pac, dy_pac = pacman.get_movement(player)
        move_with_walls(pacman, dx_pac, 0, walls)
        move_with_walls(pacman, 0, dy_pac, walls)

        # Pacman eats dots
        eat_dots(pacman, dots)

        # Check collision (ghost catches Pacman)
        if check_game_over(player, pacman):
            lives -= 1
            player.rect.topleft = (offset_x + tile_size, offset_y + tile_size)
            pacman.rect.topleft = (offset_x + tile_size * 5, offset_y + tile_size * 5)

            if lives <= 0:
                game_over = True

        # Win condition (all dots eaten)
        if len(dots) == 0:
            game_over = True

    else:
        # Restart game with R key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            score = 0
            lives = 3
            # Reset dots
            dots.clear()
            for y, line in enumerate(bg):
                for x, char in enumerate(line):
                    if char == ".":
                        draw_x = offset_x + x * tile_size
                        draw_y = offset_y + y * tile_size
                        dots.append(pygame.Rect(draw_x, draw_y, tile_size, tile_size))
            # Reset positions
            player.rect.topleft = (offset_x + tile_size, offset_y + tile_size)
            pacman.rect.topleft = (offset_x + tile_size * 5, offset_y + tile_size * 5)

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 255), wall)

    # Draw dots
    for dot in dots:
        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (dot.x + tile_size // 2, dot.y + tile_size // 2),
            tile_size // 8
        )

    # Draw characters
    screen.blit(player.image, player.rect)
    screen.blit(pacman.image, pacman.rect)

    # Draw UI
    scoreboard(10, 10, score)
    draw_lives(lives)

    # Game over screen
    if game_over:
        text = font.render("GAME OVER - Press R to Restart", True, (255, 0, 0))
        text_rect = text.get_rect(center=(BASE_WIDTH // 2, BASE_HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
