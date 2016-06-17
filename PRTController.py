from __future__ import print_function
from PRTEntry import PRTEntry
from collections import defaultdict
from tqdm import tqdm
import sys


class PRTController(object):

    def __init__(self, prt):
        self.prt_file = prt
        self.runs = defaultdict(list)
        self.f_len = self._get_len(prt)

    def _get_len(self, fname):
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
        '''searches for term and creates PRTEntry for all data in term'''
        opened = open(self.prt_file)

        for line in tqdm(opened, 'Searching PRT', total=self.f_len):
            if line.strip().startswith(terms):
                term = self._det_term(line, terms)
                temp = PRTEntry(self.x, self.y, self.z)
                temp.read_type_info(line)

                self._skip_lines(opened, term)
                temp.read_cell_info(opened)

                self.runs[term] += [temp]
        opened.close()

    def _skip_lines(self, f, term):
        for line in f:
            if line.strip().startswith(term):
                return

    def _det_term(self, line, terms):
        for each in terms:
            if line.strip().startswith(each):
                return each

if __name__ == '__main__':
    from sys import argv

    test = PRTController(argv[1])
    test.add_runs()
    print(str(test.runs))
