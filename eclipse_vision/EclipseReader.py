# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from RunSpec import RunSpec
from EclipseGrid import EclipseGrid


class EclipseReader():
    """Class for handling the Eclipse *.data file output.
    :self.read_f: DATA file string
    :self.run_spec: RunSpec object
    :self.grid: EclipseGrid object"""

    def __init__(self, f, direct):
        """initializes with filename string and project directory string"""
        self.read_f = f
        self.run_spec = RunSpec()
        self.grid = EclipseGrid(direct)

    def file_read(self):
        """reads throught the data file"""
        f = open(self.read_f)
        for line in f:
            if line.startswith('RUNSPEC'):
                self.run_spec.handle(f)
                self.grid.set_dims(self.dims())
            elif line.startswith('GRID'):
                self.grid.handle(f)

    def dims(self):
        """returns dimensions in tuple formatted (X, Y, Z)"""
        return (self.run_spec.x_dim, self.run_spec.y_dim, self.run_spec.z_dim)

    def spacing(self):
        """returns spacing in tuple formatted (DX, DY, DZ)"""
        return (self.grid.equals['DX'], self.grid.equals['DY'],
                self.grid.equals['DZ'])

if __name__ == '__main__':
    from sys import argv
    from os import getcwd
    f = argv[1]
    test = EclipseReader(f, getcwd()+"\\vG_1")

    test.file_read()
    print(test.run_spec.title)
