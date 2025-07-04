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
CELL_SIZE = 20  # Size of each cell in the maze

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

def draw_player(player):
    pygame.draw.rect(screen, GREEN, (player.pos[0] * CELL_SIZE, player.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Player agent
class Player(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.visited = [pos]

    def step(self):
        # Get possible steps
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        
        # Filter out steps that lead to walls or are occupied by other agents
        possible_steps = [p for p in possible_steps if maze[p[1]][p[0]] == 0 and self.model.grid.is_cell_empty(p) and p not in self.visited]

        if possible_steps:
            if len(possible_steps) > 1:
                # Split into multiple agents if there are multiple paths
                for step in possible_steps:
                    new_agent = Player(self.model.next_id(), self.model, step)
                    self.model.schedule.add(new_agent)
                    self.model.grid.place_agent(new_agent, step)
                    new_agent.visited = self.visited + [step]
            else:
                # Move to the single valid step
                new_pos = possible_steps[0]
                self.model.grid.move_agent(self, new_pos)
                self.visited.append(new_pos)

# Maze model
class MazeModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.shared_path = [(1, 1)]  # Shared path for all agents
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

# Function to check if any agent has reached the goal
def check_goal(model):
    goal_pos = (cols - 2, rows - 2)
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
    generate_maze(1, 1, loop_prob=0.1)  # Generate maze with loops
    add_loops(extra_loops=20)  # Add extra loops

    model = MazeModel(cols, rows)
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
            draw_start_and_end()

            # Step the model
            model.step()

            # Draw the players
            for agent in model.schedule.agents:
                draw_player(agent)

            # Check if any agent has reached the goal
            if check_goal(model):
                game_over = True
                print("Goal reached!")

        pygame.display.flip()

        # Limit the frame rate
        clock.tick(10)

if __name__ == "__main__":
    main()