from cab_global_constants import GlobalConstants
from cab_system import ComplexAutomaton

__author__ = "Michael Wagner"


class IoInterface:
    """
    This class declares the interface between the CAB system and IO components.
    """
    def __init__(self, gc: GlobalConstants, cab_core: ComplexAutomaton):
        self.gc = gc
        self.core = cab_core

    def render_simulation(self):
        pass
