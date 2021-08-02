"""
This module contains a CAB io implementation in PyGame.
"""

import pygame
import pygame.gfxdraw
import pygame.locals
import math

import cab.abm.agent as cab_agent
import cab.ca.cell as cab_cell
import cab.util.io_pygame_input as cab_pygame_io
import cab.util.io_interface as cab_io
import cab.global_constants as cab_gc
import cab.util.logging as cab_log

__author__ = 'Michael Wagner'


class PygameIO(cab_io.IoInterface):
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc: cab_gc.GlobalConstants, cab_core):
        """
        Initializes the visualization.
        """
        super().__init__(gc, cab_core)
        self.abm = cab_core.abm
        self.ca = cab_core.ca
        self.surface = None
        self.io_handler = cab_pygame_io.InputHandler(cab_core)

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
        self.surface = pygame.display.set_mode((offset_x, offset_y), pygame.locals.HWSURFACE | pygame.locals.DOUBLEBUF, 32)
        pygame.display.set_caption('Complex Automaton Base')
        cab_log.trace("[PygameIO] initializing done")

    def render_frame(self):
        self.io_handler.process_input()

        if self.gc.RUN_SIMULATION:
            self.core.step_simulation()

        draw_cell = self.draw_cell
        for c in list(self.ca.ca_grid.values()):
            draw_cell(c)
        draw_agent = self.draw_agent
        for a in self.abm.agent_set:
            draw_agent(a)
        pygame.display.flip()

# TODO: Change render_simulation to fit the whole simulation loop inside.
    def render_simulation(self):
        cab_log.trace("[PygameIO] start rendering simulation")
        while True:
            self.render_frame()

    def draw_agent(self, agent: cab_agent.CabAgent):
        """
        Simple exemplary visualization. Draw agent as a black circle
        """
        if agent.x is not None and agent.y is not None and not agent.dead:
            radius = int(agent.size / 1.25)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)

            pygame.draw.circle(self.surface, agent.color, (x, y), radius, 0)
            pygame.gfxdraw.aacircle(self.surface, x, y, radius, (50, 100, 50))

    def draw_cell(self, cell: cab_cell.CACell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if cell is None:
            pass
        else:
            pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), cell.color)
            if self.gc.DISPLAY_GRID:
                pygame.gfxdraw.aapolygon(self.surface, cell.get_corners(), self.gc.DEFAULT_GRID_COLOR)
            else:
                pygame.gfxdraw.aapolygon(self.surface, cell.get_corners(), cell.color)
            return
