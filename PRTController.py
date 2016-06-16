from PRTEntry import PRTEntry
from collections import defaultdict
from tqdm import *


class PRTController(object):

    def __init__(self, prt):
        self.prt_file = prt
        self.runs = defaultdict(list)
        self.f_len = self._get_len(prt)

    def _get_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def set_dims(self, dim_tup):
        self.x, self.y, self.z = dim_tup

    def add_runs(self, term):
        '''searches for term and creates PRTEntry for all data in term'''
        opened = open(self.prt_file)

        for line in tqdm(opened, 'Searching PRT', total=self.f_len):
            if line.strip().startswith(term):
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

if __name__ == '__main__':
    from sys import argv

    test = PRTController(argv[1])
    test.add_runs()
    print(str(test.runs))
