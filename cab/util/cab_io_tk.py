"""
This module contains a CAB io implementation in TkInter.
"""

# External library imports.
import math
import sys
from tkinter import Tk, Canvas

# Internal Simulation System component imports.
from cab.ca.cab_ca_hex import CAHex

from util.cab_io_interface import IoInterface

__author__ = 'Michael Wagner'


class TkIO(IoInterface):
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, cab_core):
        super().__init__(gc, cab_core)
        self.root = Tk()
        self.width = 0
        self.height = 0
        self.root.title("Complex Automaton")
        self.canvas = None
        self.cell_shape_mapping = list()
        self.agent_shape_mapping = list()

        self.init_canvas()
        self.init_cell_shape_mapping()
        self.init_agent_shape_mapping()

        self.input_actions = TkInputActions(self)
        self.input_actions.set_binds()

    def init_canvas(self):
        if self.gc.USE_HEX_CA:
            self.width = int((math.sqrt(3) / 2) * (self.gc.CELL_SIZE * 2) * (self.gc.DIM_X - 1))
            self.height = int((3 / 4) * (self.gc.CELL_SIZE * 2) * (self.gc.DIM_Y - 1))
            # print(offset)
            # screen = pygame.display.set_mode((self.gc.GRID_WIDTH, self.gc.GRID_HEIGHT), pygame.RESIZABLE, 32)
        else:
            self.width = self.gc.CELL_SIZE * self.gc.DIM_X
            self.height = self.gc.CELL_SIZE * self.gc.DIM_Y

        col = '#%02x%02x%02x' % self.gc.DEFAULT_CELL_COLOR
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg=col)
        self.canvas.pack()

    def init_cell_shape_mapping(self):
        for k, v in list(self.core.ca.ca_grid.items()):
            corners_list = [i for tupl in v.get_corners() for i in tupl]
            col_f = self.get_color_string(v.color)
            col_o = self.get_color_string((0, 0, 0))
            polygon = self.canvas.create_polygon(corners_list, fill=col_f, outline=col_o)
            old_color = v.color
            self.cell_shape_mapping.append((polygon, v, old_color))

    def init_agent_shape_mapping(self):
        for agent in self.core.abm.agent_set:
            radius = int(agent.size / 1.25)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)
            x1 = x - radius
            x2 = x + radius

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)
            y1 = y - radius
            y2 = y + radius

            col_f = self.get_color_string(agent.color)
            if self.gc.DISPLAY_GRID:
                col_o = self.get_color_string((0, 0, 0))
            else:
                col_o = self.get_color_string(agent.color)
            circle = self.canvas.create_oval([x, y1, x2, y2], fill=col_f, outline=col_o)
            old_color = agent.color
            self.agent_shape_mapping.append((circle, agent, old_color))

    def update_cells(self):
        new_list = list()
        for (polygon, cell, color) in self.cell_shape_mapping:
            if cell.color != color:
                col = self.get_color_string(cell.color)
                self.canvas.itemconfig(polygon, fill=col)
                old_color = cell.color
                new_list.append((polygon, cell, old_color))
            else:
                new_list.append((polygon, cell, color))
            # Update grid drawing
            if self.gc.DISPLAY_GRID:
                col_o = self.get_color_string((0, 0, 0))
            else:
                col_o = self.get_color_string(cell.color)
            self.canvas.itemconfig(polygon, outline=col_o)
        self.cell_shape_mapping = new_list

    def update_agents(self):
        new_list = list()
        # Add agents that are new to the simulation.
        for agent in self.core.abm.new_agents:
            radius = int(agent.size / 0.9)

            horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
            offset = agent.y * (horiz / 2)
            x = int(agent.x * horiz) + int(offset)
            x1 = x - radius
            x2 = x + radius

            vert = self.gc.CELL_SIZE * 2 * (3 / 4)
            y = int(agent.y * vert)
            y1 = y - radius
            y2 = y + radius

            col_f = self.get_color_string(agent.color)
            col_o = self.get_color_string((0, 0, 0))
            circle = self.canvas.create_oval([x1, y1, x2, y2], fill=col_f, outline=col_o)
            old_color = agent.color
            self.agent_shape_mapping.append((circle, agent, old_color))
        self.core.abm.new_agents = list()

        # TODO: remove agents that are dead.
        # Update existing agents.
        for (oval, agent, color) in self.agent_shape_mapping:
            if agent.color != color:
                col = self.get_color_string(agent.color)
                self.canvas.itemconfig(oval, fill=col)
                color = agent.color
            if self.gc.RUN_SIMULATION and (agent.x != agent.prev_x or agent.y != agent.prev_y) :
                # Calculate position change
                horiz = self.gc.CELL_SIZE * 2 * (math.sqrt(3) / 2)
                offset1 = agent.y * (horiz / 2)
                offset2 = agent.prev_y * (horiz / 2)
                x1 = int(agent.x * horiz) + int(offset1)
                x2 = int(agent.prev_x * horiz) + int(offset2)
                vert = self.gc.CELL_SIZE * 2 * (3 / 4)
                y1 = int(agent.y * vert)
                y2 = int(agent.prev_y * vert)
                dx = x1 - x2
                dy = y1 - y2
                self.canvas.move(oval, dx, dy)
            new_list.append((oval, agent, color))
        self.agent_shape_mapping = new_list

    def clear_cell_shape_mapping(self):
        for (polygon, cell, old_color) in self.cell_shape_mapping:
            self.canvas.delete(polygon)
        self.cell_shape_mapping = list()

    def clear_agent_shape_mapping(self):
        for (oval, agent, old_color) in self.agent_shape_mapping:
            self.canvas.delete(oval)
        self.agent_shape_mapping = list()

    def render_frame(self):
        """Draws a new frame every N milliseconds"""
        self.update_cells()
        self.update_agents()
        if self.gc.RUN_SIMULATION:
            self.core.step_simulation()
        self.root.after(1, self.render_frame)

    def render_simulation(self):
        self.render_frame()
        self.root.mainloop()

    def get_color_string(self, triple):
        return '#%02x%02x%02x' % triple


