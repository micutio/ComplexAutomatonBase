"""
ComplexAutomaton module of the Complex Automaton Base.
Contains the automaton itself.
"""

import pygame
import math

from cab.abm.cab_abm import ABM
from cab.ca.cab_ca import CARect
from cab.ca.cab_ca_hex import CAHex
from cab.util.cab_input_handling import InputHandler
from cab.util.cab_visualization import Visualization

from pygame.locals import *


__author__ = 'Michael Wagner'


class ComplexAutomaton:
    """
    The main class of Sugarscape. This controls everything.
    """

    def __init__(self, global_constants, **kwargs):
        # proto_cell=None, proto_agent=None, proto_visualizer=None, proto_handler=None):
        """
        Standard initializer.
        :param global_constants: All constants or important variables that control the simulation.
        """
        self.gc = global_constants

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

        self.screen = pygame.display.set_mode((offset_x, offset_y), HWSURFACE | DOUBLEBUF, 32)
        pygame.display.set_caption('Complex Automaton Base')

        if 'proto_visualizer' in kwargs:
            self.visualizer = kwargs['proto_visualizer'].clone(self.gc, self.screen, self)
        else:
            self.visualizer = Visualization(self.gc, self.screen, self)

        if 'proto_cell' in kwargs:
            if self.gc.USE_HEX_CA:
                self.ca = CAHex(self.gc, self.visualizer, proto_cell=kwargs['proto_cell'])
            else:
                self.ca = CARect(self.gc, self.visualizer, proto_cell=kwargs['proto_cell'])
            self.proto_cell = kwargs['proto_cell']
        else:
            if self.gc.USE_HEX_CA:
                self.ca = CAHex(self.gc, self.visualizer)
            else:
                self.ca = CARect(self.gc, self.visualizer)
            self.proto_cell = None

        if 'proto_agent' in kwargs:
            self.abm = ABM(self.gc, self.visualizer, proto_agent=kwargs['proto_agent'])
            self.proto_agent = kwargs['proto_agent']
        else:
            self.abm = ABM(self.gc, self.visualizer)
            self.proto_agent = None

        if 'proto_handler' in kwargs:
            self.handler = kwargs['proto_handler'].clone(self)
        else:
            self.handler = InputHandler(cab_system=self)

        self.display_info()
        return

    def display_info(self):
        print("\n {0}, version {1}"
              "\n keys:"
              "\n        [SPACE] pause/resume simulation"
              "\n          [S]   step simulation        "
              "\n          [R]   reset simulation       "
              "\n ".format(self.gc.TITLE, self.gc.VERSION))

    def reset_simulation(self):
        self.ca.__init__(self.gc, self.visualizer, self.proto_cell)
        self.abm.__init__(self.gc, self.visualizer, self.proto_agent)
        self.gc.TIME_STEP = 0

    def step_simulation(self):
        self.abm.cycle_system(self.ca)
        self.ca.cycle_automaton()
        self.gc.TIME_STEP += 1

    def render_simulation(self):
        self.ca.draw_cells()
        self.abm.draw_agents()
        pygame.display.flip()

    def run_main_loop(self):
        """
        Main method. It executes the CA.
        """
        print("simulation log:")
        print()
        while True:
            if self.gc.RUN_SIMULATION:
                self.step_simulation()
                self.gc.TIME_STEP += 1
            self.render_simulation()
            self.handler.process_input()
