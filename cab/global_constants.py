"""
Simulation and model constants. These are supposed to be accessible project-wide.
"""

__author__ = 'Michael Wagner'


class GlobalConstants:
    def __init__(self):
        self.VERSION = "version: 11-2018"
        self.TITLE = "TITLE"
        self.GUI = None  # Options: "TK", "PyGame"
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RNG_SEED = "ABCDL"
        self.RUN_SIMULATION = False
        self.TIME_STEP = 0
        self.ONE_AGENT_PER_CELL = False
        ################################
        #         CA CONSTANTS         #
        ################################
        self.USE_HEX_CA = False
        self.USE_CA_BORDERS = True
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
        self.CELL_SIZE = 15  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        self.DEFAULT_CELL_COLOR = (34, 42, 48)
        ################################
        # Specifically for Rect. CAs   #
        ################################
        self.USE_MOORE_NEIGHBORHOOD = True
        ################################
        # Specifically for Hex CAs     #
        ################################
        self.HEX_DIRECTIONS = [(+1, -1, 0), (+1, 0, -1), (0, +1, -1),
                               (-1, +1, 0), (-1, 0, +1), (0, -1, +1)]
        ################################
        #        ABM CONSTANTS         #
        ################################
        self.DEFAULT_AGENT_COLOR = (0, 255, 0)
        ################################
        #      UTILITY CONSTANTS       #
        ################################
