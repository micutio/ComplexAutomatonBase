"""
This module contains all classes associated with the CA cells.
"""

# External library imports
import math
from abc import ABCMeta, abstractmethod


__author__ = 'Michael Wagner'


class CACell(metaclass=ABCMeta):
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """
    def __init__(self, x, y, gc):
        self.x = x
        self.y = y
        self.gc = gc
        self.neighbors = []
        self.corners = []
        self.rectangular = True
        self.is_border = False
        self.color = gc.DEFAULT_CELL_COLOR

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def set_corners(self):
        pass

    def get_corners(self):
        return self.corners

    @abstractmethod
    def sense_neighborhood(self):
        raise NotImplementedError("Method needs to be implemented")

    @abstractmethod
    def update(self):
        raise NotImplementedError("Method needs to be implemented")

    @abstractmethod
    def clone(self, x, y):
        return CACell(x, y, self.gc)

    def on_lmb_click(self):
        """
        Executed when the mouse is pointed at the cell and left clicked.
        To be implemented by the gui class.
        """
        pass

    def on_rmb_click(self):
        """
        Executed when the mouse is pointed at the cell and right clicked.
        To be implemented by the gui class.
        """
        pass

    def on_mouse_scroll_up(self):
        """
        Executed when the mouse is pointed at the cell and wheel scrolled up.
        """
        pass

    def on_mouse_scroll_down(self):
        """
        Executed when the mouse is pointed at the cell and wheel scrolled down.
        """
        pass


class CellRect(CACell):
    """
    This class extends the basic CACell class with methods for rectangular cells.
    """

    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.w = gc.CELL_SIZE
        self.h = gc.CELL_SIZE
        self.set_corners()
        
    def set_corners(self):
        self.corners = []
        self.corners.append((self.x * self.w, self.y * self.h))
        self.corners.append((self.x * self.w + self.w, self.y * self.h))
        self.corners.append((self.x * self.w + self.w, self.y * self.h + self.h))
        self.corners.append((self.x * self.w, self.y * self.h + self.h))

    def clone(self, x, y):
        pass

    def update(self):
        pass

    def sense_neighborhood(self):
        pass


class CellHex(CACell):
    """
    This class extends the basic CACell class with methods for hexagonal cells.

    """

    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.h = gc.CELL_SIZE * 2
        self.vert = self.h * (3 / 4)
        self.w = self.h * (math.sqrt(3) / 2)     
        self.horiz = self.w
        self.q = x
        self.r = y
        self.z = -self.q - self.r
        self.rectangular = False
        self.c_size = gc.CELL_SIZE

        # self.directions = [(1, -1,  0), (1,  0, -1), ( 0, 1, -1), (-1, 1,  0), (-1,  0, 1), ( 0, -1, 1)]

        self.corners = []
        self.set_corners()

    def set_corners(self):
        self.corners = []
        for i in range(6):
            angle = 2 * math.pi / 6 * (i + 0.5)
            
            x = (self.x * self.horiz) + self.c_size * math.cos(angle)
            offset = self.y * (self.horiz / 2)

            y = (self.y * self.vert) + self.c_size * math.sin(angle)
            # offset = 1
            # print('x = {0}, y = {1}, offset = {2}'.format(x, y, offset))
            # corners.append((x + offset, y))
            self.corners.append((int(x) + int(offset), int(y)))

    def get_cube(self):
        return self.x, self.y, self.z

    def distance_to(self, neighbor):
        x1, y1, z1 = self.get_cube()
        x2, y2, z2 = neighbor.get_cube()
        return max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))

    def clone(self, x, y):
        pass

    def update(self):
        pass

    def sense_neighborhood(self):
        pass
