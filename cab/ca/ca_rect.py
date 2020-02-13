"""
This module contains the class for a CA with rectangular cells.
Moore and von-Neumann neighborhoods are available.
"""

from typing import Dict, Tuple, Union

import cab.ca.ca as cab_ca
import cab.abm.agent as cab_agent
import cab.ca.cell as cab_cell

__author__: str = 'Michael Wagner'


class CARect(cab_ca.CabCA):
    def __init__(self, cab_sys, proto_cell: cab_cell.CellRect = None):
        """
        Initializes and returns the cellular automaton.
        The CA is a dictionary and not a list of lists
        :returns The initialized CA.
        """
        super().__init__(cab_sys, proto_cell)
        self.ca_grid: Dict[Tuple[int, int], cab_cell.CellRect] = dict()
        self.sys = cab_sys
        self.grid_height: int = self.sys.gc.GRID_HEIGHT
        self.grid_width: int = self.sys.gc.GRID_WIDTH
        self.height: int = int(self.grid_height / self.sys.gc.CELL_SIZE)
        self.width: int = int(self.grid_width / self.sys.gc.CELL_SIZE)
        self.cell_size: int = self.sys.gc.CELL_SIZE
        self.use_moore_neighborhood: bool = self.sys.gc.USE_MOORE_NEIGHBORHOOD
        self.use_borders: bool = self.sys.gc.USE_CA_BORDERS
        self.proto_cell: cab_cell.CellRect = None

        if proto_cell is None:
            for j in range(0, self.height):
                for i in range(0, self.width):
                    self.ca_grid[i, j] = cab_cell.CellRect(i, j, self.sys.gc)
        else:
            self.proto_cell = proto_cell
            for j in range(0, self.height):
                for i in range(0, self.width):
                    self.ca_grid[i, j] = proto_cell.clone(i, j)

        if self.use_moore_neighborhood:
            self.init_moore()
            self.init_moore_borders()
        else:
            self.init_von_neumann()
            self.init_von_neumann_borders()

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

    def get_agent_neighborhood(self, agent_x, agent_y, dist) ->\
            Dict[Tuple[int, int], Tuple[cab_cell.CellRect, Union[bool, cab_agent.CabAgent]]]:
        """
        Creates a dictionary {'position': (cell, [agents on that cell])}
        for the calling agent to get an overview over its immediate surrounding.
        """
        x = int(agent_x / self.cell_size)
        y = int(agent_y / self.cell_size)
        neighborhood = {}
        other_agents = self.sys.abm.agent_locations
        for i in range(-1 - dist, 2 + dist):
            for j in range(-1 - dist, 2 + dist):
                grid_x = x + i
                grid_y = y + j
                if (grid_x, grid_y) in self.ca_grid and not (grid_x == 0 and grid_y == 0):
                    a = self.ca_grid[grid_x, grid_y]
                    if (grid_x, grid_y) not in other_agents:
                        b = False
                    else:
                        b = other_agents[grid_x, grid_y]
                    neighborhood[grid_x, grid_y] = (a, b)
        return neighborhood

    # Individual methods for this specific CA

    def init_von_neumann(self):
        """
        Looping over all cells to gather the neighbor information they need to update.
        This method uses Von-Neumann-Neighborhood (except for borders which are dealt
        with by borders_von_neumann)
        This method is used for initializing neighbor references in the cells
        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                neighbors = [self.ca_grid[x, (y - 1)],
                             self.ca_grid[x, (y + 1)],
                             self.ca_grid[(x - 1), y],
                             self.ca_grid[(x + 1), y]]
                self.ca_grid[x, y].set_neighbors(neighbors)

    def init_von_neumann_borders(self):
        """
        Going through all border-regions of the automaton to update them.
        This method is used for initializing neighbor references in the cells
        """
        w = self.width
        h = self.height
        for y in range(1, self.height - 1):
            neighbors_vn = [
                self.ca_grid[0, (y - 1)], self.ca_grid[0, (y + 1)], self.ca_grid[1, y]]
            self.ca_grid[0, y].set_neighbors(neighbors_vn)

            neighbors_vn = [self.ca_grid[(
                w - 1), (y - 1)], self.ca_grid[(w - 1), (y + 1)], self.ca_grid[(w - 2), y]]
            self.ca_grid[(w - 1), y].set_neighbors(neighbors_vn)

        for x in range(1, self.width - 1):
            neighbors_vn = [self.ca_grid[x, 1],
                            self.ca_grid[(x - 1), 0], self.ca_grid[(x + 1), 0]]
            self.ca_grid[x, 0].set_neighbors(neighbors_vn)

            neighbors_vn = [
                self.ca_grid[x, (h - 2)], self.ca_grid[(x - 1), (h - 1)], self.ca_grid[(x + 1), (h - 1)]]
            self.ca_grid[x, (h - 1)].set_neighbors(neighbors_vn)

        # top left corner
        neighbors_vn = [self.ca_grid[0, 1], self.ca_grid[1, 0]]
        self.ca_grid[0, 0].set_neighbors(neighbors_vn)

        # top right corner
        neighbors_vn = [self.ca_grid[(w - 1), 1], self.ca_grid[(w - 2), 0]]
        self.ca_grid[(w - 1), 0].set_neighbors(neighbors_vn)

        # bottom left corner
        neighbors_vn = [self.ca_grid[0, (h - 2)], self.ca_grid[1, (h - 1)]]
        self.ca_grid[0, (h - 1)].set_neighbors(neighbors_vn)

        # bottom right corner
        neighbors_vn = [
            self.ca_grid[(w - 1), (h - 2)], self.ca_grid[(w - 2), (h - 1)]]
        self.ca_grid[(w - 1), (h - 1)].set_neighbors(neighbors_vn)

    def init_moore(self):
        """
        Looping over all cells to gather the neighbor information they need to update.
        This method uses Moore_neighborhood.  (except for borders which are dealt
        with by borders_moore)
        This method is used for initializing neighbor references in the cells

        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                neighbors = [self.ca_grid[x, (y - 1)],
                             self.ca_grid[x, (y + 1)],
                             self.ca_grid[(x - 1), y],
                             self.ca_grid[(x + 1), y],
                             self.ca_grid[(x - 1), (y - 1)],  # Top Left
                             self.ca_grid[(x + 1), (y - 1)],  # Top Right
                             self.ca_grid[(x - 1), (y + 1)],  # Bottom Left
                             self.ca_grid[(x + 1), (y + 1)]]  # Bottom Right
                self.ca_grid[x, y].set_neighbors(neighbors)

    def init_moore_borders(self):
        """
        Going through all border-regions of the automaton to update them.
        This method is used for initializing neighbor references in the cells

        """
        w = self.width
        h = self.height
        for y in range(1, self.height - 1):
            neighbors_mo = [self.ca_grid[0, (y - 1)], self.ca_grid[0, (y + 1)], self.ca_grid[1, y],
                            self.ca_grid[1, (y - 1)], self.ca_grid[1, (y + 1)]]
            self.ca_grid[0, y].set_neighbors(neighbors_mo)

            neighbors_mo = [self.ca_grid[(w - 1), (y - 1)], self.ca_grid[(w - 1), (y + 1)], self.ca_grid[(w - 2), y],
                            self.ca_grid[(w - 2), (y - 1)], self.ca_grid[(w - 2), (y + 1)]]
            self.ca_grid[(w - 1), y].set_neighbors(neighbors_mo)

        for x in range(1, self.width - 1):
            neighbors_mo = [self.ca_grid[x, 1], self.ca_grid[(x - 1), 0], self.ca_grid[(x + 1), 0],
                            self.ca_grid[(x - 1), 1], self.ca_grid[(x + 1), 1]]
            self.ca_grid[x, 0].set_neighbors(neighbors_mo)

            neighbors_mo = [self.ca_grid[x, (h - 2)], self.ca_grid[(x - 1), (h - 1)], self.ca_grid[(x + 1), (h - 1)],
                            self.ca_grid[(x - 1), (h - 2)], self.ca_grid[(x + 1), (h - 2)]]
            self.ca_grid[x, (h - 1)].set_neighbors(neighbors_mo)

        # top left corner
        neighbors_mo = [self.ca_grid[0, 1],
                        self.ca_grid[1, 0], self.ca_grid[1, 1]]
        self.ca_grid[0, 0].set_neighbors(neighbors_mo)

        # top right corner
        neighbors_mo = [
            self.ca_grid[(w - 1), 1], self.ca_grid[(w - 2), 0], self.ca_grid[(w - 2), 1]]
        self.ca_grid[(w - 1), 0].set_neighbors(neighbors_mo)

        # bottom left corner
        neighbors_mo = [
            self.ca_grid[0, (h - 2)], self.ca_grid[1, (h - 1)], self.ca_grid[1, (h - 2)]]
        self.ca_grid[0, (h - 1)].set_neighbors(neighbors_mo)

        # bottom right corner
        neighbors_mo = [self.ca_grid[(
            w - 1), (h - 2)], self.ca_grid[(w - 2), (h - 1)], self.ca_grid[(w - 2), (h - 2)]]
        self.ca_grid[(w - 1), (h - 1)].set_neighbors(neighbors_mo)
