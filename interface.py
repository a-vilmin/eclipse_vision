from ModelMaker import ModelMaker
from collections import defaultdict
from os import walk


class Interface(object):

    def __init__(self):
        self.files = defaultdict(str)
        self.directory = ''

    def start(self):
        print("Welcome to Petrel/Eclipse visual modeler.")
        self.body()

    def search(self):
        terms = raw_input("What terms are you modeling today? Please " +
                          "enter terms seperated by a space.\n")
        return terms.strip().split()

    def file_finder(self):
        while True:
            path = raw_input("What is the directory containing your " +
                             "project?\n")

            for root, dirs, files in walk(path):
                for f in files:
                    if f.endswith(".PRT"):
                        self.files["PRT"] = root + f
                    elif f.endswith(".data"):
                        self.files["DATA"] = root + f

            if not self.files["PRT"]:
                print("Directory doesn't contain a *.PRT file. Please try " +
                      "again.\n")
                continue
            elif not self.files["DATA"]:
                print("Directory doesn't contain a *.data file. Please try " +
                      "again.\n")
            else:
                break

    def body(self):
        self.file_finder()
        modeler = ModelMaker(self.files["DATA"], self.files["PRT"])

        terms = tuple(self.search())
        modeler.run(terms)
        print("Visual modeling files created")
