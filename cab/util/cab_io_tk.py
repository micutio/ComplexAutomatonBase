"""
This module contains a CAB io implementation in TkInter.
"""

# External library imports.
import math
import sys
from tkinter import Tk, Canvas

# Internal Simulation System component imports.
from cab.ca.cab_ca_hex import CAHex

__author__ = 'Michael Wagner'


class TkIO:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, cab_core):
        self.root = Tk()
        self.gc = gc
        self.core = cab_core
        self.width = 0
        self.height = 0
        self.root.title("Complex Automaton")
        self.canvas = None
        self.cell_map = {}
        self.agent_map = {}

        self.input_actions = TkInputActions(gc, cab_core, self.canvas)
        self.init_canvas()
        self.init_cells()
        self.init_agents()

        self.input_actions = TkInputActions(self.gc, self.core, self.root)
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

    def init_cells(self):
        for k, v in list(self.core.ca.ca_grid.items()):
            corners_list = [i for tupl in v.get_corners() for i in tupl]
            col_f = '#%02x%02x%02x' % v.color
            col_o = '#%02x%02x%02x' % (0, 0, 0)
            polygon = self.canvas.create_polygon(corners_list, fill=col_f, outline=col_o)
            old_color = v.color
            self.cell_map[k] = (polygon, v, old_color)

    def init_agents(self):
        if self.gc.ONE_AGENT_PER_CELL:
            for k,v in list(self.core.abm.agent_locations.items()):
                x1 = v.x - self.core.gc.CELL_SIZE
                y1 = v.y - self.core.gc.CELL_SIZE
                x2 = v.x + self.core.gc.CELL_SIZE
                y2 = v.y + self.core.gc.CELL_SIZE
                col_f = '#%02x%02x%02x' % v.color
                col_o = '#%02x%02x%02x' % (0, 0, 0)
                circle = self.canvas.create_oval([x1, y1, x2, y2], fill=col_f, outline=col_o)
                old_color = v.color
                self.agent_map[k] = (circle, v, old_color)
        else:
            for k,v in list(self.core.abm.agent_locations.items()):
                for agent in v:
                    x1 = agent.x - self.core.gc.CELL_SIZE
                    y1 = agent.y - self.core.gc.CELL_SIZE
                    x2 = agent.x + self.core.gc.CELL_SIZE
                    y2 = agent.y + self.core.gc.CELL_SIZE
                    col_f = '#%02x%02x%02x' % agent.color
                    col_o = '#%02x%02x%02x' % (0, 0, 0)
                    circle = self.canvas.create_oval([x1, y1, x2, y2], fill=col_f, outline=col_o)
                    old_color = agent.color
                    if k in self.agent_map:
                        self.agent_map[k].append((circle, agent, old_color))
                    else:
                        self.agent_map[k] = [(circle, v, old_color)]

    def update_cells(self):
        for k, v in list(self.cell_map.items()):
            if v[1].color != v[2]:
                col = '#%02x%02x%02x' % v[1].color
                self.canvas.itemconfig(v[0], fill=col)
                old_color = v[1].color
                self.cell_map[k] = (v[0], v[1], old_color)

    def update_agents(self):
        if self.gc.ONE_AGENT_PER_CELL:
            for k, v in self.agent_map:
                # TODO: Take care of new agents.

                # Take care of deleted agents.
                if k not in self.core.abm.agent_locations:
                    self.canvas.delete(v[0])
                    self.agent_map.pop(k)
                    continue
                if v[1].x != v[1].prev_x or v[1].y != v[1].prev_y:
                    dx = (v[1].x - v[1].prev_x)
                    dy = (v[1].y - v[1].prev_y)
                    self.canvas.move(v[0], dx, dy)
                if v[1].color != v[2]:
                    col = '#%02x%02x%02x' % v[1].color
                    self.canvas.itemconfig(v[0], fill=col)
                    old_color = v[1].color
                    self.agent_map[k] = (v[0], v[1], old_color)
        else:
            for k, v in self.agent_map:
                for vv in v:
                    if vv[1].x != vv[1].prev_x or vv[1].y != vv[1].prev_y:
                        dx = (vv[1].x - vv[1].prev_x)
                        dy = (vv[1].y - vv[1].prev_y)
                        self.canvas.move(vv[0], dx, dy)
                    if vv[1].color != vv[2]:
                        col = '#%02x%02x%02x' % vv[1].color
                        self.canvas.itemconfig(vv[0], fill=col)
                        old_color = vv[1].color
                        self.agent_map[k] = (vv[0], vv[1], old_color)

    def render_frame(self):
        """Draws a new frame every N milliseconds"""
        if self.gc.RUN_SIMULATION:
            self.core.step_simulation()
        self.update_cells()
        self.update_agents()
        self.root.after(1, self.render_frame)

    def render_simulation(self):
        self.render_frame()
        self.root.mainloop()


class TkInputActions:

    def __init__(self, gc, cab_core, root):
        self.gc = gc
        self.core = cab_core
        self.root = root
        self.mx = 0
        self.my = 0

    def set_binds(self):
        self.root.bind('<space>', self.key_space)
        self.root.bind('s', self.key_s)
        self.root.bind('r', self.key_r)
        self.root.bind('q', self.key_q)
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

    def key_q(self, event):
        print(' < shutting down... Bye!')
        sys.exit()

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