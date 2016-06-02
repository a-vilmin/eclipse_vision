# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from RunSpec import RunSpec
from EclipseGrid import EclipseGrid
from Region import Region


class MainReader():
    def __init__(self, f):

        self.run_spec = RunSpec()
        self.grid = EclipseGrid()
        self.regions = Region()
        try:
            self.read_f = f
        except NameError:
            print("Cannot open file")

    def file_read(self):
        for line in self.read_f:
            if line.startswith('RUNSPEC'):
                self.run_spec.handle(self.read_f)
            elif line.startswith('GRID'):
                self.grid.handle(self.read_f)

if __name__ == '__main__':
    from sys import argv
    f = open(argv[1])
    test = MainReader(f)

    test.file_read()
    print(test.run_spec.title)
