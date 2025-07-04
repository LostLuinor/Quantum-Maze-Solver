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

# Ensure there's a path to the goal
maze[rows - 6][cols - 5] = 0
maze[rows - 5][cols - 6] = 0

# Directions for DFS: right, down, left, up (in terms of grid movement)
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Draw the maze
def draw_maze():
    for y in range(rows):
        for x in range(cols):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Player agent
class Player(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pos = (1, 1)
        self.visited = []

    def step(self):
        # Get possible steps
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        
        # Filter out steps that lead to walls or are occupied by other agents
        possible_steps = [p for p in possible_steps if maze[p[1]][p[0]] == 0 and self.model.grid.is_cell_empty(p) and p not in self.visited]

        if possible_steps:
            # Move to a random valid step
            new_pos = random.choice(possible_steps)
            self.model.grid.move_agent(self, new_pos)
            self.model.shared_path.append(new_pos)
            self.visited.append(new_pos)

# Maze model
class MazeModel(Model):
    def __init__(self, width, height, num_agents):
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.shared_path = [(1, 1)]  # Shared path for all agents

        # Create player agents
        for i in range(self.num_agents):
            a = Player(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

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

# Start maze generation from the top-left corner (1,1)
generate_maze(1, 1)

# Function to draw the player
def draw_player(player):
    pygame.draw.rect(screen, GREEN, (player.pos[0] * CELL_SIZE, player.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the exit
def draw_exit():
    pygame.draw.rect(screen, RED, ((cols - 3) * CELL_SIZE, (rows - 3) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to check if any agent has reached the goal
def check_goal(model):
    goal_pos = (cols - 3, rows - 3)
    for agent in model.schedule.agents:
        if agent.pos == goal_pos:
            print("Goal reached by agent", agent.unique_id)
            print("Path taken:", agent.visited)
            for p in agent.visited:
                pygame.draw.rect(screen, BLUE, ((p[0]) * CELL_SIZE, (p[1]) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            return True
    return False

# Main game loop
def main():
    num_agents = (rows-2)*(cols-2)//2  # Number of agents
    model = MazeModel(cols, rows, num_agents)
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        if not game_over:
            # Fill the screen with black background
            screen.fill(BLACK)

            # Draw the maze and the start/goal points
            draw_maze()
            draw_exit()

            # Step the model
            model.step()

            # Draw the players
            for agent in model.schedule.agents:
                draw_player(agent)

            # Check if any agent has reached the goal
            # if check_goal(model):
            #     game_over = True
            #     print("Goal reached!")

        pygame.display.flip()

        # Limit the frame rate
        clock.tick(20)

if __name__ == "__main__":
    main()