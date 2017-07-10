"""
This module contains the random number generator used by the CAB system.
"""


from random import Random


__author__ = "Michael Wagner"


m_rng = Random()

def get_RNG():
    return m_rng

def seed_RNG(seed_value):
    m_rng.seed(seed_value)
