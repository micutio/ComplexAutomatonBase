# CAB libraries
from cab.complex_automaton import ComplexAutomaton
from cab.global_constants import GlobalConstants
import cab.util.logging as cab_log

# External libraries
import unittest


class GeneralTestCase(unittest.TestCase):
    """
    Tests for CAB System
    TODO: Add function to advance the ca by n steps and compare the output with
          expected values.
    """

    def test_startup(self):
        cab_log.set_log_trace()
        gc = GlobalConstants()
        simulation = ComplexAutomaton(gc)
        self.assertTrue(simulation)


if __name__ == '__main__':
    unittest.main()
