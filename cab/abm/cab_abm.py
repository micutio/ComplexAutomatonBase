"""
This module contains all classes associated with the agent based system,
except for the agent classes themselves.
"""

__author__ = 'Michael Wagner'


# TODO: include choice between cells inhabitable by only one or multiple agents at once.
class ABM:
    def __init__(self, gc, proto_agent=None):
        """
        Initializes an abm with the given number of agents and returns it.
        :param gc: Global Constants, Parameters for the ABM.
        :return: An initialized ABM.
        """
        self.agent_set = set()
        self.agent_locations = dict()
        self.gc = gc
        self.new_agents = []
        if proto_agent is not None:
            self.add_agent(proto_agent)

    def cycle_system(self, ca):
        """
        Cycles through all agents and has them perceive and act in the world
        """
        # Have all agents perceive and act in a random order
        # While we're at it, look for dead agents to remove
        # changed_agents = []
        for a in self.agent_set:
            a.perceive_and_act(self, ca)
            if a.x != a.prev_x or a.y != a.prev_y:
                self.update_agent_position(a)
        self.agent_set = set([agent for agent in self.agent_set if not agent.dead])
        dead_agents = [agent for agent in self.agent_set if agent.dead]
        for agent in dead_agents:
            self.remove_agent(agent)
        self.schedule_new_agents()

    def update_agent_position(self, agent):
        if self.gc.ONE_AGENT_PER_CELL:
            self.agent_locations.pop((agent.prev_x, agent.prev_y))
            self.agent_locations[agent.x, agent.y] = agent
        else:
            self.agent_locations[agent.prev_x, agent.prev_y].remove(agent)
            if not self.agent_locations[agent.prev_x, agent.prev_y]:
                self.agent_locations.pop((agent.prev_x, agent.prev_y))
            try:
                self.agent_locations[agent.x, agent.y].add(agent)
            except KeyError:
                self.agent_locations[agent.x, agent.y] = {agent}  # set([agent])

    def add_agent(self, agent):
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
        self.new_agents = list()

    def remove_agent(self, agent):
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

    # def draw_agents(self):
    #     """
    #     Iterates over all agents and hands them over to the visualizer.
    #     """
    #     draw = self.visualizer.draw_agent
    #     for a in self.agent_set:
    #         draw(a)
