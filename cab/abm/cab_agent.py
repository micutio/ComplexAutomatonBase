"""
This module contains all classes associated with the agents of the system.
"""


import uuid
from abc import ABCMeta, abstractmethod


__author__ = 'Michael Wagner'


class CabAgent(metaclass=ABCMeta):
    """
    Parent class for all agents.
    Every subclass has to implement the perceive_and_act() method.
    """

    def __init__(self, x, y, gc):
        self.a_id = uuid.uuid4().urn
        self.gc = gc
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.size = gc.CELL_SIZE
        self.color = gc.DEFAULT_AGENT_COLOR
        self.dead = False

    @abstractmethod
    def perceive_and_act(self, abm, ca):
        raise NotImplementedError("Method needs to be implemented")

    def on_lmb_click(self, abm, ca):
        """
        Executed when the mouse is pointed at the agent and left clicked.
        To be implemented by the gui class.
        :return: 
        """
        pass

    def on_rmb_click(self, abm, ca):
        """
        Executed when the mouse is pointed at the agent and right clicked.
        To be implemented by the gui class.
        :return: 
        """
        pass

    def on_mouse_scroll_up(self, abm, ca):
        """
        Executed when the mouse is pointed at the cell and wheel scrolled up.
        """
        pass

    def on_mouse_scroll_down(self, abm, ca):
        """
        Executed when the mouse is pointed at the cell and wheel scrolled down.
        """
        pass