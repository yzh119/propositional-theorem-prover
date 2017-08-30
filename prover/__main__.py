import sys

from .solver import *
from .parser import *

args = sys.argv

assert len(args) == 2, "Invalid format"
sequent = args[1]

tree = parse_string(sequent, "SEQ")
print(tree)

provable = bfs_solver(tree)

if provable:
    print('QED')

print(provable)
