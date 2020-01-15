import csv
import pandas as pd
import math as mth
def opendoc(doc): 
    """
    Opens the provided `doc` as a csv readable file with pandas. All data is automatically an integer and can be made a float later.
    The data is returned in a tuple containing the dataframe and the amount of documents.
    """
    csv = pd.read_csv(doc, delimiter=";") 
    docamount = csv.shape[1] - 1 # the amount of documents in the dataframe is returned. One is subtracted since the first cell is empty
    return(csv, docamount)

def calcdf(doc): 
    """Calculate document frequency for the csv-file `doc` and return this document frequency in a list sorted by document ID."""
    csv = opendoc(doc)
    newcsv = csv[0].astype(bool).sum(axis=1, numeric_only=True) # generate a dataframe with all the occurences of the word, PLUS ONE
    df = newcsv.apply(lambda x: x - 1) # return the value of newcsv (dataframe with doc occurences) minus one for every row
    return df.tolist() # document frequency is returned as a regular list

def calcidf(df, docamount):
    """Calculate the inversed document frequency for the `df` dataframe provided. The function returns an inverted document frequency per word in a list."""
    idf = list()
    for term in df:
        multiplication = docamount * term
        term = mth.log2(multiplication)
        idf.append(term)
    return idf


test = opendoc("test_data/recepten.csv")
df = calcdf("test_data/recepten.csv")
print(calcidf(df, test[1]))