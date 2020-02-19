# ComplexAutomatonBase [![travis badge](https://travis-ci.org/Micutio/ComplexAutomatonBase.svg?branch=master)](https://travis-ci.org/Micutio/ComplexAutomatonBase)

Minimalistic Framework for Complex Automata

## About

The Complex Automaton Base, or CAB in short, offers a foundation for agent-based simulations. These simulations take place in a two-dimensional world that consists of either a rectangular or a hexagonal grid. Such worlds can either have a life on their own or be populated with so-called agents which occupy one cell at a time but can also be outfitted to move across the world's grid.

With only these two elements, grid world and agents, the framework is capable of simulating an astounding variety of real life ecosystems. Swarm animals like ants or bees, natural phenomena like forest fires or human behavior and man-made ecosystems like urban sprawl and land use development are all fields that can be explored by using complex automata.

This project might be interesting for you if:

- you want to explore and play around with ideas about systems that exhibit decentralization and organic growth

- you like to build and play around with artificial worlds

- you're learning how to write programs in Python and are looking for simple yet fascinating little projects to start off with and apply what you've learned

## Installation

Use the `setup.sh` script to install and uninstall (`setup.sh -rm`) on your local system.

## How to use it

The repository over at [CAB-Simulations](https://github.com/micutio/CAB_Simulations) contains some example applications which can be used to start off and explore the capabilities of the framework. To further help you along, have a look a the templates, which can give you a head start in programming new scenarios. There is a minimalistic one, for small applications that fit into one single file, and a slightly more advanced example with the recommended project structure for more complex simulations.

A fully fleshed out tutorial will be added in the future.

## TODOs

- type annotations in the source code, for better readability
- create unit tests
- use dataclass decorator where appropriate
- look into zipapp and other ways of packing & distribution
- use iterators and generators for querying cells and agents
- convert this todo-list into github issues
- consult <https://docs.python.org/3/library/profile.html> to profile simulation
