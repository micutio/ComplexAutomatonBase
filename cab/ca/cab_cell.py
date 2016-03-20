"""
This module contains all classes associated with the CA cells.
"""

__author__ = 'Michael Wagner'

import math


class CACell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """
    def __init__(self, x, y, gc):
        self.x = x
        self.y = y
        self.gc = gc
        self.neighbors = []
        self.rectangular = True
        self.is_border = False

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def sense_neighborhood(self):
        raise NotImplementedError("Method needs to be implemented")

    def update(self):
        raise NotImplementedError("Method needs to be implemented")

    def clone(self, x, y):
        return CACell(x, y, self.gc)

class CellRect(CACell):
    """
    This class extends the basic CACell class with methods for rectangular cells.
    """
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)
        self.w = gc.CELL_SIZE
        self.h = gc.CELL_SIZE
        
    def get_corners(self):
        corners = []
        corners.append((self.x * self.w, self.y * self.h))
        corners.append((self.x * self.w + self.w, self.y * self.h))
        corners.append((self.x * self.w + self.w, self.y * self.h + self.h))
        corners.append((self.x * self.w, self.y * self.h + self.h))
        return corners

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

        #self.directions = [(1, -1,  0), (1,  0, -1), ( 0, 1, -1), (-1, 1,  0), (-1,  0, 1), ( 0, -1, 1)]

        self.corners = []
        self.corners = self.get_corners()

    def get_corners(self):
        corners = []
        for i in range(6):
            angle = 2 * math.pi / 6 * (i + 0.5)
            
            x = (self.x * self.horiz) + self.c_size * math.cos(angle)
            offset = self.y * (self.horiz / 2)

            y = (self.y * self.vert) + self.c_size * math.sin(angle)
            # offset = 1
            # print('x = {0}, y = {1}, offset = {2}'.format(x, y, offset))
            # corners.append((x + offset, y))
            corners.append((int(x) + int(offset), int(y)))
        return corners

    def get_cube(self):
        return self.x, self.y, self.z

    def distance_to(neighbor):
        x1, y1, z1 = self.get_cube()
        x2, y2, z2 = neighbor.get_cube()
        return max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))
