from PRTController import PRTController
from vtk import vtkImageData, vtkFloatArray, vtkXMLImageDataWriter
from collections import defaultdict
from tqdm import tqdm
from os import makedirs, path
import time


class VTKWriter():

    def __init__(self, prt, direct):
        self.prt = PRTController(prt)
        self.grid = defaultdict(list)
        self.dir = direct

    def _set_grid_spec(self, vtk, eclipse):
        """expect eclipse file reader object. refer to readme for specs"""
        vtk.SetOrigin(0, 0, 0)
        dx, dy, dz = eclipse.spacing()
        vtk.SetSpacing(dx, dy, dz)

        x_dim, y_dim, z_dim = eclipse.dims()
        vtk.SetDimensions(int(x_dim)+1, int(y_dim)+1, int(z_dim)+1)

    def add_run(self, eclipse, search_terms):
        self.prt.set_dims(eclipse.dims())
        self.prt.add_runs(search_terms)

        x_dim, y_dim, z_dim = eclipse.dims()
        # run is PRTEntry object
        for term, runs in self.prt.runs.iteritems():
            for run in tqdm(runs, "creating "+term+"'s vtk arrays"):
                tmp = vtkImageData()
                self._set_grid_spec(tmp, eclipse)

                array = vtkFloatArray()
                array.SetName(run.name)
                array.SetNumberOfComponents(1)

                # starts at bottom and moves down x rows, building up
                for z in range(z_dim - 1, -1, -1):
                    for y in range(0, y_dim):
                        for x in range(0, x_dim):
                            scalar = run.cells[z][y][x]
                            array.InsertNextTuple1(scalar)
                tmp.GetCellData().AddArray(array)
                self.grid[term] += [tmp]

    def add_poro(self, eclipse):

        if 'PORO' not in eclipse.grid.includes:
            return

        tmp = vtkImageData()
        self._set_grid_spec(tmp, eclipse)

        array = vtkFloatArray()
        array.SetName("PORO Values")
        array.SetNumberOfComponents(1)

        x_dim, y_dim, z_dim = eclipse.dims()

        for z in tqdm(range(z_dim - 1, -1, -1), "Writing Porosity Arrays"):
            for y in range(0, y_dim):
                for x in range(0, x_dim):
                    scalar = eclipse.grid.includes['PORO'][z][y][x]
                    array.InsertNextTuple1(scalar)
        tmp.GetCellData().AddArray(array)
        self.grid["PORO"] += [tmp]

    def add_perms(self, eclipse):
        tmp = vtkImageData()
        self._set_grid_spec(tmp, eclipse)

        array = vtkFloatArray()
        array.SetName("PERM Values")
        array.SetNumberOfComponents(1)

        x_dim, y_dim, z_dim = eclipse.dims()

        for z in tqdm(range(z_dim - 1, -1, -1), "Writing Perm Arrays"):
            for y in range(0, y_dim):
                for x in range(0, x_dim):
                    scalar = eclipse.grid.includes['PERMX'][z][y][x]
                    array.InsertNextTuple1(scalar)
        tmp.GetCellData().AddArray(array)
        self.grid["PERMS"] += [tmp]

    def write_file(self):
        for key, value in self.grid.iteritems():
            dir_name = path.join(self.dir, time.strftime("%d_%m_%Y"))
            dir_name = path.join(dir_name, key)

            try:
                makedirs(dir_name)
            except OSError:
                pass

            i = 1
            for each in tqdm(value, "Writing "+key+" vtk files"):
                legacy = vtkXMLImageDataWriter()
                legacy.SetFileName(path.join(dir_name, key + str(i) + '.vti'))
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
