from PRTController import PRTController
from vtk import vtkImageData, vtkFloatArray, vtkXMLImageDataWriter
from tqdm import *


class VTKWriter():

    def __init__(self, prt):
        self.prt = PRTController(prt)
        self.grid = []

    def set_grid_spec(self, vtk, eclipse):
        """expect eclipse file reader object. refer to readme for specs"""
        vtk.SetOrigin(0, 0, 0)
        dx, dy, dz = eclipse.spacing()
        vtk.SetSpacing(dx, dy, dz)

        x_dim, y_dim, z_dim = eclipse.dims()
        vtk.SetDimensions(int(x_dim)+1, int(y_dim)+1, int(z_dim)+1)

    def add_run(self, eclipse, term="PRESSURE"):
        self.prt.set_dims(eclipse.dims())
        self.prt.add_runs(term)
        runs = self.prt.runs[term]

        x_dim, y_dim, z_dim = eclipse.dims()
        # run is PRTEntry object
        for run in tqdm(runs, "creating "+term+" vtk arrays"):

            tmp = vtkImageData()
            self.set_grid_spec(tmp, eclipse)

            array = vtkFloatArray()
            array.SetName(run.name+" at "+str(run.time)+" days.")
            array.SetNumberOfComponents(1)

            # starts at bottom and moves down x rows, building up
            for z in range(z_dim - 1, -1, -1):
                for y in range(0, y_dim):
                    for x in range(0, x_dim):
                        scalar = run.cells[z][y][x]
                        array.InsertNextTuple1(scalar)
            tmp.GetCellData().AddArray(array)
            self.grid += [tmp]

    def add_perms(self, eclipse):
        tmp = vtkImageData()
        array = vtkFloatArray()

        array.SetName("PERM Values")
        array.SetNumberOfComponents(1)

        x_dim, y_dim, z_dim = eclipse.dims()

        for z in range(z_dim - 1, -1, -1):
            for y in range(0, y_dim):
                for x in range(0, x_dim):
                    scalar = eclipse.grid.perms[z][y][x]
                    array.InsertNextTuple1(scalar)
        tmp.GetCellData().AddArray(array)
        self.grid += [tmp]

    def write_file(self, term):
        i = 1
        for each in tqdm(self.grid, "Writing VTK Files"):
            legacy = vtkXMLImageDataWriter()
            legacy.SetFileName(term+"_"+str(i)+'.vti')
            legacy.SetInput(each)
            legacy.Write()
            i += 1
if __name__ == '__main__':
    from EclipseReader import EclipseReader
    from sys import argv

    test_ER = EclipseReader(argv[1])
    test_VTK = VTKWriter(argv[2])

    test_ER.file_read()
    test_VTK.set_grid_spec(test_ER)
    test_VTK.add_run(test_ER)

    test_VTK.write_file("test")
