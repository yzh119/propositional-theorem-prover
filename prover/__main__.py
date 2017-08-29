import sys

from .slover import *
from .parser import *

args = sys.argv

assert len(args) == 2, "Invalid format"
sequent = args[1]

tree = parse_string(sequent, "SEQ")

print(tree)
print(bfs_slover(tree))
