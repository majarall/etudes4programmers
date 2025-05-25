import numpy as np 
from scipy.ndimage import convolve
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



# Program to explorte game of life by Conway.
# Estimated time 3 weeks. 


# What are the rules LIFE?

# 1. The immediate neighbors of a cell are those cells occupying the eight horizontally,
# vertically, and diagonally adjacent cells.
# 2. If a LIFE cell has fewer than two immediate neighbors, it dies of loneliness. If a LIFE
# cell has more than three immediate neighbors, it dies of overcrowding.
# 3. If an empty square has exactly three LIFE cells as immediate neighbors, a new cell is
# born in the square.
# 4. Births and deaths all take place exactly at the change of generations. Thus a dying cell
# may help birth a new one, but a newborn cell may not resurrect a dying cell, nor may one
# dying cell stave off death for another by lowering the local population density.


# Pseudo program

# 1. Print 2d grid of the Flatland. Does the size matter here? 10x10 or 100x100?
# Start by a numpy array 10x10


def get_grid(x,y):
	""" retunrs a square 2d array of size x*y"""

	return np.zeros((x,y), dtype=int)

# 2. Randomly distribute a configuration of living cells. 
# choose a number of living cells to begin with, change this number according to the behvior of LIFE. 
def initial_state(A, initial_lives):
	"""Create random positions of living cells (1s), and distribute them to array A"""
	positions = np.random.choice(A.size, initial_lives, replace=False)
	np.put(A, positions, 1)
	return A


# Checks:
# 1. If LIFE cell < 2 neigbors then cell = dead. If LIFE cell > 3 neighbors then cell = dead.
# IF empty cell == 3 neighbors LIFE cell then LIFE cell


def apply_rules(A):
    """
    Apply Conway's Game of Life rules to the grid:
    1. Any live cell with fewer than two live neighbors dies (underpopulation)
    2. Any live cell with two or three live neighbors lives on
    3. Any live cell with more than three live neighbors dies (overpopulation)
    4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction)
    
    Args:
        A : 2D numpy array representing the current state
        
    Returns:
        The updated grid after applying the rules
    """
    # 3x3 kernel with center zero (so it doesn't count the cell itself)
    kernel = np.array([[1, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1]])
    
    # Count neighbors for each cell
    neighbor_counts = convolve(A, kernel, mode='constant', cval=0)
    
    # Create a copy of the grid to avoid modifying it during rule application
    new_A = A.copy()
    
    # Apply rules
    # Rule 1 & 3: Live cells with < 2 or > 3 neighbors die
    live_cells = A == 1
    over_population = neighbor_counts > 3
    under_population = neighbor_counts < 2
    mask_rule_1_and_3 = live_cells & (under_population | over_population)  
    new_A[mask_rule_1_and_3] = 0
    # Rule 4: Dead cells with exactly 3 neighbors become alive
    dead_cell = A == 0
    reproduction = neighbor_counts == 3
    mask_rule_4 = dead_cell & reproduction
    new_A[mask_rule_4] = 1
    
    return new_A

def enhanced_animation(initial_grid, num_generations=50, interval=200):
    # Setup the figure and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Conway's Game of Life", fontsize=16)
    
    # Main grid display
    img = ax1.imshow(initial_grid, cmap='viridis', interpolation='nearest')
    ax1.set_title("Grid")
    ax1.grid(True, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
    
    # Stats tracking
    generations = [0]
    live_cells = [np.sum(initial_grid)]
    line, = ax2.plot(generations, live_cells, 'r-')
    ax2.set_xlim(0, num_generations)
    ax2.set_ylim(0, initial_grid.size)
    ax2.set_title("Population over time")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Live cells")
    ax2.grid(True)
    
    # Animation state
    grid = initial_grid.copy()
    
    def update(frame):
        nonlocal grid
        # Update grid
        grid = apply_rules(grid)
        
        # Update grid display
        img.set_array(grid)
        
        # Update statistics
        generations.append(frame + 1)
        population = np.sum(grid)
        live_cells.append(population)
        line.set_data(generations, live_cells)
        
        # Update titles
        ax1.set_title(f"Generation {frame + 1}")
        
        return [img, line]
    
    ani = FuncAnimation(
        fig, 
        update, 
        frames=num_generations,
        interval=interval,
        blit=False
    )
    
    plt.tight_layout()
    plt.show()
    return ani, fig


x = y = 20
initial_lives = 40
grid = get_grid(x,y)
initial_grid = initial_state(grid, initial_lives)  
enhanced_animation(initial_grid)

"""
fig, ax = plt.subplots(figsize=(8, 8))
img = ax.imshow(A, cmap='hot', interpolation='nearest')
fig.colorbar(img, label='Value')  # Create colorbar AFTER creating the image
title = ax.set_title("Iteration 0")

# Animation update function
def update(frame):
    global A
    
    # Apply Game of Life rules to update the grid
    A = apply_rules(A)
    
    # Update the image data instead of creating a new plot
    img.set_array(A)
    plt.title(f"Iteration {frame+1}")
    #title.set_text(f"Iteration {frame+1}")
    return [img, title]

# Create the animation
num_generations = 10  # Your original number
ani = FuncAnimation(
    fig, 
    update, 
    frames=num_generations,
    interval=500,  # milliseconds between frames
    blit=True
)
plt.tight_layout()
plt.show()

"""


# TODOS next time:

# 1. Fix the title issue when plotting, the problem apears to be that the first iteration 0 is overlapping with other iterations
# 2. Add all the rules properly.
# 3. Refactor the code, make a function of the rules
# 4. validate that the game is working properly

