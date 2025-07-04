import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 30  # Size of each cell in the maze

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (200, 100, 50)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze with Buttons')

# Frame rate control
clock = pygame.time.Clock()

# Number of rows and columns in the maze
cols = SCREEN_WIDTH // CELL_SIZE
rows = SCREEN_HEIGHT // CELL_SIZE

# Maze grid (initialized with walls)
maze = [[1 for _ in range(cols)] for _ in range(rows)]

# Directions for DFS: right, down, left, up (in terms of grid movement)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Generate the maze using DFS
def generate_maze(x, y):
    maze[x][y] = 0
    random.shuffle(DIRECTIONS)

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx * 2, y + dy * 2

        if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[nx][ny] == 1:
            maze[x + dx][y + dy] = 0
            generate_maze(nx, ny)

# Draw the maze
def draw_maze():
    for x in range(cols):
        for y in range(rows):
            color = WHITE if maze[x][y] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Add buttons at specific grid positions
BUTTON_POSITIONS = [(3, 3), (5, 5), (7, 7)]  # Grid positions for buttons

def draw_buttons():
    for bx, by in BUTTON_POSITIONS:
        pygame.draw.rect(
            screen,
            BUTTON_COLOR,
            (bx * CELL_SIZE, by * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

# Functions to be triggered by button clicks
def button_action_1():
    print("Button 1 clicked! 🎉")

def button_action_2():
    print("Button 2 clicked! 🎉")

def button_action_3():
    print("Button 3 clicked! 🎉")

# Map buttons to actions
BUTTON_ACTIONS = {
    (3, 3): button_action_1,
    (5, 5): button_action_2,
    (7, 7): button_action_3,
}

# Handle button clicks
def handle_button_click(mouse_pos):
    mx, my = mouse_pos
    grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE  # Convert pixel to grid position

    if (grid_x, grid_y) in BUTTON_ACTIONS:
        BUTTON_ACTIONS[(grid_x, grid_y)]()

# Main game loop
def main():
    generate_maze(1, 1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_click(pygame.mouse.get_pos())

        # Draw everything
        screen.fill(BLACK)
        draw_maze()
        draw_buttons()

        # Update display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
