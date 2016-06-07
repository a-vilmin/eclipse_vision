# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from RunSpec import RunSpec
from EclipseGrid import EclipseGrid
from Region import Region


class EclipseReader():
    def __init__(self, f):

        try:
            self.read_f = f
        except NameError:
            print("Cannot open file")
            return

        self.run_spec = RunSpec()
        self.grid = EclipseGrid()
        self.regions = Region()

    def file_read(self):
        for line in self.read_f:
            if line.startswith('RUNSPEC'):
                self.run_spec.handle(self.read_f)
            elif line.startswith('GRID'):
                self.grid.handle(self.read_f)

    def dims(self):
        return (self.run_spec.x_dim, self.run_spec.y_dim, self.run_spec.z_dim)

    def spacing(self):
        return (self.grid.equals['DX'], self.grid.equals['DY'],
                self.grid.equals['DZ'])

if __name__ == '__main__':
    from sys import argv
    f = open(argv[1])
    test = EclipseReader(f)

    test.file_read()
    print(test.run_spec.title)
