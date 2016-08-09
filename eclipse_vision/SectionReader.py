class SectionReader(object):

    def __init__(self):
        raise TypeError("Cannot make object SectionReader")

    def _section_done(self, line):
        if len(line.split()) > 1:
                if line.split()[1].count('-') > 2:
                    return True
        return False
    
    def handle(self, f):
        raise TypeError("Must define function")
        
