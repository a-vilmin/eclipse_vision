# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from VTKWriter import VTKWriter
from EclipseReader import EclipseReader


class ModelMaker():
    """class for merging data parsed from PRT file with the creation of vtk
    files.
    :self.vtk_write: VTKWriter object
    :self.eclipse_read: EclipseReader object"""

    def __init__(self, data_file, prt_file, wk_dir):
        """creates self variables and requires data file string, prt file string,
        and project directory string to initialize"""

        self.vtk_write = VTKWriter(prt_file, wk_dir)
        self.eclipse_read = EclipseReader(data_file, wk_dir)

    def run(self, terms):
        """reads Eclipse outputs and creates VTK files in project directory"""

        self.eclipse_read.file_read()
        self.vtk_write.add_perms(self.eclipse_read)
        self.vtk_write.add_poro(self.eclipse_read)
        self.vtk_write.add_runs(self.eclipse_read, terms)
        self.vtk_write.write_file()

if __name__ == '__main__':
    from sys import argv

    model = ModelMaker(argv[1], argv[2])
    model.run()
