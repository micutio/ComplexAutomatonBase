"""
ComplexAutomaton module of the Complex Automaton Base.
Contains the automaton itself.
"""

# External library imports.
# import pygame
# import math
# from pygame.locals import *

# Internal Simulation System component imports.
from cab.cab_global_constants import GlobalConstants
from cab.abm.cab_abm import ABM
from cab.ca.cab_ca import CARect
from cab.ca.cab_ca_hex import CAHex
from cab.util.cab_io_tk import TkIO

from cab.util.cab_io_pygame import PygameIO

__author__ = 'Michael Wagner'


class ComplexAutomaton:
    """
    The main class of Sugarscape. This controls everything.
    """

    def __init__(self, global_constants: GlobalConstants, **kwargs):
        """
        Standard initializer.
        :param global_constants: All constants or important variables that control the simulation.
        :param kwargs**: cell prototype, agent prototype, visualizer prototype and IO handler prototype.
        """
        self.gc = global_constants

        if 'proto_agent' in kwargs:
            self.abm = ABM(self.gc, proto_agent=kwargs['proto_agent'])
            self.proto_agent = kwargs['proto_agent']
        else:
            self.abm = ABM(self.gc)
            self.proto_agent = None

        if 'proto_cell' in kwargs:
            if self.gc.USE_HEX_CA:
                self.ca = CAHex(self, proto_cell=kwargs['proto_cell'])
            else:
                self.ca = CARect(self, proto_cell=kwargs['proto_cell'])
            self.proto_cell = kwargs['proto_cell']
        else:
            if self.gc.USE_HEX_CA:
                self.ca = CAHex(self)
            else:
                self.ca = CARect(self)
            self.proto_cell = None

        # TODO: Make this dependent on global constants
        # PygameIO() | TkIO() | QtIO()
        if self.gc.gui == "TK":
            self.visualizer = TkIO(self.gc, self)
        elif self.gui == "PyGame":
            self.visualizer = PygameIO(self.gc, self)
        self.display_info()

    def display_info(self):
        print("\n {0}, version {1}"
              "\n keys:"
              "\n        [SPACE] pause/resume simulation"
              "\n          [S]   step simulation        "
              "\n          [R]   reset simulation       "
              "\n ".format(self.gc.TITLE, self.gc.VERSION))

    def reset_simulation(self):
        print('resetting simulation')
        self.abm.__init__(self.gc, proto_agent=self.proto_agent)
        self.ca.__init__(self, proto_cell=self.proto_cell)
        self.gc.TIME_STEP = 0

    def step_simulation(self):
        self.abm.cycle_system(self.ca)
        self.ca.cycle_automaton()
        self.gc.TIME_STEP += 1

    def run_main_loop(self):
        """
        Main method. It executes the CA.
        """
        print("simulation log:")
        print()
        self.visualizer.render_simulation()
