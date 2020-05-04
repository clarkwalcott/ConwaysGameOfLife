import pickle
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

# Rules for Conway's Game of Life
# 1. Any live cell with two or three live neighbors survives.
# 2. Any dead cell with three live neighbors becomes a live cell.
# 3. All other live cells die in the next generation (by under or overpopulation). Similarly, all other dead cells stay dead.

# A cell and its neighbors can be represented as a 3x3 grid with the cell in the center
def conway():
    board = np.array([[1,0,1,0,0,0,0,0],
                      [0,1,1,0,0,0,0,0],
                      [0,1,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0]])
                      
    mask = np.array([[1,1,1],[1,9,1],[1,1,1]])
    board = load_board("small_exploder.cw")
    check_rules = np.vectorize(rules)

    check = 1
    count = 0
    rule = board.copy()
    plt.show()
    while(True):
        sums = ndimage.convolve(rule, mask, mode='constant', cval=0.0)      # Computes the sum of every cell's neighbors
        rule = check_rules(sums-9)
        plt.imshow(rule)
        plt.pause(0.05)
        plt.ion()
        sum(sums.flatten())

def rules(a):
    if a == -6:             # if a dead cell has exactly 3 neighbors
        return 1            # it becomes alive
    elif a < 0:             # otherwise if a cell is dead, it remains dead
        return 0
    elif a > 1 and a < 4:   # if a cell is alive and has 2 or 3 live neighbors, it survives
        return 1
    else:                   # otherwise the live cell dies
        return 0

# Loads the board state from a file and returns the board object
def load_board(filename):
    with open(filename, 'rb') as f:
        board = pickle.load(f)
    return board

# Saves the board state to a file
def save_board(filename, board):
    with open(filename, 'wb') as f:
        pickle.dump(board, f)

try:
    conway()
except Exception as ex:
    exit()