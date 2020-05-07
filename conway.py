import pickle
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from PIL import Image
import time

# RIP John Conway 1937-2020

# Rules for Conway's Game of Life
# 1. Any live cell with two or three live neighbors survives.
# 2. Any dead cell with three live neighbors becomes a live cell.
# 3. All other live cells die in the next generation (by under or overpopulation). Similarly, all other dead cells stay dead.

# A cell and its neighbors can be represented as a 3x3 grid with the cell in the center

def conway(bd):
    b = np.asarray(bd, dtype=np.int64)[::step_size, ::step_size]
    board = b//255
    # board = np.array([[0,0,0,0,0,0,0,0],
    #                   [0,1,0,0,0,0,0,0],
    #                   [0,1,0,0,0,0,0,0],
    #                   [0,1,0,0,0,0,0,0],
    #                   [0,0,0,0,0,0,0,0],
    #                   [0,0,0,0,0,0,0,0],
    #                   [0,0,0,0,0,0,0,0],
    #                   [0,0,0,0,0,0,0,0]])

    mask = np.array([[1,1,1],[1,9,1],[1,1,1]])
    check_rules = np.vectorize(rules)
    rule = board.copy()
    plt.show()
    while(True):
        sums = ndimage.convolve(rule, mask, mode='constant', cval=0.0)      # Computes the sum of every cell's neighbors
        rule = check_rules(sums-9)
        plt.imshow(rule)
        plt.pause(0.05)
        plt.ion()
        sum(sums.flatten())

def add_cell(x, y):
    global step_size 
    
    # Locks each cell to the grid
    x = (x//step_size)*step_size
    y = (y//step_size)*step_size

    # picks out the region that we want to color
    box = (x, y, x+step_size, y+step_size)
    try:
        # crops out the region using the box coordinates and loads the intensity values of the pixels
        region = img.crop(box)
        pixels = region.load()
        for i in range(step_size):
            for j in range(step_size):
                pixels[i, j] = 255          # sets the pixels in the region to white
        
        # puts the altered pixels back into the image
        img.paste(region, box)
        img.save("board.png")
        # displays the new image with the flipped pixel
        plt.imshow(img)
        plt.show()
    except Exception as ex:
        print(ex)

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

def onclick(event):
    try:
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
        add_cell(int(event.xdata), int(event.ydata))
        
    except:
        pass

try:
    global img, step_size
    step_size= 10
    fig, ax = plt.subplots()
    # plt.savefig("output.png")
    img = Image.new('L', (400,400), "black")
    plt.imshow(img)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    conway(img)
except Exception as ex:
    print(ex)
    plt.close()
    exit()