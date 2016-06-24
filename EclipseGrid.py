# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

import numpy as np
from SectionReader import SectionReader
from copy import deepcopy
from os import path


class EclipseGrid(SectionReader):
    def __init__(self, directory):
        self.equals = {}
        self.include_file = ""
        self.perms = np.array(1)
        self.directory = directory

    def set_dims(self, dim_tuple):
        dz, dy, dx = dim_tuple
        self.perms = np.empty((dz, dy, dx))

    def handle(self, f):
        for line in f:
            if super(EclipseGrid, self)._section_done(line):
                return
            
            if line.startswith('EQUALS'):
                self._equals_handler(f)
            elif line.startswith('INCLUDE'):
                self.include_file = path.join(self.directory, next(f).strip())
                self._include_handler()

    def _equals_handler(self, f):
        for line in f:
            if line.startswith("/"):
                return
            else:
                line = line.strip().split()
                self.equals[line[0]] = float(line[1])

    def _include_handler(self):
        try:
            grid_data = open(self.include_file)
            grid_data.readline()  # First line is garbage
        except NameError:
            print("File cannot be opened.")
            return

        for line in grid_data:
            line = line.strip().replace("'", "").split()

            if not line or line[0] == '/':
                continue
            elif line[0] == 'COPY':
                return
            else:
                val, x = line[1:3]
                y, z = (line[4], line[6])
                self.perms[int(z)-1][int(y)-1][int(x)-1] = float(val)

    def _copy(self, f):
        for line in f:
            line = line.strip().split()

            if not line or line[0] == '/':
                continue
            else:
                self.perms[line[1]] = deepcopy(self.perms[line[0]])

if __name__ == '__main__':
    from sys import argv

    f = open(argv[1])
    f.readline()  # read thru first lines

    test = EclipseGrid()

    test.handle(f)  # read thru section RUNSPEC
    test.handle(f)
    print(test.include_file)

    for key, value in test.equals.iteritems():
        print(key + " " + str(value))

    for key, value in test.perms.iteritems():
        leng = len(value)
        print(key + " " + str(leng) + str(value[leng-3045]))
