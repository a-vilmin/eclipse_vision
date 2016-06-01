from SectionReader import SectionReader


class EclipseGrid(SectionReader):
    def __init__(self):
        self.equals = {}
        self.include_file = ""

    def handle(self, f):
        for line in f:
            if super(EclipseGrid, self)._section_done(line):
                return

            if line.startswith('EQUALS'):
                self._equals_handle(f)
            elif line.startswith('INCLUDE'):
                self.include_file = next(f).strip('\n')
                self._include_handle(f)

    def _equals_handle(self, f):
        for line in f:
            if line.startswith("/"):
                return
            else:
                line = line.split()
                self.equals[line[0]] = float(line[1])

    def _include_handle(self, f):
        return

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
