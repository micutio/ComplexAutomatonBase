#!/usr/bin/env bash

echo "-> unpacking distribution"
mkdir inst
tar -xf dist/ComplexAutomatonBase-0.9.tar.gz --directory inst/
cd inst/ComplexAutomatonBase-0.9
echo "-> installing test distribution"
sudo python3 setup.py install
