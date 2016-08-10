# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31
from SectionReader import SectionReader
# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31


class RunSpec(SectionReader):
    """Class for parsing RUNSPEC sections of DATA files from Eclipse output
    :self.title: Title of entire simulation
    :self.x_dim, y_dim, z_dim: 3D dimensions of simulation grid"""

    def __init__(self):
        self.title = ""
        self.x_dim = 0
        self.y_dim = 0
        self.z_dim = 0

    def _convert(self, x, y, z):
        """assigns int values to self.dim values from strings"""
        self.x_dim = int(x)
        self.y_dim = int(y)
        self.z_dim = int(z)

    def handle(self, f):
        for line in f:
            if super(RunSpec, self)._section_done(line):
                return

            if line.startswith('TITLE'):
                self.title = next(f).strip('\n')
            elif line.startswith('DIMENS'):
                f.next()
                line = next(f)
                dims = line.split()
                x, y, z = dims[:3]
                self._convert(x, y, z)


if __name__ == '__main__':
    from sys import argv

    tester = RunSpec()
    f = open(argv[1])
    f.readline()
    tester.handle(f)

    print(tester.title)
    print(str(tester.x_dim))
    print(str(tester.y_dim))
    print(str(tester.z_dim))
