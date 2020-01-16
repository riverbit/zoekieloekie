import pandas as pd
import math as mth
def opendoc(doc): 
    """
    Opens the provided `doc` as a csv readable file with pandas. All data is automatically an integer and can be made a float later.
    The data is returned in a tuple containing the dataframe and the amount of documents. Other functions require the dataframe produced by this function.
    """
    csv = pd.read_csv(doc, delimiter=";") 
    docamount = csv.shape[1] - 1 # the amount of documents in the dataframe is returned. One is subtracted since the first cell is empty
    return(csv, docamount)

def calcdf(dataframe): 
    """Calculates document frequency for the csv-file `doc` and returns this document frequency in a list sorted by document ID. Supply `dataframe`."""
    adj_dataframe = dataframe[0].astype(bool).sum(axis=1, numeric_only=True) # generate a dataframe with all the occurences of the word, PLUS ONE
    df = adj_dataframe.apply(lambda x: x - 1) # return the value of newcsv (dataframe with doc occurences) minus one for every row
    return df.tolist() # document frequency is returned as a regular list

def calcidf(df, dataframe):
    """
    Calculate the inversed document frequency for the `df` dataframe provided. The function returns an inverted document frequency per word in a list.
    Provide `df` as document frequency and `dataframe` the dataframe tuple containing the length as well, generated with the `opendoc` function.
    """
    idf = list()
    for term in df:
        multiplication = dataframe[1] * term
        term = mth.log2(multiplication)
        idf.append(term) # add the idf just created to a new list called idf, with a entry for every word
    return idf

def generatetwmatrix(dataframe, idf):
    """Generates a squared weighted term matrix from a `dataframe` and `idf`. Returns the updated weighted term matrix."""
    dataframe = dataframe[0] # get the first entry from the tuple
    for tuple in dataframe.itertuples(): # create a tuple from every line in the dataframe
        tuplen = len(tuple) # get the length of the tuple
        for i in range(2, tuplen): # for every digit in the tuple (starting from 2), do the loop
            tupvalue = tuple[i]
            if type(tupvalue) is not str: # check if it is a float or integer
                current_row = tuple[0] # get the current row which is the first item in the tuple
                header = tuple._fields[i] # the name of the field is the label of the namedtuple
                tupvalue = tupvalue * idf[current_row] # multiply the tupvalue with the inverted document frequency of the current row
                sq_tupvalue = tupvalue * tupvalue
                dataframe.at[(current_row), header] = sq_tupvalue
    return dataframe

dataframe = opendoc("test_data/recepten.csv")
df = calcdf(dataframe)
idf = calcidf(df, dataframe)
#print(dataframe[0])
#print(idf)
print(generatetwmatrix(dataframe, idf))

#for(label, series) in dataframe[0].iterrows():
    #print(label)
    #print(series)