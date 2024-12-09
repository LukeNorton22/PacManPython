import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
TILE_SIZE = WIDTH // 20  # 20 columns and 15 rows for the maze

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
WALL_COLOR = (0, 0, 128)
PELLET_COLOR = (255, 255, 255)
GHOST_EYE_WHITE = (255, 255, 255)
GHOST_EYE_BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac-Man with Maze')

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for score display
font = pygame.font.SysFont('arial', 24)

def game_over_screen(score):
    """Display the Game Over screen with the final score and replay option."""
    screen.fill(BLACK)
    game_over_text = font.render('Game Over', True, WHITE)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    replay_text = font.render('Press R to Replay or Q to Quit', True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(replay_text, (WIDTH // 2 - replay_text.get_width() // 2, HEIGHT // 1.5))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

def win_screen(score):
    """Display the Win screen with the final score and replay option."""
    screen.fill(BLACK)
    win_text = font.render('You Win!', True, WHITE)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    replay_text = font.render('Press R to Replay or Q to Quit', True, WHITE)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(replay_text, (WIDTH // 2 - replay_text.get_width() // 2, HEIGHT // 1.5))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

# Pac-Man settings
PACMAN_RADIUS = TILE_SIZE / 2
PACMAN_SPEED = 4

# Ghost settings
GHOST_RADIUS = TILE_SIZE / 2
GHOST_SPEED = 2

# Pellet settings
PELLET_RADIUS = 5

# Bullet settings
BULLET_RADIUS = 3
BIG_BULLET_RADIUS = 8
BULLET_SPEED = 6

# Define directions
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

# Maze layout (1 = wall, 0 = open path, 2 = ghost cage, 3 = gun vitamin, 4 = wall-breaking vitamin)
MAZES = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
]

# Place vitamins for each level
def place_gun_vitamin():
    """Randomly place the gun vitamin on any open path (not a wall or ghost cage)."""
    while True:
        row = random.randint(0, len(MAZE) - 1)
        col = random.randint(0, len(MAZE[0]) - 1)
        if MAZE[row][col] == 0:  # Check for open path
            MAZE[row][col] = 3
            break


def place_wall_break_vitamin():
    """Randomly place the wall-breaking vitamin on any open path (not a wall or ghost cage)."""
    while True:
        row = random.randint(0, len(MAZE) - 1)
        col = random.randint(0, len(MAZE[0]) - 1)
        if MAZE[row][col] == 0:  # Check for open path
            MAZE[row][col] = 4
            break

def reset_vitamins():
    """Reset vitamins for a new level."""
    place_gun_vitamin()
    place_wall_break_vitamin()


class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = DIRECTIONS['LEFT']
        self.queued_direction = None  # Store the next direction to move when possible
        self.angle = 45  # Mouth open angle
        self.mouth_opening = True  # Direction of mouth animation
        self.has_gun = False
        self.has_wall_breaker = False
        self.bullets = []
        self.bullet_count = 2  # Total bullets available
        self.big_bullet = None

    def move(self):
        # Check if the queued direction is valid
        if self.queued_direction:
            new_x = self.x + self.queued_direction[0] * PACMAN_SPEED
            new_y = self.y + self.queued_direction[1] * PACMAN_SPEED
            if not is_wall_collision(new_x, new_y, PACMAN_RADIUS):
                self.direction = self.queued_direction  # Change direction
                self.queued_direction = None  # Clear the queued direction

        # Move in the current direction
        new_x = self.x + self.direction[0] * PACMAN_SPEED
        new_y = self.y + self.direction[1] * PACMAN_SPEED

        if not is_wall_collision(new_x, new_y, PACMAN_RADIUS):
            self.x = new_x
            self.y = new_y

    def draw(self):
        direction_angle = {
            DIRECTIONS['UP']: 90,
            DIRECTIONS['DOWN']: 270,
            DIRECTIONS['LEFT']: 180,
            DIRECTIONS['RIGHT']: 0
        }[self.direction]

        start_angle = math.radians(direction_angle + self.angle / 2)
        end_angle = math.radians(direction_angle - self.angle / 2)

        pygame.draw.arc(
            screen, YELLOW,
            pygame.Rect(self.x - PACMAN_RADIUS, self.y - PACMAN_RADIUS, PACMAN_RADIUS * 2, PACMAN_RADIUS * 2),
            start_angle, end_angle, 0
        )
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), int(PACMAN_RADIUS))
        pygame.draw.polygon(
            screen, BLACK,
            [
                (self.x, self.y),
                (
                    self.x + PACMAN_RADIUS * math.cos(start_angle),
                    self.y - PACMAN_RADIUS * math.sin(start_angle)
                ),
                (
                    self.x + PACMAN_RADIUS * math.cos(end_angle),
                    self.y - PACMAN_RADIUS * math.sin(end_angle)
                )
            ]
        )

        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[1])), BULLET_RADIUS)

        if self.big_bullet:
            pygame.draw.circle(screen, ORANGE, (int(self.big_bullet[0]), int(self.big_bullet[1])), BIG_BULLET_RADIUS)

        # Update mouth angle for animation
        if self.mouth_opening:
            self.angle -= 2
            if self.angle <= 10:
                self.mouth_opening = False
        else:
            self.angle += 2
            if self.angle >= 45:
                self.mouth_opening = True

    def change_direction(self, direction):
        self.queued_direction = DIRECTIONS.get(direction, self.direction)

    def shoot(self):
        if self.has_gun and self.bullet_count > 0:
            bullet_x = self.x + self.direction[0] * (PACMAN_RADIUS + BULLET_RADIUS)
            bullet_y = self.y + self.direction[1] * (PACMAN_RADIUS + BULLET_RADIUS)
            self.bullets.append([bullet_x, bullet_y, self.direction])
            self.bullet_count -= 1
        elif self.has_wall_breaker and not self.big_bullet:
            bullet_x = self.x + self.direction[0] * (PACMAN_RADIUS + BIG_BULLET_RADIUS)
            bullet_y = self.y + self.direction[1] * (PACMAN_RADIUS + BIG_BULLET_RADIUS)
            self.big_bullet = [bullet_x, bullet_y, self.direction]

    def update_bullets(self, ghosts):
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2][0] * BULLET_SPEED
            bullet[1] += bullet[2][1] * BULLET_SPEED

            # Remove bullets that go out of bounds
            if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
                self.bullets.remove(bullet)
                continue

            if is_wall_collision(bullet[0], bullet[1], BULLET_RADIUS):
                self.bullets.remove(bullet)
                continue

            for ghost in ghosts[:]:
                if ((bullet[0] - ghost.x) ** 2 + (bullet[1] - ghost.y) ** 2) < (BULLET_RADIUS + GHOST_RADIUS) ** 2:
                    ghosts.remove(ghost)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

        if self.big_bullet:
            self.big_bullet[0] += self.big_bullet[2][0] * BULLET_SPEED
            self.big_bullet[1] += self.big_bullet[2][1] * BULLET_SPEED

            # Remove big bullet that goes out of bounds
            if self.big_bullet[0] < 0 or self.big_bullet[0] > WIDTH or self.big_bullet[1] < 0 or self.big_bullet[1] > HEIGHT:
                self.big_bullet = None
                return

            # Destroy walls
            big_bullet_grid = (int(self.big_bullet[0] // TILE_SIZE), int(self.big_bullet[1] // TILE_SIZE))
            if MAZE[big_bullet_grid[1]][big_bullet_grid[0]] == 1:
                MAZE[big_bullet_grid[1]][big_bullet_grid[0]] = 0
                self.big_bullet = None

class Ghost:
    def __init__(self, x, y, color=RED, personality='chaser', update_interval=10):
        self.x = x
        self.y = y
        self.color = color
        self.target = None  # Target position (Pac-Man's current position)
        self.path = []  # Path to the target
        self.personality = personality  # 'chaser', 'ambusher', 'wanderer', 'scatterer'
        self.direction = random.choice(list(DIRECTIONS.values()))  # Random starting direction
        self.update_interval = update_interval  # How often to recalculate the path (frames)
        self.frames_since_last_update = random.randint(0, update_interval)  # Start at a random frame

    def bfs(self, start, target):
        """Perform Breadth-First Search (BFS) to find the shortest path to the target."""
        queue = [start]
        visited = set()
        parent = {}

        visited.add(start)

        while queue:
            current = queue.pop(0)
            if current == target:
                break

            for direction in DIRECTIONS.values():
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if (0 <= neighbor[0] < len(MAZE[0]) and
                        0 <= neighbor[1] < len(MAZE) and
                        MAZE[neighbor[1]][neighbor[0]] != 1 and
                        neighbor not in visited):
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current

        # Reconstruct the path
        path = []
        current = target
        while current in parent:
            path.insert(0, current)
            current = parent[current]

        return path

    def move_towards_pacman(self, pacman, frame_count):
        """Move towards Pac-Man using BFS for pathfinding, but each ghost has its own strategy."""
        ghost_grid = (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))

        if self.personality == 'chaser':
            pacman_grid = (int(pacman.x // TILE_SIZE), int(pacman.y // TILE_SIZE))
        elif self.personality == 'ambusher':
            pacman_grid = (
                int((pacman.x + pacman.direction[0] * 10 * PACMAN_SPEED) // TILE_SIZE),
                int((pacman.y + pacman.direction[1] * 10 * PACMAN_SPEED) // TILE_SIZE)
            )
        elif self.personality in ['wanderer', 'scatterer']:
            self.move_randomly()
            return

        if self.frames_since_last_update >= self.update_interval or not self.path:
            self.target = pacman_grid
            self.path = self.bfs(ghost_grid, pacman_grid)
            self.frames_since_last_update = 0
        else:
            self.frames_since_last_update += 1

        if self.path:
            next_step = self.path[0]
            next_x = next_step[0] * TILE_SIZE + TILE_SIZE // 2
            next_y = next_step[1] * TILE_SIZE + TILE_SIZE // 2

            dx = next_x - self.x
            dy = next_y - self.y
            distance = math.hypot(dx, dy)

            if distance < GHOST_SPEED:
                self.x = next_x
                self.y = next_y
                self.path.pop(0)
            else:
                self.x += dx / distance * GHOST_SPEED
                self.y += dy / distance * GHOST_SPEED

    def move_randomly(self):
        """Move randomly, and if a wall is hit, choose a new direction."""
        new_x = self.x + self.direction[0] * GHOST_SPEED
        new_y = self.y + self.direction[1] * GHOST_SPEED

        if not is_wall_collision(new_x, new_y, GHOST_RADIUS):
            self.x = new_x
            self.y = new_y
        else:
            # Change to a new random direction if a wall is hit
            self.direction = random.choice(list(DIRECTIONS.values()))

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(GHOST_RADIUS))
        # Draw eyes
        eye_radius = GHOST_RADIUS // 4
        eye_offset = GHOST_RADIUS // 2
        pygame.draw.circle(screen, GHOST_EYE_WHITE, (int(self.x - eye_offset // 2), int(self.y - eye_offset)), eye_radius)
        pygame.draw.circle(screen, GHOST_EYE_WHITE, (int(self.x + eye_offset // 2), int(self.y - eye_offset)), eye_radius)
        pygame.draw.circle(screen, GHOST_EYE_BLUE, (int(self.x - eye_offset // 2), int(self.y - eye_offset)), eye_radius // 2)
        pygame.draw.circle(screen, GHOST_EYE_BLUE, (int(self.x + eye_offset // 2), int(self.y - eye_offset)), eye_radius // 2)


def draw_maze():
    for row_idx, row in enumerate(MAZE):
        for col_idx, tile in enumerate(row):
            if tile == 1:  # 1 for wall
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            elif tile == 3:  # 3 for gun vitamin
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = row_idx * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(screen, GREEN, (x, y), TILE_SIZE // 4)
            elif tile == 4:  # 4 for wall-breaking vitamin
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = row_idx * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(screen, RED, (x, y), TILE_SIZE // 4)

def is_wall_collision(x, y, radius):
    """Check if the bounding box of a circular entity at (x, y) with the given radius is colliding with any wall."""
    # Define the bounding box of the circle
    entity_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    # Iterate through the maze to check for collisions with walls
    for row_idx, row in enumerate(MAZE):
        for col_idx, tile in enumerate(row):
            if tile == 1:  # 1 for wall
                wall_rect = pygame.Rect(col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if entity_rect.colliderect(wall_rect):
                    return True
    return False

def generate_pellets():
    """Generate a list of pellet positions based on the maze."""
    pellets = []
    for row_idx, row in enumerate(MAZE):
        for col_idx, tile in enumerate(row):
            if tile == 0:  # Place a pellet on open paths only, avoid ghost cage
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = row_idx * TILE_SIZE + TILE_SIZE // 2
                pellets.append((x, y))
    return pellets

def draw_pellets(pellets):
    """Draw all pellets on the screen."""
    for pellet in pellets:
        pygame.draw.circle(screen, PELLET_COLOR, (int(pellet[0]), int(pellet[1])), PELLET_RADIUS)

def release_ghosts(ghosts):
    """Release ghosts from the cage after the game starts."""
    for ghost in ghosts:
        ghost.x = WIDTH // 2
        ghost.y = HEIGHT // 2

def check_pacman_collision(pacman, ghosts):
    """Check if Pac-Man collides with any ghost."""
    for ghost in ghosts:
        if ((pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2) < (PACMAN_RADIUS + GHOST_RADIUS) ** 2:
            return True
    return False

def check_gun_vitamin_collision(pacman):
    """Check if Pac-Man collides with a gun vitamin."""
    pacman_grid = (int(pacman.x // TILE_SIZE), int(pacman.y // TILE_SIZE))
    if MAZE[pacman_grid[1]][pacman_grid[0]] == 3:
        MAZE[pacman_grid[1]][pacman_grid[0]] = 0
        pacman.has_gun = True
        pacman.bullet_count = 5  # Reload the gun

def check_wall_break_vitamin_collision(pacman):
    """Check if Pac-Man collides with a wall-breaking vitamin."""
    pacman_grid = (int(pacman.x // TILE_SIZE), int(pacman.y // TILE_SIZE))
    if MAZE[pacman_grid[1]][pacman_grid[0]] == 4:
        MAZE[pacman_grid[1]][pacman_grid[0]] = 0
        pacman.has_wall_breaker = True

def main():
    levels = 3
    current_level = 0

    # Load sound effects
    eat_sound = pygame.mixer.Sound('eat.wav')
    gun_shot_sound = pygame.mixer.Sound('gun_shot.wav')

    while True:
        global MAZE
        MAZE = MAZES[current_level]
        pacman = PacMan(60, 60)
        ghosts = [
            Ghost(WIDTH // 2, HEIGHT // 2, RED, personality='chaser', update_interval=10),
            Ghost(WIDTH // 2, HEIGHT // 2, BLUE, personality='ambusher', update_interval=20),
            Ghost(WIDTH // 2, HEIGHT // 2, ORANGE, personality='wanderer', update_interval=15),
            Ghost(WIDTH // 2, HEIGHT // 2, CYAN, personality='scatterer', update_interval=30),
        ]

        pellets = generate_pellets()
        reset_vitamins()
        score = 0
        running = True
        ghosts_released = False
        frame_count = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pacman.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        pacman.change_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        pacman.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        pacman.change_direction('RIGHT')
                    elif event.key == pygame.K_SPACE:
                        pacman.shoot()
                        gun_shot_sound.play()  # Play gun shot sound when shooting

            if not ghosts_released:
                release_ghosts(ghosts)
                ghosts_released = True

            pacman.move()
            pacman.update_bullets(ghosts)
            check_gun_vitamin_collision(pacman)
            check_wall_break_vitamin_collision(pacman)

            # Check for collision with ghosts
            if check_pacman_collision(pacman, ghosts):
                if not game_over_screen(len(generate_pellets()) - len(pellets)):
                    pygame.quit()
                    sys.exit()
                break

            # Check for pellet collisions and play sound
            new_pellets = []
            for pellet in pellets:
                if ((pacman.x - pellet[0]) ** 2 + (pacman.y - pellet[1]) ** 2) <= (PACMAN_RADIUS + PELLET_RADIUS) ** 2:
                    eat_sound.play()  # Play sound when pellet is eaten
                else:
                    new_pellets.append(pellet)
            pellets = new_pellets

            # Check if all pellets are collected
            if not pellets:
                if current_level < levels - 1:
                    current_level += 1
                    running = False
                else:
                    if not win_screen(len(generate_pellets())):
                        pygame.quit()
                        sys.exit()
                    break

            # Move all ghosts toward Pac-Man
            for ghost in ghosts:
                ghost.move_towards_pacman(pacman, frame_count)

            frame_count += 1

            # Draw game objects
            screen.fill(BLACK)
            draw_maze()
            draw_pellets(pellets)
            pacman.draw()

            for ghost in ghosts:
                ghost.draw()

            # Draw score
            score_text = font.render(f'Score: {len(generate_pellets()) - len(pellets)}', True, WHITE)
            screen.blit(score_text, (10, 10))

            level_text = font.render(f'Level: {current_level + 1}', True, WHITE)
            screen.blit(level_text, (10, 40))

            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    main()
