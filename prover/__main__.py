import sys

from .solver import *
from .parser import *

args = sys.argv

assert len(args) == 2, "Invalid format"
sequent = args[1]

tree = parse_string(sequent, "SEQ")

provable, history = bfs_solver(tree)

print(provable)
if provable:
    for approach, sequent in reversed(history):
        print(approach, sequent)
