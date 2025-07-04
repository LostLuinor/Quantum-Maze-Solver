import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20  # Size of each cell in the maze

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Enhanced Maze with Loops')

# Frame rate control
clock = pygame.time.Clock()

# Number of rows and columns in the maze
cols = SCREEN_WIDTH // CELL_SIZE
rows = SCREEN_HEIGHT // CELL_SIZE

# Maze grid (initialized with walls)
maze = [[1 for _ in range(cols)] for _ in range(rows)]

# Ensure the outermost boundaries are walls
for i in range(rows):
    maze[i][0] = 1  # Left boundary
    maze[i][cols - 1] = 1  # Right boundary
for j in range(cols):
    maze[0][j] = 1  # Top boundary
    maze[rows - 1][j] = 1  # Bottom boundary

# Fix the goal point
maze[rows - 2][cols - 2] = 0  # Mark the goal as a path

# Directions for DFS: right, down, left, up (in terms of grid movement)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Recursive DFS function to generate the maze
def generate_maze(x, y, loop_prob=0.1):
    maze[x][y] = 0  # Mark the cell as a path
    random.shuffle(DIRECTIONS)  # Randomize direction
    
    draw_maze()
    draw_start_and_end()

        # Update the display
    pygame.display.flip()

        # Limit the frame rate
    clock.tick(10)

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx * 2, y + dy * 2

        # Check if the new cell is within the inner maze boundaries
        if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[nx][ny] == 1:
            # Occasionally skip knocking down a wall to create loops
            if random.random() < loop_prob:
                continue

            # Knock down the wall between the current cell and the new cell
            maze[x + dx][y + dy] = 0
            # Recursively visit the new cell
            generate_maze(nx, ny, loop_prob)

# Add loops to the maze after generation
def add_loops(extra_loops=10):
    for _ in range(extra_loops):
        x = random.randint(1, cols - 2)
        y = random.randint(1, rows - 2)

        # Only knock down a wall if it exists
        if maze[x][y] == 1:
            maze[x][y] = 0

# Draw the maze
def draw_maze():
    for x in range(cols):
        for y in range(rows):
            color = WHITE if maze[x][y] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw start and end points
def draw_start_and_end():
    pygame.draw.rect(screen, GREEN, (CELL_SIZE, CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Start
    pygame.draw.rect(screen, RED, ((cols - 2) * CELL_SIZE, (rows - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Goal

# Main game loop
def main():
    generate_maze(1, 1, loop_prob=0.1)  # Generate maze with loops
    add_loops(extra_loops=20)  # Add extra loops

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Fill the screen with black background
        screen.fill(BLACK)

        # Draw the maze and the start/goal points
        draw_maze()
        draw_start_and_end()

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
