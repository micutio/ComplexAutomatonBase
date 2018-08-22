
"""
This module contains all classes associated with the agent based system,
except for the agent classes themselves.
"""

from cab.abm.cab_agent import CabAgent
from cab.ca.cab_ca import CabCA
from cab.cab_global_constants import GlobalConstants
from cab.util.cab_logging import trace

__author__ = 'Michael Wagner'


# TODO: include choice between cells inhabitable by only one or multiple agents at once.
class ABM:
    def __init__(self, gc: GlobalConstants, proto_agent: CabAgent=None):
        """
        Initializes an abm with the given number of agents and returns it.
        :param gc: Global Constants, Parameters for the ABM.
        :return: An initialized ABM.
        """
        self.agent_set = set()
        self.agent_locations = dict()
        self.gc = gc
        self.new_agents = list()
        self.dead_agents = list()
        if proto_agent is not None:
            trace('[ABM] have proto agent {0}'.format(proto_agent))
            self.add_agent(proto_agent)
            self.schedule_new_agents()
        else:
            trace('[ABM] have NO proto agent')

    def cycle_system(self, ca: CabCA):
        """
        Cycles through all agents and has them perceive and act in the world
        """
        # Have all agents perceive and act in a random order
        # While we're at it, look for dead agents to remove
        # changed_agents = []
        self.new_agents = list()
        self.dead_agents = list()

        for a in self.agent_set:
            a.perceive_and_act(self, ca)
            if a.x != a.prev_x or a.y != a.prev_y:
                self.update_agent_position(a)

        self.agent_set = set([agent for agent in self.agent_set if not agent.dead])
        trace("[ABM] agent set = {0}".format(self.agent_set))
        self.dead_agents = [agent for agent in self.agent_set if agent.dead]
        trace("[ABM] dead agents = {0}".format(self.dead_agents))

        for agent in self.dead_agents:
            self.remove_agent(agent)
        self.schedule_new_agents()

    def update_agent_position(self, agent: CabAgent):
        """
        Update all agent positions in the location map.
        """
        if self.gc.ONE_AGENT_PER_CELL:
            self.agent_locations.pop((agent.prev_x, agent.prev_y))
            self.agent_locations[agent.x, agent.y] = agent
            trace("[ABM] moving agent from = {0}, {1}".format(agent.prev_x, agent.prev_y))
        else:
            self.agent_locations[agent.prev_x, agent.prev_y].remove(agent)
            if not self.agent_locations[agent.prev_x, agent.prev_y]:
                trace("[ABM] position {0}, {1} empty, removing from location map".format(agent.prev_x, agent.prev_y))
                self.agent_locations.pop((agent.prev_x, agent.prev_y))
            try:
                self.agent_locations[agent.x, agent.y].add(agent)
            except KeyError:
                self.agent_locations[agent.x, agent.y] = {agent}  # set([agent])

    def add_agent(self, agent: CabAgent):
        """
        Add an agent to the system.
        """
        self.new_agents.append(agent)
        pos = (agent.x, agent.y)
        if agent.x is not None and agent.y is not None:
            if self.gc.ONE_AGENT_PER_CELL:
                if pos not in self.agent_locations:
                    self.agent_locations[pos] = agent
                    # Can't insert agent if cell is already occupied.
            else:
                if pos in self.agent_locations:
                    self.agent_locations[pos].add(agent)
                else:
                    self.agent_locations[pos] = {agent}
        trace("[ABM] agent added to position {0}, {1}".format(agent.x, agent.y))

    def schedule_new_agents(self):
        """
        Adds an agent to be scheduled by the abm.
        """
        for agent in self.new_agents:
            # pos = (agent.x, agent.y)
            self.agent_set.add(agent)
            # if agent.x is not None and agent.y is not None:
            #     if self.gc.ONE_AGENT_PER_CELL:
            #         if pos not in self.agent_locations:
            #             self.agent_locations[pos] = agent
            #         # Can't insert agent if cell is already occupied.
            #     else:
            #         if pos in self.agent_locations:
            #             self.agent_locations[pos].add(agent)
            #         else:
            #             self.agent_locations[pos] = {agent}
        # self.new_agents = list()
            trace("[ABM] agent {0} scheduled by the ABM".format(agent))

    def remove_agent(self, agent: CabAgent):
        """
        Removes an agent from the system.
        """
        print("removing agent {0}".format(agent))
        if self.gc.ONE_AGENT_PER_CELL:
            if self.agent_locations[agent.x, agent.y].a_id == agent.a_id:
                del(self.agent_locations[agent.x, agent.y])
        else:
            self.agent_locations[agent.x, agent.y].discard(agent)
            if len(self.agent_locations[agent.x, agent.y]) == 0:
                del(self.agent_locations[agent.x, agent.y])

    # def draw_agents(self):
    #     """
    #     Iterates over all agents and hands them over to the visualizer.
    #     """
    #     draw = self.visualizer.draw_agent
    #     for a in self.agent_set:
    #         draw(a)
