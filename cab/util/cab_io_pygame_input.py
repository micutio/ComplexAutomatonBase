"""
This module contains a generic InputHandler which handles all keyboard and mouse input to the simulation.
"""

# External library imports.
import pygame
import sys
import math

# Internal Simulation System Component imports.
from cab.ca.cab_ca_hex import CAHex
from cab_system import ComplexAutomaton

__author__ = 'Michael Wagner'


class InputHandler:
    """
    This class incorporates all methods necessary for controlling the simulation.
    """
    def __init__(self, cab_core: ComplexAutomaton):
        self.mx = 0
        self.my = 0
        if cab_core is None:
            self.core = None
        else:
            self.core = cab_core

    def clone(self, cab_core):
        return InputHandler(cab_core)

    def process_input(self):
        """
        Method to process input. Do not overwrite!
        """
        for event in pygame.event.get():
            # The 'x' on the window is clicked
            if event.type == pygame.QUIT:
                sys.exit()
            # Mouse motion
            elif event.type == pygame.MOUSEMOTION:
                self.default_mouse_motion()
            # Mouse action
            elif event.type == pygame.MOUSEBUTTONUP:
                self.custom_mouse_action(event.button)
            # Keyboard key is pressed
            elif event.type == pygame.KEYUP:
                # space bar is pressed
                self.default_keyboard_action(event.key)
                self.custom_keyboard_action(event.key)

    def default_mouse_motion(self):
        """
        Method to track mouse motion.
        Overwrite custom_mouse_motion to add functionality here.
        """
        self.mx, self.my = pygame.mouse.get_pos()
        self.mx = (self.mx / self.core.gc.CELL_SIZE)
        self.my = (self.my / self.core.gc.CELL_SIZE)
        self.custom_mouse_motion()

    def custom_mouse_motion(self):
        """
        Overwrite to define additional actions on mouse movement.
        """
        pass

    def custom_mouse_action(self, button: int):
        """
        Processing Mouse action. Overwrite to extend!
        """
        if self.core.gc.USE_HEX_CA:
            pos_x, pos_y = self.get_mouse_hex_coords()
        else:
            pos_x, pos_y = self.get_mouse_rect_coords()

        # Click on left mouse button.
        if button == 1:
            # Check if agents at this location and trigger their lmb click method.
            if (pos_x, pos_y) in self.core.abm.agent_locations:
                if self.core.gc.ONE_AGENT_PER_CELL:
                    self.core.abm.agent_locations[pos_x, pos_y].on_lmb_click()
                else:
                    for agent in self.core.abm.agent_locations[pos_x, pos_y]:
                        agent.on_lmb_click()
            # Trigger cell method.
            self.core.ca.ca_grid[pos_x, pos_y].on_lmb_click()

        # Click on right mouse button.
        elif button == 3:
            # Check if agents at this location and trigger their rmb click method.
            if (pos_x, pos_y) in self.core.abm.agent_locations:
                if self.core.gc.ONE_AGENT_PER_CELL:
                    self.core.abm.agent_locations[pos_x, pos_y].on_rmb_click()
                else:
                    for agent in self.core.abm.agent_locations[pos_x, pos_y]:
                        agent.on_lmb_click()
            # Trigger cell method.
            self.core.ca.ca_grid[pos_x, pos_y].on_rmb_click()

    def default_keyboard_action(self, active_key: int):
        """
        Method to process all the keyboard inputs.
        This is not supposed to be overwritten.
        """
        if active_key == pygame.K_SPACE:
            self.core.gc.RUN_SIMULATION = not self.core.gc.RUN_SIMULATION
            if self.core.gc.RUN_SIMULATION:
                print(' < simulation resumed')
            else:
                print(' < simulation paused')

        # Simulation Standard: 'r' resets the simulation.
        if active_key == pygame.K_r:
            self.core.reset_simulation()
            print(' < simulation reset')

        # Simulation Standard: 's' advances the simulation by one step.
        if active_key == pygame.K_s:
            self.core.step_simulation()
            print(' < stepping simulation')

        # Simulation Standard: 'q' closes the simulation and visualization window.
        if active_key == pygame.K_q:
            print(' < shutting down simulation')
            sys.exit()

    def custom_keyboard_action(self, active_key: int):
        """
        Customizable Method to process keyboard inputs.
        Overwrite this method to add more inputs.
        """
        pass

    # Additional utility methods for hexagonal cellular automata.

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
        cell_q, cell_r = CAHex.hex_round(int(_q), int(_r))
        return cell_q, cell_r

