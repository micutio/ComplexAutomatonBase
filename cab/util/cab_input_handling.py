"""
This module contains a generic InputHandler which handles all keyboard and mouse input to the simulation.
"""

# External library imports.
import pygame
import sys
import math


__author__ = 'Michael Wagner'


class InputHandler:
    """
    This class incorporates all methods necessary for controlling the simulation.
    """
    def __init__(self, cab_system):
        self.mx = 0
        self.my = 0
        if cab_system is None:
            self.sys = None
        else:
            self.sys = cab_system

    def clone(self, cab_sys):
        return InputHandler(cab_sys)

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
        self.mx = (self.mx / self.sys.gc.CELL_SIZE)
        self.my = (self.my / self.sys.gc.CELL_SIZE)
        self.custom_mouse_motion()

    def custom_mouse_motion(self):
        """
        Overwrite to define additional actions on mouse movement.
        """
        pass

    def custom_mouse_action(self, button):
        """
        Processing Mouse action. Overwrite to extend!
        """
        # Click on left mouse button.
        if button == 1:
            pass

        # Click on right mouse button
        elif button == 3:
            pass

    def default_keyboard_action(self, active_key):
        """
        Method to process all the keyboard inputs.
        This is not supposed to be overwritten.
        """
        if active_key == pygame.K_SPACE:
            self.sys.gc.RUN_SIMULATION = not self.sys.gc.RUN_SIMULATION
            if self.sys.gc.RUN_SIMULATION:
                print(" < simulation resumed")
            else:
                print(" < simulation paused")

        # Simulation Standard: 'r' resets the simulation
        if active_key == pygame.K_r:
            self.sys.reset_simulation()
            print(" < simulation reset")

        # Simulation Standard: 's' advances the simulation by one step
        if active_key == pygame.K_s:
            self.sys.step_simulation()
            self.sys.render_simulation()
            print(" < stepping simulation")

    def custom_keyboard_action(self, active_key):
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
        _q = (self.mx * math.sqrt(3) / 3 - self.my / 3)  # / self.sys.gc.CELL_SIZE
        _r = self.my * 2 / 3  # / self.sys.gc.CELL_SIZE
        cell_q, cell_r = InputHandler.hex_round(_q, _r)
        return cell_q, cell_r

    @staticmethod
    def hex_round(q, r):
        return InputHandler.cube_to_hex(*InputHandler.cube_round(*InputHandler.hex_to_cube(q, r)))

    @staticmethod
    def cube_round(x, y, z):
        rx = round(x)
        ry = round(y)
        rz = round(z)
        dx = abs(rx - x)
        dy = abs(ry - y)
        dz = abs(rz - z)

        if dx > dy and dx > dz:
            rx = -ry - rz
        elif dy > dz:
            ry = -rx - rz
        else:
            rz = -rx - ry

        return rx, ry, rz

    @staticmethod
    def cube_to_hex(x, y, z):
        return x, y

    @staticmethod
    def hex_to_cube(q, r):
        z = -q - r
        return q, r, z
