from VTKWriter import VTKWriter
from EclipseReader import EclipseReader


class ModelMaker():
    def __init__(self, data_file, prt_file):

        self.vtk_write = VTKWriter(prt_file)
        self.eclipse_read = EclipseReader(data_file)

    def run(self):
        self.eclipse_read.file_read()

        # self.vtk_write.add_perms(self.eclipse_read)
        self.vtk_write.add_run(self.eclipse_read)
        self.vtk_write.write_file("pressure")

if __name__ == '__main__':
    from sys import argv

    model = ModelMaker(argv[1], argv[2])
    model.run()
