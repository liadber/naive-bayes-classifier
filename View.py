from Tkinter import Tk, Label, Button, Entry
import tkMessageBox
import tkFileDialog
import os
import sys

from Classifier import Classifier


class View:
    def __init__(self, master):
        self.master = master
        self.master.title("Naive Bayes Classifier")

        Label(master, text="").grid(row=0)
        self.dirPath = Label(master, text="Directory Path:").grid(row=1)
        self.dirTextBox = Entry(master, width=60)
        self.dirTextBox.grid(row=1, column=1)

        self.browseButton = Button(master, text="Browse", command=lambda: self.browse())
        self.browseButton.grid(row=1, column=3)

        self.discBins = Label(master, text="Discretization Bins:").grid(row=2)
        self.discBinsBox = Entry(master, width=60)
        self.discBinsBox.grid(row=2, column=1)

        self.buildButton = Button(master, width=30, text="Build", command=lambda: self.build())
        self.buildButton.grid(row=4, column=1)

        self.classifyButton = Button(master, width=30, text="Classify", command=lambda: self.classify())
        self.classifyButton.grid(row=5, column=1)

        root.mainloop()

    def browse(self):
        self.dirPath = tkFileDialog.askdirectory();
        if self.isRequestedFilesExist():
            self.dirTextBox.delete(0, len(self.dirTextBox.get()))
            self.dirTextBox.insert(0, self.dirPath)
        else:
            tkMessageBox.showerror("Naive Bayes Classifier - Error", "This path - doesn't contain the requested files.")

    def isRequestedFilesExist(self): #TODO
        expfiles = ["Structure.txt", "train.csv", "test.csv"]
        for path, subdirs, files in os.walk(self.dirPath):
            for name in files:
                if name.startswith("Structure.txt"):

                    expfiles.remove("Structure.txt")

                elif name.startswith("train.csv"):

                    expfiles.remove("train.csv")

                elif name.startswith("test.csv"):
                    expfiles.remove("test.csv")

        if len(expfiles)>0:
            self.buildButton.config(state='disabled')
            return False
        else:
            self.buildButton.config(state='normal')
            return True

    def isBinsNumberReal(self): #todo
        try:
            int (self.binsNum)
            return True
        except:
            return False

    def build(self): #TODO
        if self.dirTextBox.get() == None or self.dirTextBox.get() == "":
            tkMessageBox.showerror("Naive Bayes Classifier - Error", "There is no path.")
        else:
            self.dirPath = self.dirTextBox.get()
            self.binsNum= self.discBinsBox.get()
            if not self.isRequestedFilesExist():
                tkMessageBox.showerror("Naive Bayes Classifier - Error", "This path - doesn't contain the requested files.")
            elif not self.isBinsNumberReal():
                tkMessageBox.showerror("Naive Bayes Classifier - Error", "This bins number is illegal.")
            elif self.isDataEmpty():
                tkMessageBox.showerror("Naive Bayes Classifier - Error", "This is an Empty File of Train.")
            else:
                self.binsNum = int(self.discBinsBox.get())
                self.loadTrainSet()
                self.buildModel()

    def classify(self):
        if not self.isRequestedFilesExist():
            tkMessageBox.showerror("Naive Bayes Classifier - Error", "This path - doesn't contain the requested files.")
        else:
            self.classifier.classify()
            tkMessageBox.showinfo("Naive Bayes Classifier - Success", "Classified. Check out the output.txt")
            sys.exit()

    def loadTrainSet(self):
        self.classifier = Classifier(self.dirPath, self.binsNum)

    def buildModel(self): #todo
        pass

    def isDataEmpty(self):
        if (os.stat(self.dirPath+"/train.csv").st_size > 3):
            return False
        else:
            return True


root = Tk()
my_gui = View(root)
