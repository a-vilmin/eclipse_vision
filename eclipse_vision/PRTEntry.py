# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

import numpy as np


class PRTEntry():
    """Class for holding array of cell data parsed out of PRT file at
    individual timesteps
    :self.cells: Numpy array sized to dimensions of Eclipse simulation
    :self.time: Timestep for simulation
    :self.name: Name of simulation"""

    def __init__(self, dx, dy, dz):
        """cells initialized in order: z, y, x and are required args"""

        self.cells = np.empty((dz, dy, dx))
        self.time = 0.0
        self.name = ''

    def read_type_info(self, line):
        """parses timestep and name info from line in PRT"""
        break_up = line.strip().split()

        # title of simulation proceeds timestep. code finds all parts of
        # title and parses the timestep out.
        try:
            for each in break_up[1:]:
                try:
                    t = float(each)
                    self.time = t
                    self.name = self.name[:-1]  # get rid of last underscore
                    break
                except ValueError:
                    self.name += each+"_"
        except:
            print("Incorrect format passed to PRTEntry object. Grid data" +
                  "format not recognized!")

    def read_cell_info(self, f, pbar):
        """reads cells from PRT into np array. requires progress bar as arg"""
        curr_x = []  # PRT has X value defined at top of collumns

        for line in f:
            pbar.update(1)
            if line.startswith(" (I,  J,  K)"):
                curr_x = self._reset_i(line)
            elif line.startswith(" (*,"):
                self._read_points(curr_x, line)
            elif line.strip() == "":
                continue
            else:
                return

    def _read_points(self, curr_x, line):
        chopped = line.split(")")
        y, z = chopped[0].split(',')[1:]
        y, z = int(y), int(z)
        n_values = chopped[1].split()

        for x in curr_x:
            n = n_values.pop(0)
            self.cells[z-1][y-1][x-1] = n

    def _reset_i(self, line):
        """for getting new x values when collumns change"""
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

    test = PRTEntry(100, 100, 100)
    test.read_type_info(types.readline())

    for line in prt:
        if line.startswith(" (I,  J,  K)"):
            test_list = test._reset_i(line)
            test.read_cell_info(prt, test_list)
            break

    print("Type name is: " + test.name)
    print("Type time is: " + str(test.time))
    print(test.cells[99][0][0])

    types.close()
    prt.close()
