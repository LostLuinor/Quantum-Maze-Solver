import pygame
import random
import sys
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800  # Increased width to accommodate buttons
SCREEN_HEIGHT = 650
CELL_SIZE = 10  # Size of each cell in the maze

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGREY = (200, 200, 200)
DARKGREY = (150, 150, 150)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MazeGen_CombinedSolver')

# Frame rate control
clock = pygame.time.Clock()

# Number of rows and columns in the maze
cols = (SCREEN_WIDTH - 200) // CELL_SIZE
rows = (SCREEN_HEIGHT - 50) // CELL_SIZE

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

# Quantum Maze Solver Player agent
class QuantumPlayer(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.visited = [pos]
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def step(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        possible_steps = [p for p in possible_steps if maze[p[1]][p[0]] == 0 and self.model.grid.is_cell_empty(p) and p not in self.visited]

        if possible_steps:
            if len(possible_steps) > 1:
                for step in possible_steps:
                    new_agent = QuantumPlayer(self.model.next_id(), self.model, step)
                    self.model.schedule.add(new_agent)
                    self.model.grid.place_agent(new_agent, step)
                    new_agent.visited = self.visited + [step]
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            else:
                new_pos = possible_steps[0]
                self.model.grid.move_agent(self, new_pos)
                self.visited.append(new_pos)

# Left Turn First Solver Player agent
class LeftTurnPlayer(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.stack = [pos]
        self.visited = {pos}
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.goal_reached = False

    def step(self):
        if self.goal_reached:
            return

        goal_pos = (cols - 3, rows - 3)
        if self.pos == goal_pos:
            self.goal_reached = True
            print("Goal reached by agent", self.unique_id)
            print("Path taken:", self.stack)
            return

        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        valid_steps = [p for p in possible_steps if maze[p[1]][p[0]] == 0 and p not in self.visited]

        if valid_steps:
            new_pos = valid_steps[0]
            self.stack.append(new_pos)
            self.visited.add(new_pos)
            self.model.grid.move_agent(self, new_pos)
        else:
            if len(self.stack) > 1:
                self.stack.pop()
                new_pos = self.stack[-1]
                self.model.grid.move_agent(self, new_pos)

# Maze model
class MazeModel(Model):
    def __init__(self, width, height, agent_type):
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.current_id = 0
        self.agent_type = agent_type

        a = self.agent_type(self.next_id(), self, (1, 1))
        self.schedule.add(a)
        self.grid.place_agent(a, (1, 1))

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def step(self):
        self.schedule.step()

# Recursive DFS function to generate the maze
def generate_maze(x, y):
    maze[y][x] = 0
    random.shuffle(DIRECTIONS)
    
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx * 2, y + dy * 2
        if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[ny][nx] == 1:
            maze[y + dy][x + dx] = 0
            generate_maze(nx, ny)

def add_loops(extra_loops=10):
    for _ in range(extra_loops):
        x = random.randint(1, cols - 2)
        y = random.randint(1, rows - 2)
        if maze[y][x] == 1:
            maze[y][x] = 0

generate_maze(1, 1)
add_loops(extra_loops=50)

# Function to draw the player
def draw_player(player, color):
    pygame.draw.rect(screen, color, (player.pos[0] * CELL_SIZE, player.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw the exit
def draw_exit():
    pygame.draw.rect(screen, RED, ((cols - 3) * CELL_SIZE, (rows - 3) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw buttons
def draw_button(text, x, y, w, h, active):
    color = DARKGREY if active else LIGHTGREY
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)

# Function to draw the timer
def draw_timer(time_elapsed):
    font = pygame.font.Font(None, 36)
    text_surf = font.render(f"Time: {time_elapsed:.2f} s", True, WHITE)
    screen.blit(text_surf, (10, SCREEN_HEIGHT - 40))

# Main game loop
def main():
    agent_type = QuantumPlayer
    model = MazeModel(cols, rows, agent_type)
    running = True
    game_over = False
    start_time = pygame.time.get_ticks()
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        button1_active = 610 <= mouse_pos[0] <= 760 and 50 <= mouse_pos[1] <= 100
        button2_active = 610 <= mouse_pos[0] <= 760 and 150 <= mouse_pos[1] <= 200

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_active:
                    agent_type = QuantumPlayer
                    model = MazeModel(cols, rows, agent_type)
                    game_over = False
                    start_time = pygame.time.get_ticks()
                elif button2_active:
                    agent_type = LeftTurnPlayer
                    model = MazeModel(cols, rows, agent_type)
                    game_over = False
                    start_time = pygame.time.get_ticks()

        if not game_over:
            screen.fill(BLACK)
            draw_maze()
            draw_exit()
            model.step()
        
            for agent in model.schedule.agents:
                draw_player(agent, GREEN)

            if any(agent.pos == (cols - 3, rows - 3) for agent in model.schedule.agents):
                game_over = True
                print("Goal reached!")

        time_elapsed = (pygame.time.get_ticks() - start_time) / 1000
        draw_button("Solver 1", 610, 50, 150, 50, button1_active)
        draw_button("Solver 2", 610, 150, 150, 50, button2_active)
        draw_timer(time_elapsed)

        pygame.display.flip()
        clock.tick(15)

if __name__ == "__main__":
    main()
