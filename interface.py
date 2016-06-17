from ModelMaker import ModelMaker
from collections import defaultdict
from os import path


class Interface(object):

    def __init__(self):
        self.search_terms = []
        self.poro = False
        self.modeler = None
        self.files = defaultdict(str)

    def start(self):
        print("Welcome to Petrel/Eclipse visual modeler.")
        self.body()

    def search(self):
        terms = input("What terms are you modeling today? Please " +
                      "enter terms seperated by a space")
        self.search_terms = terms.strip().split()

    def file_finder(self):
        while True:
            prt = input("What is your *.PRT file? Please " +
                        "include full file path.").strip()
            
            if path.isfile(prt) and prt.endswith(".PRT"):
                self.files["PRT"] = prt
                break
            else:
                print(prt+" is not a valid file.")

    def body(self):
        self.file_finder()

        while True:
            self.search()
            
