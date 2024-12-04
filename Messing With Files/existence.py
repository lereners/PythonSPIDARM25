# files/existence.py
from pathlib import Path
p = Path('dadams.txt')
path = p.parent.absolute()
print(p.is_file())        # True
print(path)               # /Users/something
print(path.is_dir())      # True
q = Path('/Users/cnavarro/Documents')
print(q.is_dir())         # True
import os
# choose your dir path
path = '/Users/cnavarro/Documents'

# store files in a list
list = []

with os.scandir(path) as it:
    for entry in it:
        if entry.is_file() and entry.name.endswith('.mov'):
            list.append(entry.name)

# Print the list of files
for f in list:
    print(f)