from tkinter import Tk, Canvas

import math

from cab_global_constants import GlobalConstants

root = Tk()

root.title("Complex Automaton")

gc = GlobalConstants

if gc.USE_HEX_CA:
    can_width = int((math.sqrt(3) / 2) * (gc.CELL_SIZE * 2) * (gc.DIM_X - 1))
    can_height = int((3 / 4) * (gc.CELL_SIZE * 2) * (gc.DIM_Y - 1))
    # print(offset)
    # screen = pygame.display.set_mode((gc.GRID_WIDTH, gc.GRID_HEIGHT), pygame.RESIZABLE, 32)
else:
    can_width = gc.CELL_SIZE * gc.DIM_X
    can_height = gc.CELL_SIZE * gc.DIM_Y

can = Canvas(root, width=can_width, height=can_height)
can.pack()

root.mainloop()
