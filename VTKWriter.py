from PRTController import PRTController
from vtk import vtkImageData


class VTKWriter(PRTController):

    def __init__(self, prt):
        super().__init__(prt)
        self.grid = vtkImageData()

    def set_grid_spec(self, eclipse):
        """expect eclipse.data file reader object. refer to readme for specs"""
