"""
This module contains the random number generator used by the CAB system.
"""


from random import Random
from typing import Any

__author__ = "Michael Wagner"


m_rng = Random()


def get_RNG() -> Random:
    return m_rng


def seed_RNG(seed_value: Any):
    m_rng.seed(seed_value)
