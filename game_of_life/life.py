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

import numpy as np 
X, Y = 10, 10
A = np.zeros((X,Y), dtype=int)
print(A)
# 2. Randomly distribute a configuration of living cells. 
# choose a number of living cells to begin with, change this number according to the behvior of LIFE. 
initial_lives = 30
positions = np.random.choice(A.size, initial_lives, replace=False)
np.put(A, positions, 1)
print(A)

# Checks:
# 1. If LIFE cell < 2 neigbors then cell = dead. If LIFE cell > 3 neighbors then cell = dead.
# IF empty cell == 3 neighbors LIFE cell then LIFE cell

#
#		0	
#	0	0	0		
#		0
#
#



from scipy.ndimage import convolve


# 3x3 kernel with center zero (so it doesn't count the cell itself)
kernel = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])



import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#plt.imshow(np.zeros((10, 10)), cmap='hot', interpolation='nearest', vmin=0, vmax=1)

fig, ax = plt.subplots(figsize=(8, 8))
img = ax.imshow(A, cmap='hot', interpolation='nearest')
fig.colorbar(img, label='Value')  # Create colorbar AFTER creating the image
title = ax.set_title("Iteration 0")

# Animation update function
def update(frame):
    global A
    
    # Your existing code for updating the grid
    neighbor_counts = convolve(A, kernel, mode='constant', cval=0)
    mask_dead = neighbor_counts > 3
    mask_life = neighbor_counts == 3
    A[mask_dead] = 0
    A[mask_life] = 1
    
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

plt.show()


"""
num_generations = 5
for gen in range(num_generations):

	# Convolve to get neighbor counts for all cells
	neighbor_counts = convolve(A, kernel, mode='constant', cval=0)


	mask_dead = neighbor_counts > 3
	mask_life = neighbor_counts == 3
	A[mask_dead] = 0
	A[mask_life] = 1


	# Step 4: Display as heatmap
	plt.figure(figsize=(8,8))
	plt.title(f"Iteration {gen+1}")
	plt.imshow(A, cmap='hot', interpolation='nearest')
	plt.colorbar(label='Value')
	plt.show()
"""
