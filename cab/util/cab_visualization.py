"""
This module contains a simple visualization class, which the actual simulation visualizer should inherit from.
"""
__author__ = 'Michael Wagner'

import pygame
import pygame.gfxdraw


class Visualization:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, surface):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param surface: Pygame surface object.
        """
        if surface is None:
            self.surface = None
        else:
            self.surface = surface
        self.gc = gc

    def clone(self, surface):
        return Visualization(self.gc, surface)

    def draw_agent(self, agent):
        """
        Simple exemplary visualization. Draw agent as a black circle
        """
        raise NotImplementedError("Method needs to be implemented")

    def draw_cell(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if cell is None:
            pass
        elif cell.rectangular:
            pygame.draw.rect(self.surface, (255, 255, 255), (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        else:
            crnrs = cell.get_corners()
            # pygame.draw.polygon(self.surface, (255, 255, 255), crnrs, 1)
            
            # print(crnrs)
            # pygame.draw.aalines(self.surface, (255, 255, 255), True, crnrs, 0)
            pygame.gfxdraw.aapolygon(self.surface, crnrs, (255, 255, 255))