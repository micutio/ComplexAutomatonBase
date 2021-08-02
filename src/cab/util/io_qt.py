"""
This module contains a CAB io implementation in TkInter.
"""

# TODO: Finish or delete

# External library imports.
import math
import sys

# Internal Simulation System component imports.
from PyQt5.uic.properties import QtGui
from cab.ca.ca_hex import CAHex
from util.io_interface import IoInterface

__author__ = 'Michael Wagner'


class QtIO(IoInterface):
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, cab_core):
        super().__init__(gc, cab_core)
        self.root = QtGui.QtApplication
        self.width = 0
        self.height = 0
        self.root.title("Complex Automaton")
        self.canvas = None