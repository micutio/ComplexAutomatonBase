"""
Exemplary main module of the Complex Automaton Base.
"""

import cab.global_constants as cab_gc
import cab.complex_automaton as cab_sys

__author__ = 'Michael Wagner'

if __name__ == '__main__':
    GC = cab_gc.GlobalConstants()
    simulation = cab_sys.ComplexAutomaton(GC)
    simulation.run_main_loop()
