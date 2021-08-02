
"""
This module contains all classes associated with the agent based system,
except for the agent classes themselves.
"""

import cab.abm.agent as cab_agent
import cab.ca.ca as cab_ca
import cab.global_constants as cab_gc
import cab.util.logging as cab_log
import cab.util.stats as cab_stats

__author__ = 'Michael Wagner'


class ABM:
    def __init__(self, gc: cab_gc.GlobalConstants, proto_agent: cab_agent.CabAgent=None):
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
            cab_log.trace('[ABM] have proto agent {0}'.format(proto_agent))
            self.add_agent(proto_agent)
            self.schedule_new_agents()
        else:
            cab_log.trace('[ABM] have NO proto agent')

    @cab_stats.timedmethod
    def cycle_system(self, ca: cab_ca.CabCA):
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

        # self.agent_set = set([agent for agent in self.agent_set if not agent.dead])
        # cab_log.trace("[ABM] agent set = {0}".format(self.agent_set))
        self.dead_agents = [agent for agent in self.agent_set if agent.dead]
        # cab_log.trace("[ABM] dead agents = {0}".format(self.dead_agents))

        for agent in self.dead_agents:
            cab_log.trace("[ABM] removing agent {0} from position {1},{2}".format(
                agent, agent.x, agent.y))
            self.remove_agent(agent)

        self.agent_set = set(
            [agent for agent in self.agent_set if not agent.dead])
        # cab_log.trace("[ABM] agent set = {0}".format(self.agent_set))

        self.schedule_new_agents()

    def update_agent_position(self, agent: cab_agent.CabAgent):
        """
        Update all agent positions in the location map.
        """
        if self.gc.ONE_AGENT_PER_CELL:
            self.agent_locations.pop((agent.prev_x, agent.prev_y))
            self.agent_locations[agent.x, agent.y] = agent
            cab_log.trace("[ABM] moving agent from = {0}, {1}".format(
                agent.prev_x, agent.prev_y))
        else:
            self.agent_locations[agent.prev_x, agent.prev_y].remove(agent)
            if not self.agent_locations[agent.prev_x, agent.prev_y]:
                cab_log.trace("[ABM] position {0}, {1} empty, removing from location map".format(
                    agent.prev_x, agent.prev_y))
                self.agent_locations.pop((agent.prev_x, agent.prev_y))
            try:
                self.agent_locations[agent.x, agent.y].add(agent)
            except KeyError:
                self.agent_locations[agent.x, agent.y] = {
                    agent}  # set([agent])

    def add_agent(self, agent: cab_agent.CabAgent):
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
        cab_log.trace(
            "[ABM] agent added to position {0}, {1}".format(agent.x, agent.y))

    def schedule_new_agents(self):
        """
        Adds an agent to be scheduled by the abm.
        """
        for agent in self.new_agents:
            # pos = (agent.x, agent.y)
            self.agent_set.add(agent)
            cab_log.trace("[ABM] agent {0} scheduled by the ABM".format(agent))

    def remove_agent(self, agent: cab_agent.CabAgent):
        """
        Removes an agent from the system.
        """
        if self.gc.ONE_AGENT_PER_CELL:
            if self.agent_locations[agent.x, agent.y].a_id == agent.a_id:
                del(self.agent_locations[agent.x, agent.y])
        else:
            self.agent_locations[agent.x, agent.y].discard(agent)
            if len(self.agent_locations[agent.x, agent.y]) == 0:
                del(self.agent_locations[agent.x, agent.y])
