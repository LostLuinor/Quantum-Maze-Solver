import random
import matplotlib.pyplot as plt

# Maze dimensions
rows, cols = 21, 21  # Odd numbers to ensure walls around the maze

# Initialize the maze with walls (1)
maze = [[1 for _ in range(cols)] for _ in range(rows)]

# DFS Algorithm to generate the maze
def generate_maze(x, y):
    maze[x][y] = 0  # Mark the current cell as a path
    
    # Define possible directions (up, right, down, left)
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)  # Shuffle directions for randomness
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        
        # Check if the next cell is within the grid and is a wall
        if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and maze[nx][ny] == 1:
            maze[(x + nx) // 2][(y + ny) // 2] = 0  # Remove the wall between the current cell and next
            generate_maze(nx, ny)  # Recursively visit the next cell

# Start the maze generation at (1,1)
generate_maze(1, 1)

# Function to visualize the maze using matplotlib
def plot_maze():
    plt.figure(figsize=(10, 10))
    plt.imshow(maze, cmap='binary')
    plt.xticks([])  # Remove x-axis ticks
    plt.yticks([])  # Remove y-axis ticks
    plt.show()

# Visualize the generated maze
plot_maze()
plot_maze()
plot_maze()
