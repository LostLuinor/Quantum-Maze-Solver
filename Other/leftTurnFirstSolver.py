import pygame
import random
import sys
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 10  # Size of each cell in the maze

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MazeGen_QuantumMazeSolver')

# Frame rate control
clock = pygame.time.Clock()

# Number of rows and columns in the maze
cols = SCREEN_WIDTH // CELL_SIZE
rows = SCREEN_HEIGHT // CELL_SIZE

# Maze grid (initialized with walls)
maze = [[1 for _ in range(cols)] for _ in range(rows)]

# Directions for DFS: right, down, left, up (in terms of grid movement)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Draw the maze
def draw_maze():
    for y in range(rows):
        for x in range(cols):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Player agent with proper DFS backtracking
class Player(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.stack = [pos]  # Stack for DFS backtracking
        self.visited = {pos}  # Set of visited positions
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.goal_reached = False

    def step(self):
        if self.goal_reached:
            return

        # Check if we reached the goal
        goal_pos = (cols - 3, rows - 3)
        if self.pos == goal_pos:
            self.goal_reached = True
            print("Goal reached by agent", self.unique_id)
            print("Path taken:", self.stack)
            return

        # Get possible steps
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)

        # Filter steps
        valid_steps = [
            p for p in possible_steps
            if maze[p[1]][p[0]] == 0 and p not in self.visited
        ]

        if valid_steps:
            # Move to the first valid step
            new_pos = valid_steps[0]
            self.stack.append(new_pos)  # Add to stack
            self.visited.add(new_pos)  # Mark as visited
            self.model.grid.move_agent(self, new_pos)
        else:
            # Backtrack if no valid steps
            if len(self.stack) > 1:
                self.stack.pop()  # Remove current position from stack
                new_pos = self.stack[-1]  # Move to previous position
                self.model.grid.move_agent(self, new_pos)

# Maze model
class MazeModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.current_id = 0  # Initialize current_id for generating unique agent IDs

        # Create initial player agent
        a = Player(self.next_id(), self, (1, 1))
        self.schedule.add(a)
        self.grid.place_agent(a, (1, 1))

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def step(self):
        self.schedule.step()

# Recursive DFS function to generate the maze
def generate_maze(x, y):
    maze[y][x] = 0  # Mark the cell as a path
    random.shuffle(DIRECTIONS)  # Randomize direction
    
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx * 2, y + dy * 2

        # Check if the new cell is within the inner maze boundaries
        if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[ny][nx] == 1:
            # Knock down the wall between the current cell and the new cell
            maze[y + dy][x + dx] = 0
            # Recursively visit the new cell
            generate_maze(nx, ny)

def add_loops(extra_loops=10):
    for _ in range(extra_loops):
        x = random.randint(1, cols - 2)
        y = random.randint(1, rows - 2)

        # Only knock down a wall if it exists
        if maze[y][x] == 1:
            maze[y][x] = 0

# Start maze generation from the top-left corner (1,1)
generate_maze(1, 1)
add_loops(extra_loops=50)

# Function to draw the player
def draw_player(player, color):
    pygame.draw.rect(screen, color, (player.pos[0] * CELL_SIZE, player.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the exit
def draw_exit():
    pygame.draw.rect(screen, RED, ((cols - 3) * CELL_SIZE, (rows - 3) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main game loop
def main():
    model = MazeModel(cols, rows)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Fill the screen with black background
        screen.fill(BLACK)

        # Draw the maze and the exit
        draw_maze()
        draw_exit()

        # Step the model
        model.step()
        
        # Draw the player
        for agent in model.schedule.agents:
            # for pos in agent.visited:
                # pygame.draw.rect(screen, BLUE, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for pos in agent.stack:
                pygame.draw.rect(screen, BLUE, (pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            draw_player(agent, GREEN)
            

        pygame.display.flip()

        # Limit the frame rate
        clock.tick(15)

if __name__ == "__main__":
    main()
