from PRTController import PRTController
from vtk import vtkImageData, vtkFloatArray, vtkXMLImageDataWriter


class VTKWriter():

    def __init__(self, prt):
        self.prt = PRTController(prt)
        self.grid = vtkImageData()

    def set_grid_spec(self, eclipse):
        """expect eclipse file reader object. refer to readme for specs"""
        self.grid.SetOrigin(0, 0, 0)
        print('setting grid')
        dx, dy, dz = eclipse.spacing()
        self.grid.SetSpacing(dx, dy, dz)

        x_dim, y_dim, z_dim = eclipse.dims()
        self.grid.SetDimensions(int(x_dim)+1, int(y_dim)+1, int(z_dim)+1)

    def add_run(self, term="SGAS"):
        
        self.prt.add_runs(term)
        runs = self.prt.runs[term]
        print('setting vtk array')

        # run is PRTEntry object
        for run in runs:
            array = vtkFloatArray()
            array.SetName(run.name+" at "+str(run.time)+" days.")
            array.SetNumberOfComponents(1)

            while len(run.cells):
                scalar = run.cells.pop()
                array.InsertNextTuple1(scalar)
            self.grid.GetCellData().AddArray(array)

    def add_poro(self, eclipse):
        for direction, values in eclipse.grid.perms.iteritems():
            array = vtkFloatArray()
            array.SetName(direction)
            array.SetNumberOfComponents(1)

            while len(values):
                val = values.pop().val
                array.InsertNextTuple1(val)
            self.grid.GetCellData().AddArray(array)

    def write_file(self, name):
        print('writing vtk file')
        legacy = vtkXMLImageDataWriter()
        legacy.SetFileName(name+'.vti')
        legacy.SetInputData(self.grid)
        legacy.Write()

if __name__ == '__main__':
    from EclipseReader import EclipseReader
    from sys import argv

    f = open(argv[1])
    test_ER = EclipseReader(f)
    test_VTK = VTKWriter(argv[2])

    test_ER.file_read()
    test_VTK.set_grid_spec(test_ER)
    test_VTK.add_run()

    test_VTK.write_file("test")
