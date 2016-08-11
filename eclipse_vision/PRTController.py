# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from __future__ import print_function
from PRTEntry import PRTEntry
from collections import defaultdict
from tqdm import tqdm
import sys


class PRTController(object):
    """class for parsing PRT file output from Eclipse/Petrel
    :self.prt_file: PRT file string
    :self.runs: defaultdict of lists containing the VTK grids for each
                timestep, referrenced by search term/poro/perms
    :self.f_len: len of PRT file. Used to get better count for progress bar.
    :self.x, y, z: dimensions of simulation grid"""

    def __init__(self, prt):
        """initializes all variables and runs self._get_len. requires prt string
        as arg"""

        self.prt_file = prt
        self.runs = defaultdict(list)
        self.f_len = self._get_len(prt)

    def _get_len(self, fname):
        """gets number of lines in prt. prints periods to show progress."""

        with open(fname) as f:
            sys.stdout.write('Opening files...')
            sys.stdout.flush()
            for i, l in enumerate(f):
                if i % 1000000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                pass
        print("")
        return i + 1

    def set_dims(self, dim_tup):
        self.x, self.y, self.z = dim_tup

    def add_runs(self, terms):
        """searches for term and creates PRTEntry for all data in term"""
        opened = open(self.prt_file)

        with tqdm(total=self.f_len) as pbar:
            pbar.set_description("Searching PRT")
            for line in opened:
                if line.strip().startswith(terms):
                    term = self._det_term(line, terms)
                    entry = PRTEntry(self.x, self.y, self.z)
                    entry.read_type_info(line)

                    self._skip_lines(opened, term, pbar)
                    entry.read_cell_info(opened, pbar)

                    self.runs[term] += [entry]
                pbar.update(1)
        opened.close()

    def _skip_lines(self, f, term, pbar):
        for line in f:
            pbar.update(1)
            if line.strip().startswith(term):
                return

    def _det_term(self, line, terms):
        """determines term that section is referring to"""
        for each in terms:
            if line.strip().startswith(each):
                return each

    def write_timesteps(self, txt_file):
        for term, runs in self.runs.iteritems():
            txt_file.write("The sequence for " + term + '\n')
            for run in runs:
                txt_file.write(str(run.time) + "  ")
            txt_file.write('\n')

if __name__ == '__main__':
    from sys import argv

    test = PRTController(argv[1])
    test.set_dims((100, 100, 100))
    test.add_runs(("SGAS", "PRESSURE"))

    txt = open("timesteps.txt", 'w')

    test.write_timesteps(txt)
