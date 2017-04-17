"""
This module contains a CAB io implementation in TkInter.
"""

# External library imports.
from tkinter import Tk, Canvas
import math

# Internal Simulation System component imports.
from cab_global_constants import GlobalConstants

__author__ = 'Michael Wagner'


class TkIO:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, cab_core):
        self.root = Tk()
        self.gc = gc
        self.core = cab_core
        self.width = 0
        self.height = 0
        self.root.title("Complex Automaton")
        self.canvas = None
        self.cells = {}

        self.init_canvas()
        self.init_cells()

    def init_canvas(self):
        if self.gc.USE_HEX_CA:
            self.width = int((math.sqrt(3) / 2) * (self.gc.CELL_SIZE * 2) * (self.gc.DIM_X - 1))
            self.height = int((3 / 4) * (self.gc.CELL_SIZE * 2) * (self.gc.DIM_Y - 1))
            # print(offset)
            # screen = pygame.display.set_mode((self.gc.GRID_WIDTH, self.gc.GRID_HEIGHT), pygame.RESIZABLE, 32)
        else:
            self.width = self.gc.CELL_SIZE * self.gc.DIM_X
            self.height = self.gc.CELL_SIZE * self.gc.DIM_Y

        col = '#%02x%02x%02x' % self.gc.DEFAULT_CELL_COLOR
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg=col)
        self.canvas.pack()

    def init_cells(self):
        for k, v in list(self.core.ca.ca_grid.items()):
            corners_list = [i for tupl in v.get_corners() for i in tupl]
            col_f = '#%02x%02x%02x' % v.color
            col_o = '#%02x%02x%02x' % (0, 0, 0)
            self.cells[k] = self.canvas.create_polygon(corners_list, fill=col_f, outline=col_o)

    def render_frame(self):
        """Draws a new frame every N milliseconds"""
        if self.gc.RUN_SIMULATION:
            self.core.step_simulation()
        self.root.after(0, self.render_frame)

    def render_simulation(self):
        self.root.mainloop()
