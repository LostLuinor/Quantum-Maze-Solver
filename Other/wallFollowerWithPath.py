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
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Color for the player's path

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
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

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

# Player start position
player_x, player_y = 1, 1

# Exit point
exit_x, exit_y = cols - 2, rows - 2

# Player's initial direction (facing right)
direction = 0  # 0: right, 1: down, 2: left, 3: up

# List to store the player's path
player_path = [(player_x, player_y)]

# Wall Follower movement functions
def turn_left():
    global direction
    direction = (direction - 1) % 4

def turn_right():
    global direction
    direction = (direction + 1) % 4

def move_forward():
    global player_x, player_y
    dx, dy = DIRECTIONS[direction]
    new_x, new_y = player_x + dx, player_y + dy
    # Only move if there's no wall
    if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_x][new_y] == 0:
        player_x, player_y = new_x, new_y

# Check for wall in a specified direction
def is_wall(direction_offset):
    check_direction = (direction + direction_offset) % 4
    dx, dy = DIRECTIONS[check_direction]
    check_x, check_y = player_x + dx, player_y + dy
    return not (0 <= check_x < cols and 0 <= check_y < rows and maze[check_x][check_y] == 0)

# Function to draw the maze
def draw_maze():
    for x in range(cols):
        for y in range(rows):
            color = WHITE if maze[x][y] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the player
def draw_player():
    pygame.draw.rect(screen, GREEN, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the player's path
def draw_path():
    for pos in player_path:
        pygame.draw.rect(screen, BLUE, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the exit
def draw_exit():
    pygame.draw.rect(screen, RED, (exit_x * CELL_SIZE, exit_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Wall-follower solver function
def wall_follower():
    global player_x, player_y, direction
    if not is_wall(-1):  # Check left
        turn_left()
        move_forward()
    elif not is_wall(0):  # Check ahead
        move_forward()
    else:
        turn_right()
        if not is_wall(0):  # Check ahead again after turning right
            move_forward()
        else:
            turn_right()  # Turn right again if still blocked

    # Add the new position to the player's path
    player_path.append((player_x, player_y))

# Update the game loop to use the wall-follower solver
def main():
    global player_x, player_y
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Solve the maze step by step
        if (player_x, player_y) != (exit_x, exit_y):
            wall_follower()
        else:
            display_message("Solved!")

        # Fill the screen
        screen.fill(BLACK)

        # Draw the maze
        draw_maze()

        # Draw the player's path
        draw_path()

        # Draw the player
        draw_player()

        # Draw the exit
        draw_exit()

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(10)

# Function to display a message
def display_message(message):
    font = pygame.font.SysFont(None, 55)
    text = font.render(message, True, (0, 255, 0))
    screen.blit(text, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == "__main__":
    main()