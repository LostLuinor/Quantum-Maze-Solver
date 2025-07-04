import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 60  # Size of each cell in the maze

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Color for the player's path

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze Generator')

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

# Function to draw the maze
def draw_maze():
    for x in range(cols):
        for y in range(rows):
            color = WHITE if maze[x][y] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Player start position
player_x, player_y = 1, 1

# List to store the player's path
player_path = [(player_x, player_y)]

# Function to draw the player
def draw_player(color):
    pygame.draw.rect(screen, color, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the player's path
def draw_path():
    for pos in player_path:
        pygame.draw.rect(screen, BLUE, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Exit point
exit_x, exit_y = cols - 2, rows - 2

# Function to draw the exit
def draw_exit():
    pygame.draw.rect(screen, RED, (exit_x * CELL_SIZE, exit_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to display a message
def display_message(message):
    font = pygame.font.SysFont(None, 55)
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])
    pygame.display.flip()
    pygame.time.wait(2000)

# Update the game loop to include player movement and goal check
def main():
    global player_x, player_y
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Handle key presses for player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0 and maze[player_x - 1][player_y] == 0:
            player_x -= 1
        if keys[pygame.K_RIGHT] and player_x < cols - 1 and maze[player_x + 1][player_y] == 0:
            player_x += 1
        if keys[pygame.K_UP] and player_y > 0 and maze[player_x][player_y - 1] == 0:
            player_y -= 1
        if keys[pygame.K_DOWN] and player_y < rows - 1 and maze[player_x][player_y + 1] == 0:
            player_y += 1

        # Add the new position to the player's path
        # player_path.append((player_x, player_y))

        # Check if the player has reached the exit
        if player_x == exit_x and player_y == exit_y:
            display_message("You Win!")
            running = False

        # Fill the screen
        screen.fill(BLACK)

        # Draw the maze
        draw_maze()

        # Draw the player's path
        # draw_path()

        # Draw the player
        draw_player(GREEN)

        # Draw the exit
        draw_exit()

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(20)

if __name__ == "__main__":
    main()