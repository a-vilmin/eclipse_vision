class PRTEntry():

    # class methods
    def __init__(self):
        self.cells = []
        self.time = 0.0
        self.name = ''

    def read_type_info(self, line):
        break_up = line.strip().split()
        try:
            for each in break_up[1:]:
                try:
                    t = float(each)
                    self.time = t
                    break
                except ValueError:
                    self.name += each
        except:
            print("Incorrect format passed to PRTEntry object. Grid data" +
                  "format not recognized!")

    def read_cell_info(self, f, test_list=[]):  # testing; default list empty
        curr_x = test_list
        for line in f:
            if line.startswith(" (I,  J,  K)"):
                curr_x = self._reset_i(line)
            elif line.startswith("-------"):
                return
            elif line.strip() == "":
                continue
            else:
                self._read_points(curr_x, line)

    def _read_points(self, curr_x, line):
        chopped = line.split(")")
        n_values = chopped[1].split()

        while len(n_values):
            n = float(n_values.pop(0))
            self.cells += [n]

    def _reset_i(self, line):

        chopped = line.strip().split()
        ret_val = []

        for each in chopped[4:]:
            ret_val += [int(each)]

        return ret_val


if __name__ == '__main__':
    from sys import argv

    # use argv[1] for the parsed file to read_type_info
    types = open(argv[1])
    prt = open(argv[2])

    test = PRTEntry()
    test.read_type_info(types.readline())

    for line in prt:
        if line.startswith(" (I,  J,  K)"):
            test_list = test._reset_i(line)
            test.read_cell_info(prt, test_list)
            break

    print("Type name is: " + test.name)
    print("Type time is: " + str(test.time))
    print("Number of Cells: " + str(len(test.cells)))

    types.close()
    prt.close()