class TkInputActions:

    def __init__(self, ui):
        self.gc = ui.gc
        self.core = ui.core
        self.root = ui.root
        self.ui = ui
        self.mx = 0
        self.my = 0

    def set_binds(self):
        self.root.bind('<space>', self.key_space)
        self.root.bind('s', self.key_s)
        self.root.bind('r', self.key_r)
        self.root.bind('q', self.key_q)
        self.root.bind('g', self.key_g)
        self.root.bind('<Button-1>', self.mouse_left)
        self.root.bind('<Button-2>', self.mouse_wheel)
        self.root.bind('<Button-3>', self.mouse_right)

    def key_space(self, event):
        self.core.gc.RUN_SIMULATION = not self.core.gc.RUN_SIMULATION
        if self.core.gc.RUN_SIMULATION:
            print(' < simulation resumed')
        else:
            print(' < simulation paused')

    def key_s(self, event):
        print(' < stepping simulation')
        self.core.step_simulation()

    def key_r(self, event):
        print(' < simulation reset')
        self.core.reset_simulation()
        self.ui.clear_cell_shape_mapping()
        self.ui.clear_agent_shape.mapping()
        self.ui.init_cell_shape_mapping()
        self.ui.init_agent_shape_mapping()

    def key_q(self, event):
        print(' < shutting down... Bye!')
        sys.exit()

    def key_g(self, event):
        self.gc.DISPLAY_GRID = not self.gc.DISPLAY_GRID
        if self.gc.DISPLAY_GRID:
            print(' > showing grid')
        else:
            print(' > hiding grid')

    def mouse_motion(self, event):
        self.mx = (event.x / self.core.gc.CELL_SIZE)
        self.my = (event.y / self.core.gc.CELL_SIZE)

    def mouse_left(self, event):
        print(' < left mouse button action')
        # Update current mouse coordinates
        self.mouse_motion(event)
        # Retrieve correct location coordinates.
        if self.core.gc.USE_HEX_CA:
            pos_x, pos_y = self.get_mouse_hex_coords()
        else:
            pos_x, pos_y = self.get_mouse_rect_coords()

        print(' < triggering cell action')
        self.core.ca.ca_grid[pos_x, pos_y].on_lmb_click(self.core.abm, self.core.ca)
        if self.gc.ONE_AGENT_PER_CELL:
            if (pos_x, pos_y) in self.core.abm.agent_locations:
                print(' < triggering agent action')
                self.core.abm.agent_locations[pos_x, pos_y].on_lmb_click(self.core.abm, self.core.ca)
        else:
            if (pos_x, pos_y) in self.core.abm.agent_locations:
                print(' < triggering agent action')
                for agent in self.core.abm.agent_locations[pos_x, pos_y]:
                    agent.on_lmb_click(self.core.abm, self.core.ca)

    def mouse_wheel(self, event):
        print(' < mouse wheel action')

    def mouse_right(self, event):
        print(' < right mouse button action')
        # Update current mouse coordinates.
        self.mouse_motion(event)
        # Retrieve correct location coordinates.
        if self.core.gc.USE_HEX_CA:
            pos_x, pos_y = self.get_mouse_hex_coords()
        else:
            pos_x, pos_y = self.get_mouse_rect_coords()

        print(' < triggering cell action')
        self.core.ca.ca_grid[pos_x, pos_y].on_rmb_click(self.core.abm, self.core.ca)
        if self.gc.ONE_AGENT_PER_CELL:
            if (pos_x, pos_y) in self.core.abm.agent_locations:
                # print(' < triggering agent action')
                self.core.abm.agent_locations[pos_x, pos_y].on_rmb_click(self.core.abm, self.core.ca)
        else:
            if (pos_x, pos_y) in self.core.abm.agent_locations:
                for agent in self.core.abm.agent_locations[pos_x, pos_y]:
                    # print(' < triggering agent action')
                    agent.on_rmb_click(self.core.abm, self.core.ca)

    def get_mouse_rect_coords(self):
        return math.floor(self.mx), math.floor(self.my)

    def get_mouse_hex_coords(self):
        """
        Retrieve the current mouse cursor coordinates relative to the hexagonal grid.
        This method is only needed for hexagonal cellular automata.
        :return: Hexagonal q,r coordinates of the mouse cursor.
        """
        _q = (self.mx * math.sqrt(3) / 3 - self.my / 3)  # / self.core.gc.CELL_SIZE
        _r = self.my * 2 / 3  # / self.core.gc.CELL_SIZE
        cell_q, cell_r = CAHex.hex_round(_q, _r)
        return cell_q, cell_r