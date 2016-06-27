from ModelMaker import ModelMaker
from collections import defaultdict
from os import walk, path


class Interface(object):

    def __init__(self):
        self.files = defaultdict(list)
        self.direct = ''

    def start(self):
        print("Welcome to Petrel/Eclipse visual modeler.")
        self.body()

    def search(self):
        terms = raw_input("What terms are you modeling today? Please " +
                          "enter terms seperated by a space.\n")
        return terms.strip().split()

    def file_finder(self):
        while True:
            direct = raw_input("What is the directory containing your " +
                               "project?\n")

            for root, dirs, files in walk(direct):
                for f in files:
                    case_switched = f.lower()

                    if case_switched.endswith(".PRT"):
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
        if len(self.files["DATA"]) > 1:
            print("There are more than one file with the *.data extension " +
                  "listed here:")
            for each in self.files["DATA"]:
                print(each)
            print('')
            self.files["DATA"] = raw_input("Please enter the file you want\n")
        else:
            self.files["DATA"] = self.files["DATA"][0]

        if len(self.files["PRT"]) > 1:
            print("There are more than one file with the *.PRT extension " +
                  "listed here:")
            for each in self.files["PRT"]:
                print(each)
            print('')
            self.files["PRT"] = raw_input("Please enter the file you want\n")
        else:
            self.files["PRT"] = self.files["PRT"][0]
        
    def body(self):
        self.file_finder()
        model = ModelMaker(self.files["DATA"], self.files["PRT"], self.direct)

        terms = tuple(self.search())
        model.run(terms)
        print("Visual modeling files created")

if __name__ == '__main__':
    test = Interface()
    test.file_finder()
    print(test.files["DATA"])
    print(test.files["PRT"])
