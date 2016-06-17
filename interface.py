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
        terms = input("What terms are you modeling today? Please " +
                      "enter terms seperated by a space")
        return terms.strip().split()

    def file_finder(self):
        while True:
            prt = input("What is your *.PRT file? Please " +
                        "include full file path.").strip()

            if path.isfile(prt) and prt.endswith(".PRT"):
                self.files["PRT"] = prt
                break
            else:
                print(prt+" is not a valid file.")

        while True:
            data = input("What is your *.data file? Please " +
                         "include full file path.").strip()

            if path.isfile(data) and prt.endswith(".data"):
                self.files["DATA"] = data
                break
            else:
                print(data+" is not a valid file.")

    def body(self):
        self.file_finder()
        modeler = ModelMaker(self.files["DATA"], self.files["PRT"])

        while True:
            terms = tuple(self.search())
            modeler.run(terms)

