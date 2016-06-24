from VTKWriter import VTKWriter
from EclipseReader import EclipseReader


class ModelMaker():
    def __init__(self, data_file, prt_file, wk_dir):

        self.vtk_write = VTKWriter(prt_file, wk_dir)
        self.eclipse_read = EclipseReader(data_file, wk_dir)

    def run(self, terms):
        self.eclipse_read.file_read()
        self.vtk_write.add_perms(self.eclipse_read)
        self.vtk_write.add_run(self.eclipse_read, terms)
        self.vtk_write.write_file()

if __name__ == '__main__':
    from sys import argv

    model = ModelMaker(argv[1], argv[2])
    model.run()
