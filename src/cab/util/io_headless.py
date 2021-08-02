__author__ = "Michael Wagner"

import cab.global_constants as cab_gc
import cab.util.io_interface as cab_io


class IoHeadless(cab_io.IoInterface):
    """
    Headless 'visualization' option. This IO class omits graphical output and is used mostly for unit testing.
    """
    def __init__(self, gc: cab_gc.GlobalConstants, cab_core, numSteps):
        super().__init__(gc, cab_core)
        self.numSteps = numSteps

    def render_simulation(self):
        for _ in range(self.numSteps):
            self.core.step_simulation()
