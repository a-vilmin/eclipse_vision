from SectionReader import SectionReader
from collections import defaultdict


class EclipseGrid(SectionReader):
    def __init__(self):
        self.equals = {}
        self.include_file = ""
        self.perms = defaultdict(list)

    class PermCell():
        def __init__(self, x, y, z, val):
            self.x = x
            self.y = y
            self.z = z
            self.val = val
        
    def handle(self, f):
        for line in f:
            if super(EclipseGrid, self)._section_done(line):
                return

            if line.startswith('EQUALS'):
                self._equals_handler(f)
            elif line.startswith('INCLUDE'):
                self.include_file = next(f).strip()
                self._include_handler()

    def _equals_handler(self, f):
        for line in f:
            if line.startswith("/"):
                return
            else:
                line = line.split()
                self.equals[line[0]] = float(line[1])

    def _include_handler(self):
        grid_data = open(self.include_file)
        grid_data.readline()

        for line in grid_data:
            line = line.strip().replace("'", "").split()

            if not line or line[0] == '/':
                continue
            elif line[0] == 'COPY':
                return
            else:
                direction, val, x = line[:3]
                y, z = (line[4], line[6])
                cell = EclipseGrid.PermCell(x, y, z, val)
                self.perms[direction] += [cell]
                
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
