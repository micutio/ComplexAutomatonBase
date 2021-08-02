__author__ = "Michael Wagner"

import cab.global_constants as cab_gc


class IoInterface:
    """
    This class declares the interface between the CAB system and IO components.
    """
    def __init__(self, gc: cab_gc.GlobalConstants, cab_core):
        self.gc = gc
        self.core = cab_core

    def render_simulation(self):
        pass
