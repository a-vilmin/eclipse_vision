from PRTController import PRTController
from vtk import vtkImageData


class VTKWriter(PRTController):

    def __init__(self, prt):
        super().__init__(prt)
        self.grid = vtkImageData()

    def set_grid_spec(self, eclipse):
        """expect eclipse file reader object. refer to readme for specs"""
        x_dim, y_dim, z_dim = eclipse.dims()
        self.grid.SetDimensions(x_dim, y_dim, z_dim)

        dx, dy, dz = eclipse.spacing()
        self.grid.SetSpacing(dx, dy, dz)
