#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
cpu.load()
cpu.run()
# print("first arg", sys.argv[0])
# print("second arg", sys.argv[1])