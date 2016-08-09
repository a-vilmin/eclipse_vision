# Adam Vilmin
# Illinois State Geological Survey, University of Illinois
# 2015-05-31

from ModelMaker import ModelMaker
from collections import defaultdict
from os import walk, path


class Interface(object):
    """Interface for parsing Eclipse/Petrel output directories for search and
    visual model creation. Includes most of the error checking for each smaller
    data object.
    :self.files: dictionary of PRT and DATA file names
    :self.direct: name of Eclipse project directory"""

    def __init__(self):
        """creates self.files as defaultdict and self.direct as empty string. No
        arguments"""

        self.files = defaultdict(list)
        self.direct = ''

    def body(self):
        """main function for running interface. runs directory trace, retrieves
        search terms, and handling for ModelMaker object"""

        print("Welcome to Petrel/Eclipse visual modeler.")

        self.file_finder()
        model = ModelMaker(self.files["DATA"], self.files["PRT"], self.direct)

        terms = tuple(self.search())
        model.run(terms)
        print("Visual modeling files created")

    def search(self):
        """Returns a list of search strings that are all caps"""

        terms = raw_input("What terms are you modeling today? Please " +
                          "enter terms seperated by a space.\n")
        return [x.upper() for x in terms.strip().split()]

    def file_finder(self):
        """method to walk self.direct and locate the files for parsing (PRT and DATA)
        if either files are not located, will prompt for new directory name.
        Checksfor duplicate file extensions and handles this"""

        while True:
            direct = raw_input("What is the directory containing your " +
                               "project?\n")

            for root, dirs, files in walk(direct):
                for f in files:
                    case_switched = f.lower()

                    if case_switched.endswith(".prt"):
                        self.files["PRT"] += [path.join(root, f)]
                    elif case_switched.endswith(".data"):
                        self.files["DATA"] += [path.join(root, f)]

            if not self.files["PRT"]:
                print("Directory doesn't contain a *.PRT file. Please try " +
                      "again.\n")
                continue
            elif not self.files["DATA"]:
                print("Directory doesn't contain a *.data file. Please try " +
                      "again.\n")
            else:
                self.direct = direct
                break
        self.file_check()

    def file_check(self):
        """handles duplicate file extensions"""
        if len(self.files["DATA"]) > 1:

            print("There are more than one file with the *.data extension " +
                  "listed here:")
            for each in self.files["DATA"]:
                print(each)
            print('')

            while True:
                choice = raw_input("Please enter the file you want to use\n")

                if path.isfile(choice):
                    self.files["DATA"] = choice
                    break
                else:
                    print("You must have typed that in wrong. Try again.")
        else:
            self.files["DATA"] = self.files["DATA"][0]

        if len(self.files["PRT"]) > 1:
            print("There are more than one file with the *.PRT extension " +
                  "listed here:")
            for each in self.files["PRT"]:
                print(each)
            print('')

            while True:
                choice = raw_input("Please enter the file you want to use\n")

                if path.isfile(choice):
                    self.files["PRT"] = choice
                    break
                else:
                    print("You must have typed that in wrong. Try again.")
        else:
            self.files["PRT"] = self.files["PRT"][0]

if __name__ == '__main__':
    test = Interface()
    test.file_finder()
    print(test.files["DATA"])
    print(test.files["PRT"])
