from PRTController import PRTController
from vtk import vtkImageData


class VTKWriter(PRTController):

    def __init__(self, prt):
        super(VTKWriter, self).__init__(prt)
        self.grid = vtkImageData()

    def set_grid_spec(self, eclipse):
        """expect eclipse file reader object. refer to readme for specs"""
        dx, dy, dz = eclipse.spacing()
        self.grid.SetOrigin(0, 0, 0)
        self.grid.SetSpacing(dx, dy, dz)

        x_dim, y_dim, z_dim = eclipse.dims()
        self.grid.SetDimensions(int(x_dim)+1, int(y_dim)+1, int(z_dim)+1)

if __name__ == '__main__':
    from EclipseReader import EclipseReader
    from sys import argv

    f = open(argv[1])
    test_ER = EclipseReader(f)
    test_VTK = VTKWriter(argv[2])

    test_ER.file_read()
    test_VTK.set_grid_spec(test_ER)

    print(str(test_VTK.grid.GetNumberOfPoints()))
    print(str(test_VTK.grid.GetNumberOfCells()))
