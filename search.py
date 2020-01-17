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

def generatesqrmatrix(dataframe):
    """Generates a squared weighted term matrix from a `dataframe`. Returns the updated weighted term matrix."""
    dataframe = dataframe[0] # get the first entry from the tuple
    for tuple in dataframe.itertuples(): # create a tuple from every line in the dataframe
        tuplen = len(tuple) # get the length of the tuple
        for i in range(2, tuplen): # for every digit in the tuple (starting from 2), do the loop
            tupvalue = tuple[i]
            if type(tupvalue) is not str: # check if it is a float or integer
                current_row = tuple[0] # get the current row which is the first item in the tuple
                header = tuple._fields[i] # the name of the field is the label of the namedtuple
                tupvalue = tupvalue * tupvalue # square the tupvalue
                dataframe.at[(current_row), header] = tupvalue
    return dataframe

def generatedveclen(twmatrix):
    """
    Generates the document vector length for every document when given the term-weight matrix as `twmatrix`. Supplies a list.
    """
    header = list(twmatrix)
    headerlen = len(header)
    totals = list()
    for i in range(1, headerlen):
        total = twmatrix[header[i]].sum()
        total_sqrt = mth.sqrt(total)
        totals.append(total_sqrt)
    return totals

dataframe = opendoc("test_data/recepten.csv")
print(dataframe[1])
twmatrix = generatesqrmatrix(dataframe)
print(twmatrix)
print(generatedveclen(twmatrix))