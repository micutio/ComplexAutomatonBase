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
