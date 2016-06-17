from ModelMaker import ModelMaker
from collections import defaultdict
from os import path


class Interface(object):

    def __init__(self):
        self.files = defaultdict(str)

    def start(self):
        print("Welcome to Petrel/Eclipse visual modeler.")
        self.body()

    def search(self):
        terms = raw_input("What terms are you modeling today? Please " +
                          "enter terms seperated by a space.\n")
        return terms.strip().split()

    def file_finder(self):
        while True:
            prt = raw_input("What is your *.PRT file? Please " +
                            "include full file path.\n")

            if path.isfile(prt) and prt.endswith(".PRT"):
                self.files["PRT"] = prt
                break
            else:
                print(prt+" is not a valid file.")

        while True:
            data = raw_input("What is your *.data file? Please " +
                             "include full file path.\n").strip()

            if path.isfile(data) and data.endswith(".data"):
                self.files["DATA"] = data
                break
            else:
                if not path.isfile(data):
                    print(data+" does not exist!")
                elif not prt.endswith(".data"):
                    print(data+" is not correct file type")
                else:
                    print("Unknown error with "+data)

    def body(self):
        self.file_finder()
        modeler = ModelMaker(self.files["DATA"], self.files["PRT"])

        while True:
            terms = tuple(self.search())
            modeler.run(terms)
            print("Visual files created")
            return
