import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Recursive Division Maze Generator')

# Initialize maze grid
cols = SCREEN_WIDTH // CELL_SIZE
rows = SCREEN_HEIGHT // CELL_SIZE
maze = [[0 for x in range(cols)] for y in range(rows)]

def draw_grid():
    screen.fill(WHITE)
    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, 
                               (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def add_border():
    # Add top and bottom walls
    for x in range(cols):
        maze[0][x] = 1
        maze[rows-1][x] = 1
    # Add left and right walls
    for y in range(rows):
        maze[y][0] = 1
        maze[y][cols-1] = 1

def divide(x, y, width, height, orientation):
    if width < 3 or height < 3:
        return

    # Find where to draw the wall
    wx = x + (0 if orientation else random.randint(1, width-2))
    wy = y + (random.randint(1, height-2) if orientation else 0)

    # Find where to put the passage
    px = wx + (0 if orientation else random.randint(0, 1))
    py = wy + (random.randint(0, 1) if orientation else 0)

    # Direction and length of the wall
    dx = 1 if orientation else 0
    dy = 0 if orientation else 1

    # Length of the wall
    length = min(height if orientation else width, rows - wy if orientation else cols - wx)

    # Draw the wall and add the passage with bounds checking
    for i in range(length):
        if orientation:
            if 0 <= (wy + i) < rows and 0 <= wx < cols:  # Check bounds
                if (wy + i) != py or wx != px:
                    maze[wy + i][wx] = 1
        else:
            if 0 <= wy < rows and 0 <= (wx + i) < cols:  # Check bounds
                if (wx + i) != px or wy != py:
                    maze[wy][wx + i] = 1

    # Recursively divide the created chambers
    nx, ny = (x, y)
    w = min(wx - x if orientation else width, cols - nx)
    h = min(height if orientation else wy - y, rows - ny)
    if w >= 3 and h >= 3:
        divide(nx, ny, w, h, not orientation)

    nx = x if orientation else wx + 1
    ny = wy + 1 if orientation else y
    w = min(width if orientation else x + width - wx - 1, cols - nx)
    h = min(y + height - wy - 1 if orientation else height, rows - ny)
    if w >= 3 and h >= 3:
        divide(nx, ny, w, h, not orientation)

def generate_maze():
    # Clear the maze
    for y in range(rows):
        for x in range(cols):
            maze[y][x] = 0

    add_border()
    divide(1, 1, cols-2, rows-2, random.choice([True, False]))

def main():
    clock = pygame.time.Clock()
    generate_maze()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    generate_maze()  # Generate new maze on spacebar press

        draw_grid()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()