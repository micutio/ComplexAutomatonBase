"""
ComplexAutomaton module of the Complex Automaton Base.
Contains the automaton itself.
"""


from cab.cab_global_constants import GlobalConstants
from cab.abm.cab_abm import ABM
from cab.ca.cab_ca_rect import CARect
from cab.ca.cab_ca_hex import CAHex

from cab.util.cab_io_tk import TkIO
from cab.util.cab_io_pygame import PygameIO
from cab.util.cab_rng import seed_RNG
from util.cab_logging import *

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
        self.gc: GlobalConstants = global_constants
        seed_RNG(self.gc.RNG_SEED)

        if 'proto_agent' in kwargs:
            debug('[ComplexAutomaton] have proto agent {0}'.format(kwargs['proto_agent']))
            self.abm = ABM(self.gc, proto_agent=kwargs['proto_agent'])
            self.proto_agent = kwargs['proto_agent']
        else:
            self.abm = ABM(self.gc)
            self.proto_agent = None

        if 'proto_cell' in kwargs:
            debug('[ComplexAutomaton] have proto agent {0}'.format(kwargs['proto_agent']))
            if self.gc.USE_HEX_CA:
                debug('[ComplexAutomaton] initializing hexagonal CA')
                self.ca = CAHex(self, proto_cell=kwargs['proto_cell'])
            else:
                debug('[ComplexAutomaton] initializing rectangular CA')
                self.ca = CARect(self, proto_cell=kwargs['proto_cell'])
            self.proto_cell = kwargs['proto_cell']
        else:
            if self.gc.USE_HEX_CA:
                debug('[ComplexAutomaton] initializing hexagonal CA')
                self.ca = CAHex(self)
            else:
                debug('[ComplexAutomaton] initializing rectangular CA')
                self.ca = CARect(self)
            self.proto_cell = None

        if self.gc.gui == "TK":
            debug('[ComplexAutomaton] initializing Tk IO')
            self.visualizer = TkIO(self.gc, self)
        elif self.gc.gui == "PyGame":
            debug('[ComplexAutomaton] initializing Pygame IO')
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
        info('resetting simulation')
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
