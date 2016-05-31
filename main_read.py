# Adam Vilmin 
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from collections import OrderedDict
import sys
from vtk import *

class MainReader():

    def __init__(self, f):

        self.run_spec = RunSpec()
        self.grid = EclipseGrid()
        self.regions = Region()
        self.read_f = f
        
    def file_read(self):
        for line in self.read_f:
            if line.startswith('RUNSPEC'):
                self.run_spec.handle(self.read_f)
