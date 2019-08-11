import pandas as pd


class Cleaner:
    def __init__(self, classifier):
        self.classifier = classifier
        self.clean(classifier.df)

    def clean(self, df):
        for attribute in self.classifier.structure:
            if self.classifier.structure[attribute][0]=="NUMERIC":
                df[attribute].fillna(df[attribute].mean(), inplace=True)
                df[attribute]= pd.cut(df[attribute], self.classifier.binsNum, range(1,self.classifier.binsNum))
            else:
                df[attribute].fillna(df[attribute].mode()[0], inplace=True)
        return df