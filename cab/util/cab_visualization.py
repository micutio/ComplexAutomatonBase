"""
This module contains a simple visualization class, which the actual simulation visualizer should inherit from.
"""


import pygame
import pygame.gfxdraw
from pygame.locals import *
import math

from cab.util.cab_input_handling import InputHandler

__author__ = 'Michael Wagner'


class Visualization:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, cab_core):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param surface: Pygame surface object.
        """
        self.abm = cab_core.abm
        self.ca = cab_core.ca
        self.surface = None
        self.gc = gc
        self.core = cab_core
        self.io_handler = InputHandler()

        # Initialize UI components.
        pygame.init()
        # pygame.display.init()
        if self.gc.USE_HEX_CA:
            offset_x = int((math.sqrt(3) / 2) * (self.gc.CELL_SIZE * 2) * (self.gc.DIM_X - 1))
            offset_y = int((3 / 4) * (self.gc.CELL_SIZE * 2) * (self.gc.DIM_Y - 1))
            # print(offset)
            # self.screen = pygame.display.set_mode((self.gc.GRID_WIDTH, self.gc.GRID_HEIGHT), pygame.RESIZABLE, 32)
        else:
            offset_x = self.gc.CELL_SIZE * self.gc.DIM_X
            offset_y = self.gc.CELL_SIZE * self.gc.DIM_Y
        self.surface = pygame.display.set_mode((offset_x, offset_y), HWSURFACE | DOUBLEBUF, 32)
        pygame.display.set_caption('Complex Automaton Base')

    def render_simulation(self):
        self.io_handler.process_input()

        draw_cell = self.draw_cell
        for c in list(self.ca.ca_grid.values()):
            draw_cell(c)
        draw_agent = self.draw_agent
        for a in self.abm.agent_set:
            draw_agent(a)
        pygame.display.flip()

    def draw_agent(self, agent):
        """
        Simple exemplary visualization. Draw agent as a black circle
        """
        if agent.x is not None and agent.y is not None and not agent.dead:
            radius = int(agent.size / 1.5)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)

            pygame.draw.circle(self.surface, agent.color, (x, y), radius, 0)
            pygame.gfxdraw.aacircle(self.surface, x, y, radius, (50, 100, 50))

    def draw_cell(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if cell is None:
            pass
        elif cell.rectangular:
            pygame.draw.rect(self.surface, cell.color, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        else:
            if self.gc.DISPLAY_GRID:
                pygame.gfxdraw.aapolygon(self.surface, cell.get_corners(), (190, 190, 190))
            else:
                pygame.gfxdraw.aapolygon(self.surface, cell.get_corners(), cell.color)
            return