"""
ComplexAutomaton module of the Complex Automaton Base.
Contains the automaton itself.
"""


import cab.global_constants as cab_gc
import cab.abm.abm as cab_abm
import cab.ca.ca_rect as ca_rect
import cab.ca.ca_hex as ca_hex

import cab.util.io_tk as cab_io_tk
import cab.util.io_pygame as cab_io_pg
import cab.util.rng as cab_rng
import cab.util.logging as cab_log

__author__ = 'Michael Wagner'


class ComplexAutomaton:
    """
    The main class of Sugarscape. This controls everything.
    """

    def __init__(self, global_constants: cab_gc.GlobalConstants, **kwargs):
        """
        Standard initializer.
        :param global_constants: All constants or important variables that control the simulation.
        :param kwargs**: cell prototype, agent prototype, visualizer prototype and IO handler prototype.
        """
        self.gc: cab_gc.GlobalConstants = global_constants
        cab_rng.seed_RNG(self.gc.RNG_SEED)

        if 'proto_agent' in kwargs:
            cab_log.trace('[ComplexAutomaton] have proto agent {0}'.format(kwargs['proto_agent']))
            self.abm = cab_abm.ABM(self.gc, proto_agent=kwargs['proto_agent'])
            self.proto_agent = kwargs['proto_agent']
        else:
            self.abm = cab_abm.ABM(self.gc)
            self.proto_agent = None

        if 'proto_cell' in kwargs:
            cab_log.trace('[ComplexAutomaton] have proto cell {0}'.format(kwargs['proto_cell']))
            if self.gc.USE_HEX_CA:
                cab_log.trace('[ComplexAutomaton] initializing hexagonal CA')
                self.ca = ca_hex.CAHex(self, proto_cell=kwargs['proto_cell'])
            else:
                cab_log.trace('[ComplexAutomaton] initializing rectangular CA')
                self.ca = ca_rect.CARect(self, proto_cell=kwargs['proto_cell'])
            self.proto_cell = kwargs['proto_cell']
        else:
            if self.gc.USE_HEX_CA:
                cab_log.trace('[ComplexAutomaton] initializing hexagonal CA')
                self.ca = ca_hex.CAHex(self)
            else:
                cab_log.trace('[ComplexAutomaton] initializing rectangular CA')
                self.ca = ca_rect.CARect(self)
            self.proto_cell = None

        if self.gc.gui == "TK":
            cab_log.trace('[ComplexAutomaton] initializing Tk IO')
            self.visualizer = cab_io_tk.TkIO(self.gc, self)
        elif self.gc.gui == "PyGame":
            cab_log.trace('[ComplexAutomaton] initializing Pygame IO')
            self.visualizer = cab_io_pg.PygameIO(self.gc, self)
        self.display_info()

    def display_info(self):
        print("\n {0}, version {1}"
              "\n keys:"
              "\n        [SPACE] pause/resume simulation"
              "\n          [S]   step simulation        "
              "\n          [R]   reset simulation       "
              "\n ".format(self.gc.TITLE, self.gc.VERSION))

    def reset_simulation(self):
        """
        Re-call the initializers for ABM and CA to reset the CAB completely.
        TODO: Improve this, as not everything that can be modified is reset.
        """
        cab_log.info('resetting simulation')
        self.abm.__init__(self.gc, proto_agent=self.proto_agent)
        self.ca.__init__(self, proto_cell=self.proto_cell)
        self.gc.TIME_STEP = 0

    def step_simulation(self):
        self.abm.cycle_system(self.ca)
        self.ca.cycle_automaton()
        self.gc.TIME_STEP += 1

    def run_main_loop(self):
        """
        Main method. Hand over simulation control to the GUI and run from there.
        """
        print("simulation log:")
        print()
        self.visualizer.render_simulation()
