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
WHITE = (255, 255, 255)  # Path color
BLACK = (0, 0, 0)        # Wall color

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Generator with Kruskal's Algorithm")

# Frame rate control
clock = pygame.time.Clock()

# Number of rows and columns in the maze
cols = SCREEN_WIDTH // CELL_SIZE
rows = SCREEN_HEIGHT // CELL_SIZE

# Walls lists
vertical_walls = []
horizontal_walls = []

def initialize_maze():
    global sets, walls, vertical_walls, horizontal_walls
    sets = {}         # Each cell in its own set
    walls = set()     # Set to keep track of walls
    vertical_walls.clear()
    horizontal_walls.clear()
    # Assign each cell to a unique set and add walls
    for x in range(cols):
        for y in range(rows):
            sets[(x, y)] = (x, y)
            if x < cols - 1:
                # Vertical wall between (x, y) and (x+1, y)
                vertical_walls.append(((x, y), (x + 1, y)))
                walls.add(((x, y), (x + 1, y)))
            if y < rows - 1:
                # Horizontal wall between (x, y) and (x, y+1)
                horizontal_walls.append(((x, y), (x, y + 1)))
                walls.add(((x, y), (x, y + 1)))

def find(cell):
    # Path compression for efficiency
    if sets[cell] != cell:
        sets[cell] = find(sets[cell])
    return sets[cell]

def union(cell1, cell2):
    root1 = find(cell1)
    root2 = find(cell2)
    if root1 != root2:
        sets[root2] = root1
        return True
    return False

def generate_maze_kruskal():
    initialize_maze()
    wall_list = vertical_walls + horizontal_walls
    random.shuffle(wall_list)
    for wall in wall_list:
        cell1, cell2 = wall
        if union(cell1, cell2):
            # Remove the wall between cell1 and cell2
            walls.remove(wall)

def draw_maze():
    screen.fill(WHITE)
    # Draw vertical walls
    for wall in vertical_walls:
        if wall in walls:
            (x1, y1), (x2, y2) = wall
            x = max(x1, x2)
            y = y1
            pygame.draw.line(
                screen, BLACK,
                (x * CELL_SIZE, y * CELL_SIZE),
                (x * CELL_SIZE, (y + 1) * CELL_SIZE),
                2
            )
    # Draw horizontal walls
    for wall in horizontal_walls:
        if wall in walls:
            (x1, y1), (x2, y2) = wall
            x = x1
            y = max(y1, y2)
            pygame.draw.line(
                screen, BLACK,
                (x * CELL_SIZE, y * CELL_SIZE),
                ((x + 1) * CELL_SIZE, y * CELL_SIZE),
                2
            )
    # Draw the outer borders
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)

def main():
    generate_maze_kruskal()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze()

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()