"""
This module contains the class for a CA with rectangular cells.
Moore and von-Neumann neighborhoods are available.
"""

from cab.abm.cab_agent import CabAgent
from cab.ca.cab_cell import CACell

from abc import ABCMeta
from typing import Dict, Tuple, Union

__author__: str = 'Michael Wagner'


class CabCA(metaclass=ABCMeta):
    def __init__(self, cab_sys, proto_cell: CACell=None):
        """
        Initializes and returns the cellular automaton.
        The CA is a dictionary and not a list of lists
        :returns The initialized CA.
        """
        self.proto_cell = proto_cell
        self.cab_sys = cab_sys
        raise NotImplementedError("Method needs to be implemented")

    # Common Interface for all CA classes

    # def draw_cells(self):
    #     """
    #     Simply iterating over all cells and calling their draw() method.
    #     """
    #     draw = self.visualizer.draw_cell
    #     for cell in self.ca_grid.values():
    #         draw(cell)

    def cycle_automaton(self):
        """
        This method updates the cellular automaton
        """
        raise NotImplementedError("Method needs to be implemented")

    def update_cells_from_neighborhood(self):
        raise NotImplementedError("Method needs to be implemented")

    def update_cells_state(self):
        """
        After executing update_neighs this is the actual update of the cell itself
        """
        raise NotImplementedError("Method needs to be implemented")

    def get_agent_neighborhood(self, agent_x, agent_y, dist) ->\
            Dict[Tuple[int, int], Tuple[CACell, Union[bool, CabAgent]]]:
        """
        Creates a dictionary {'position': (cell, [agents on that cell])}
        for the calling agent to get an overview over its immediate surrounding.
        """
        raise NotImplementedError("Method needs to be implemented")