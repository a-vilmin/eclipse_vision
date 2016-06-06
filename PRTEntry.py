class PRTEntry():

    # nested class to store cell data
    class Cell():
        def __init__(self):
            self.y = 0
            self.x = 0
            self.z = 0
            self.n = 0.0

    # class methods
    def __init__(self):
        self.cells = []
        self.time = 0.0
        self.name = ''

    def read_type_info(self, line):

        break_up = line.strip().split()
        try:
            for each in break_up[1:]:
                try:
                    t = float(each)
                    self.time = t
                    break
                except ValueError:
                    self.name += each
        except:
            print("Incorrect format passed to PRTEntry object. Grid data" +
                  "format not recognized!")

    def read_cell_info(self, f):

        for line in f:
            
