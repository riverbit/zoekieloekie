import csv
import pandas as pd
def opendoc(doc): ## open document as csv readable file with pandas. All data is automatically an integer and can be made a float later
    csv = pd.read_csv(doc, delimiter=";") 
    return csv

def calcdf(doc): # calculate document frequency
    csv = opendoc(doc)
    newcsv = csv.astype(bool).sum(axis=1, numeric_only=True) # generate a dataframe with all the occurences of the word, PLUS ONE
    return newcsv.apply(lambda x: x - 1) # return the value of newcsv minus one for every row

test = opendoc("test_data/recepten.csv")
print(test)
csv = calcdf("test_data/recepten.csv")
print(csv)