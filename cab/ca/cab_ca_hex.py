"""
This module contains the class for a CA with hexagonal cells in pointy top layout.
"""

from cab.ca.cab_cell import CellHex

import math
import random

__author__ = 'Michael Wagner'


class CAHex:
    """
    For reference go to "http://www.redblobgames.com/grids/hexagons/"
    Hex CA parameters:
    - even-r horizontal layout
    - cube coordinates for algorithms
    - axial coordinates for storage
    """

    def __init__(self, gc, visualizer, proto_cell=None):
        """
        Initializes and returns the cellular automaton.
        The CA is a dictionary and not a list of lists
        :return: The initialized CA.
        """
        self.ca_grid = {}
        self.gc = gc
        self.grid_height = gc.GRID_HEIGHT
        self.grid_width = gc.GRID_WIDTH
        self.height = int(self.grid_height / gc.CELL_SIZE)
        self.width = int(self.grid_width / gc.CELL_SIZE)
        self.cell_size = gc.CELL_SIZE
        self.visualizer = visualizer
        self.use_borders = gc.USE_CA_BORDERS
        self.proto_cell = None

        if proto_cell is None:
            for j in range(0, self.height):
                for i in range(0, self.width):
                    # self.ca_grid[i, j] = CellHex(i, j, gc.CELL_SIZE, gc)
                    q = i - math.floor(j / 2)
                    self.ca_grid[q, j] = CellHex(q, j, gc)
                    # print('x={0}, y={1}'.format(q, j))
                    if self.gc.USE_CA_BORDERS and (i == 0 or j == 0 or i == (self.width - 1) or j == (self.height - 1)):
                        self.ca_grid[q, j].is_border = True
        else:
            self.proto_cell = proto_cell
            for j in range(0, self.height):
                for i in range(0, self.width):
                    # self.ca_grid[i, j] = proto_cell.clone(i, j, gc.CELL_SIZE)
                    q = i - math.floor(j / 2)
                    self.ca_grid[q, j] = proto_cell.clone(q, j)
                    # print('x={0}, y={1}'.format(q, j))
                    if self.gc.USE_CA_BORDERS and (i == 0 or j == 0 or i == (self.width - 1) or j == (self.height - 1)):
                        self.ca_grid[q, j].is_border = True

        for cell in list(self.ca_grid.values()):
            self.set_cell_neighborhood(cell)

    # Common Interface for all CA classes

    def set_cell_neighborhood(self, cell):
        cx, cy, cz = cell.get_cube()
        for d in self.gc.HEX_DIRECTIONS:
            x = cx + d[0]
            y = cy + d[1]
            if (x, y) in self.ca_grid:
                cell.neighbors.append(self.ca_grid[x, y])

    def draw_cells(self):
        """
        Simply iterating over all cells and calling their draw() method.
        """
        draw = self.visualizer.draw_cell
        for cell in self.ca_grid.values():
            draw(cell)

    def cycle_automaton(self):
        """
        This method updates the cellular automaton
        """
        self.update_cells_from_neighborhood()
        self.update_cells_state()

    def update_cells_from_neighborhood(self):
        for cell in self.ca_grid.values():
            cell.sense_neighborhood()

    def update_cells_state(self):
        """
        After executing update_neighs this is the actual update of the cell itself
        """
        for cell in self.ca_grid.values():
            cell.update()

    def get_agent_neighborhood(self, other_agents, agent_x, agent_y, dist):
        """
        Creates a dictionary {'position': (cell, set(agents on that cell))} where position is an (x,y) tuple
        for the calling agent to get an overview over its immediate surrounding.
        """
        if dist is None:
            dist = 1
        # x = int(agent_x / self.cell_size)
        # y = int(agent_y / self.cell_size)
        x = agent_x
        y = agent_y
        neighborhood = {}
        for i in range(0 - dist, 1 + dist):
            for j in range(0 - dist, 1 + dist):
                grid_x = x + i
                grid_y = y + j
                if (grid_x, grid_y) in self.ca_grid and not (grid_x == 0 and grid_y == 0):
                    neigh_cell = self.ca_grid[grid_x, grid_y]
                    if (grid_x, grid_y) not in other_agents:
                        neigh_agents = False
                    else:
                        neigh_agents = other_agents[grid_x, grid_y]
                    neighborhood[grid_x, grid_y] = (neigh_cell, neigh_agents)
        return neighborhood

    def get_empty_agent_neighborhood(self, other_agents, agent_x, agent_y, dist):
        """
        Creates a dictionary {'position': cell} where position is an (x,y) tuple
        for the calling agent to get an overview over its immediate surrounding.
        """
        if dist is None:
            dist = 1
        # x = int(agent_x / self.cell_size)
        # y = int(agent_y / self.cell_size)
        x = agent_x
        y = agent_y
        neighborhood = {}
        for i in range(0 - dist, 1 + dist):
            for j in range(0 - dist, 1 + dist):
                grid_x = x + i
                grid_y = y + j
                if (grid_x, grid_y) in self.ca_grid and not (grid_x == 0 and grid_y == 0):
                    neigh_cell = self.ca_grid[grid_x, grid_y]
                    if (grid_x, grid_y) not in other_agents:
                        neighborhood[grid_x, grid_y] = neigh_cell
                    else:
                        continue
        return neighborhood

    def get_random_valid_position(self):
        return random.choice(list(self.ca_grid.keys()))

    @staticmethod
    def hex_round(q, r):
        return CAHex.cube_to_hex(*CAHex.cube_round(*CAHex.hex_to_cube(q, r)))

    @staticmethod
    def cube_round(x, y, z):
        rx = round(x)
        ry = round(y)
        rz = round(z)
        dx = abs(rx - x)
        dy = abs(ry - y)
        dz = abs(rz - z)

        if dx > dy and dx > dz:
            rx = -ry - rz
        elif dy > dz:
            ry = -rx - rz
        else:
            rz = -rx - ry

        return rx, ry, rz

    @staticmethod
    def cube_to_hex(x, y, z):
        return x, y

    @staticmethod
    def hex_to_cube(q, r):
        z = -q - r
        return q, r, z

    @staticmethod
    def hex_distance(q1, r1, q2, r2):
        return (abs(q1 - q2) +
                abs(q1 + r1 - q2 - r2) +
                abs(r1 - r2)) / 2

    @staticmethod
    def cube_distance(cell_a, cell_b):
        return max(abs(cell_a.x - cell_b.x), abs(cell_a.y - cell_b.y),
                   abs(cell_a.z - cell_b.z))

    @staticmethod
    def get_direction_from_to(q1, r1, q2, r2):
        pass

    @staticmethod
    def float_interpolate(a, b, t):
        return a + (b - a) * t

    @staticmethod
    def cube_interpolate(a, b, t):
        x = CAHex.float_interpolate(a.x, b.x, t)
        y = CAHex.float_interpolate(a.y, b.y, t)
        z = CAHex.float_interpolate(a.z, b.z, t)
        return x, y, z

    @staticmethod
    def get_cell_in_direction(a, b):
        # N = CAHex.cube_distance(a, b)
        _x, _y, _z = CAHex.cube_interpolate(a, b, 1)
        _q, _r = CAHex.cube_to_hex(*CAHex.cube_round(_x, _y, _z))
        return _q, _r
