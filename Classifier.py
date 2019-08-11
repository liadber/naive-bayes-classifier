import tkMessageBox

import os
import pandas as pd

from Cleaner import Cleaner


class Classifier:
    def __init__(self, dirPath, binsNum):
        self.binsNum=binsNum
        self.dirPath=dirPath
        self.m_estimate=2
        self.loadStructure()
        try:
            self.df = pd.read_csv(self.dirPath+"/train.csv")
        except IOError:
            tkMessageBox.showerror("Naive Bayes Classifier - Error", "There is a problem with open " + self.dirPath + "/train.csv")
        self.cleaner= Cleaner(self)
        self.naiveBases= {} #attributeValue and Classification to NaiveBase
        self.cProb={}
        for (i,record) in self.df.iterrows():
            recordDic= record.to_dict()
            for attribute in recordDic:
                value=recordDic[attribute]
                c=recordDic["class"]
                n_c = len(self.df.loc[((self.df[attribute] == value) & (self.df["class"] == c))].index)
                n = len(self.df.loc[(self.df["class"] == c)].index)
                m = self.m_estimate
                M = len(self.structure[attribute])
                p= float(1)/M
                naiveBase= float(n_c+m*p)/(n+m)
                self.naiveBases[attribute + str(value) + c] = naiveBase
        for c in self.structure["class"]:
            self.cProb[c]= float(len(self.df.loc[(self.df["class"] == c)].index))/len(self.df.index)
        tkMessageBox.showinfo("Naive Bayes Classifier - Success",
                               "Building classifier using train-set is done!")



    def loadStructure(self):
        try:
            structureFile = open(self.dirPath+"/Structure.txt", "r")
        except IOError:
            tkMessageBox.showerror("Naive Bayes Classifier - Error", "There is a problem with open " + self.dirPath + "/Structure.txt")
        with structureFile:
            self.structure ={} # Each attribute and his values;
            for attribute in structureFile:
                attributeParts = attribute.split()
                values= self.getValues(attributeParts)
                self.structure[attributeParts[1]]=values
            structureFile.close()

    def getValues(self, attributeParts):
        if attributeParts[2][0] != '{':
            return [attributeParts[2]]
        else:
            attributeParts=attributeParts[2][1:-1]
            values=attributeParts.split(",")
            return values

    def classify(self):
        if os.path.exists(self.dirPath+"/output.txt"):
            os.remove(self.dirPath+"/output.txt")
        output = open(self.dirPath+"/output.txt", "w+")
        self.test= self.cleaner.clean(pd.read_csv(self.dirPath+"/test.csv"))
        counter=0
        for (i,record) in self.test.iterrows():
            recordDic= record.to_dict()
            naiveBasesRecord = {}
            for c in self.structure["class"]:
                naiveBasesRecord[c]=self.cProb[c]
                for attribute in recordDic:
                    if not attribute == "class":
                        tmp = attribute + str(recordDic[attribute]) + c
                        tmpValue = self.naiveBases.get(tmp)
                        if not type(tmpValue)==float:
                            tmpValue=1
                        naiveBasesRecord[c]=naiveBasesRecord[c]*tmpValue
            cMax = self.getMaxClass(naiveBasesRecord)
            output.write(str(counter)+" "+str(cMax)+"\n")
            counter+=1
        output.close()



    def getMaxClass(self, naiveBasesRecord):
        first=True
        for c in naiveBasesRecord:
            if first:
                cMax=c
                first=False
            if naiveBasesRecord[c]==max(naiveBasesRecord[c],naiveBasesRecord[cMax]):
                cMax=c
        return cMax