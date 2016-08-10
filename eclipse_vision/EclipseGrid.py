# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

import numpy as np
from SectionReader import SectionReader
from os import path
import sys
from collections import defaultdict


class EclipseGrid(SectionReader):
    """Class for handling include files for PERM and parsing include files
    :self.equals: Dictionary for equals section (DX, DY, DZ are most used)
    :self.include_file: string for file DATA file references
    :self.includes: dictionary to numpy arrays parsed from include_file
    :self.directory: string of Eclipse project directory"""

    def __init__(self, directory):
        """init all variables empty except directory string (required arg)"""

        self.equals = {}
        self.include_file = ""
        self.includes = defaultdict(lambda: np.array(1))  # arr is place holder
        self.directory = directory

    def set_dims(self, dim_tuple):
        """resizes self.includes numpy array arguments to dims of model"""
        dx, dy, dz = dim_tuple
        self.includes = defaultdict(lambda: np.empty((dz, dy, dx)))

    def handle(self, f):
        for line in f:
            if super(EclipseGrid, self)._section_done(line):
                return

            if line.startswith('EQUALS'):
                self._equals_handler(f)
            elif line.startswith('INCLUDE'):
                self.include_file = path.join(self.directory, next(f).strip())

                if not self._include_handler():
                    self._include_fail()

    def _equals_handler(self, f):
        """handles EQUALS section"""
        for line in f:
            if line.startswith("/"):
                return
            else:
                line = line.strip().split()
                self.equals[line[0]] = float(line[1])

    def _include_handler(self):
        """parses include file name and parses into numpy array"""
        try:
            grid_data = open(self.include_file)
            grid_data.readline()  # First line is garbage
        except:
            # file opening error handling

            ex_ty, ex, tb = sys.exc_info()
            print(ex_ty+" because "+self.include_file+" cannot be " +
                  "located in directory.")
            return False

        # actual parsing code
        for line in grid_data:
            line = line.strip().replace("'", "").split()

            if not line or line[0] == '/' or line[0] == 'EQUALS':
                continue
            elif line[0] == 'COPY':
                break
            else:
                name, val, x = line[0:3]
                y, z = (line[4], line[6])
                self.includes[name][int(z)-1][int(y)-1][int(x)-1] = float(val)
        return True

    def _include_fail(self):
        new_name = raw_input("Please specify location of "+self.include_file)
        self.include_file = new_name

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
