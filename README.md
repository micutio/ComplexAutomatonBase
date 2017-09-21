# ComplexAutomatonBase
Minimalistic Framework for Complex Automata [![Build Status](https://travis-ci.org/travis-ci/travis-web.svg?branch=master)](https://travis-ci.org/travis-ci/travis-web)

## About

The **C**omplex **A**utomaton **B**ase offers a foundation for agent-based simulations.
These simulations take place in a two-dimensional world that consists of either
a rectangular or a hexagonal grid. Such worlds can either have a life on their
own or be populated with so-called agents which occupy one cell at a time but
can also be outfitted to move across the world's grid.

With only these two elements, grid world and agents, the framework is capable
of simulating an astounding variety of real life ecosystems. Swarm animals like
ants or bees, natural phenomena like forest fires or human behavior and man-made
ecosystems like urban sprawl and land use development are all fields that can be
explored by using complex automata.


## Is this interesting for me?

This project is definitely for you if:

* you want to explore and play around with ideas about systems that exhibit decentralization
and organic growth

* you like to build and play around with artificial worlds

* you're learning how to write programs in Python and are looking for simple
yet fascinating little projects to start off with and apply what you've learned

## Installation

Use the shell scripts to pack and install the CA Framework.
Optionally run 1_pack_dist.sh to create a distributable package or use the
.tar.gz file in the dist dist subfolder.

Then run 2_install_dist.sh to install the library into your local python directory.

Import ComplexAutomatonBase in your scripts by using "import cab"

To remove, execute 3_uninst_dist_solus.sh or 3_uninst_dist_ubuntu.sh, depending on your operating system.
This will be changed in the future to make the install and uninstall process operating system agnostic.

## How to use it

The repository over at [CAB-Simulations](https://github.com/micutio/CAB_Simulations)
contains a small number of example applications which can be used to start off
and explore the capabilities of the framework. To further help you along, have
a look a the templates, which can give you a head start in programming new
scenarios. There is a minimalistic one, for small applications that fit into
one single file, and a slightly more advanced example with the recommended
project structure for more complex simulations.

A fleshed out tutorial will be added eventually of course.
