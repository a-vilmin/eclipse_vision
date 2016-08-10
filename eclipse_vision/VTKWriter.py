# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from PRTController import PRTController
from vtk import vtkImageData, vtkFloatArray, vtkXMLImageDataWriter
from collections import defaultdict
from tqdm import tqdm
from os import makedirs, path
import time


class VTKWriter():
    """class for writing vtk files based on Eclipse outputs parsed from
    EclipseReader and PRTController objects
    :self.prt: PRTController object
    :self.grid: defaultdict of lists referenced by VTKArray name
    :self.dir: project directory string"""

    def __init__(self, prt, direct):
        """initializes self variables and requires PRT name string
        and directory string"""

        self.prt = PRTController(prt)
        self.grid = defaultdict(list)
        self.dir = direct

    def _set_grid_spec(self, vtk, eclipse):
        """Uses EclipseReader object to set params for the VTK file. Takes
        vtkImageData object and EclipseReader as args"""

        vtk.SetOrigin(0, 0, 0)

        dx, dy, dz = eclipse.spacing()
        vtk.SetSpacing(dx, dy, dz)

        x_dim, y_dim, z_dim = eclipse.dims()
        vtk.SetDimensions(int(x_dim)+1, int(y_dim)+1, int(z_dim)+1)

    def add_runs(self, eclipse, search_terms):
        """Uses self.prt to search PRT file using list of search terms then creates
        vtkFloatArrays for the scalar values"""

        self.prt.set_dims(eclipse.dims())

        # actual PRT file parsing
        self.prt.add_runs(search_terms)

        x_dim, y_dim, z_dim = eclipse.dims()

        # self.prt.runs is dictionary referencing lists of PRTEntry objects
        for term, runs in self.prt.runs.iteritems():
            # run is PRTEntry object
            for run in tqdm(runs, "creating "+term+"'s vtk arrays"):

                # writing individual time steps requires seperate VTK grids
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
        """creates porocity VTK file if Poro is flagged by EclipseReader"""

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
        """creates Permiability VTK file"""
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
        """Writes all VTK grids in self.grid to VTI files"""

        for key, value in self.grid.iteritems():
            # creates directory for each term in Eclipse project directory
            # root for all VTI files is dated by parser runtime date
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
                legacy.SetInputData(each)
                legacy.Write()
                i += 1

if __name__ == '__main__':
    from EclipseReader import EclipseReader
    from sys import argv

    test_ER = EclipseReader(argv[1])
    test_VTK = VTKWriter(argv[2])

    test_ER.file_read()
    test_VTK.set_grid_spec(test_ER)
    test_VTK.add_runs(test_ER)

    test_VTK.write_file("test")
