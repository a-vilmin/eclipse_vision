# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31


class SectionReader(object):
    """Abstract class to impliment the section done method in all Eclipse
    parsing objects. Contains abstract method handle that must be added in
    child class"""

    def __init__(self):
        raise TypeError("Cannot make object SectionReader")

    def _section_done(self, line):
        if len(line.split()) > 1:
                if line.split()[1].count('-') > 2:
                    return True
        return False

    def handle(self, f):
        raise TypeError("Must define function")
