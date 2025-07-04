import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 50  # Size of each cell in the maze

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze Solver')

# Frame rate control
clock = pygame.time.Clock()

# Number of rows and columns in the maze
cols = SCREEN_WIDTH // CELL_SIZE
rows = SCREEN_HEIGHT // CELL_SIZE

# Maze grid (initialized with walls)
maze = [[1 for _ in range(cols)] for _ in range(rows)]

# Directions for DFS: right, down, left, up (in terms of grid movement)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up
direction_index = 0  # Start facing "right" direction

# Recursive DFS function to generate the maze
def generate_maze(x, y):
    maze[x][y] = 0  # Mark the cell as a path
    random.shuffle(DIRECTIONS)  # Randomize direction

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx * 2, y + dy * 2

        # Ensure the new cell is inside the maze boundaries
        if 0 <= nx < cols and 0 <= ny < rows and maze[nx][ny] == 1:
            # Knock down the wall between the current cell and the new cell
            maze[x + dx][y + dy] = 0
            # Recursively visit the new cell
            generate_maze(nx, ny)

# Start maze generation from the top-left corner (1,1)
generate_maze(1, 1)

# Function to draw the maze
def draw_maze():
    for x in range(cols):
        for y in range(rows):
            color = WHITE if maze[x][y] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Player start position
player_x, player_y = 1, 1

# Exit point
exit_x, exit_y = cols - 1, rows - 1

# Function to draw the player
def draw_player():
    pygame.draw.rect(screen, (0, 255, 0), (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the exit
def draw_exit():
    pygame.draw.rect(screen, (255, 0, 0), (exit_x * CELL_SIZE, exit_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Check if a position is within the maze and is a path (0)
def is_path(x, y):
    return 0 <= x < cols and 0 <= y < rows and maze[x][y] == 0

# Wall follower algorithm
def wall_follower_solve():
    global player_x, player_y, direction_index

    # Order of directions relative to the current direction
    left_turn = (direction_index - 1) % 4
    right_turn = (direction_index + 1) % 4
    back_turn = (direction_index + 2) % 4

    # Determine the coordinates of the possible moves
    left_x, left_y = player_x + DIRECTIONS[left_turn][0], player_y + DIRECTIONS[left_turn][1]
    forward_x, forward_y = player_x + DIRECTIONS[direction_index][0], player_y + DIRECTIONS[direction_index][1]
    right_x, right_y = player_x + DIRECTIONS[right_turn][0], player_y + DIRECTIONS[right_turn][1]

    # Check for possible moves in the wall-follower order (left, forward, right, back)
    if is_path(left_x, left_y):
        # Turn left
        player_x, player_y = left_x, left_y
        direction_index = left_turn
    elif is_path(forward_x, forward_y):
        # Move forward
        player_x, player_y = forward_x, forward_y
    elif is_path(right_x, right_y):
        # Turn right
        player_x, player_y = right_x, right_y
        direction_index = right_turn
    else:
        # Turn back if no other options
        player_x, player_y = player_x + DIRECTIONS[back_turn][0], player_y + DIRECTIONS[back_turn][1]
        direction_index = back_turn

# Update the game loop to include the wall follower algorithm
def main():
    global player_x, player_y
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Solve the maze using the wall follower algorithm
        wall_follower_solve()

        # Check if the player has reached the exit
        if player_x == exit_x and player_y == exit_y:
            running = False

        # Fill the screen
        screen.fill(BLACK)

        # Draw the maze
        draw_maze()

        # Draw the player
        draw_player()

        # Draw the exit
        draw_exit()

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(10)

if __name__ == "__main__":
    main()
