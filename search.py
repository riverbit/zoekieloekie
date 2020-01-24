import pandas as pd
import math as mth
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
ps = PorterStemmer()

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
    dataframesqr = dataframe.copy()
    for tuple in dataframesqr.itertuples(): # create a tuple from every line in the dataframe
        tuplen = len(tuple) # get the length of the tuple
        for i in range(2, tuplen): # for every digit in the tuple (starting from 2), do the loop
            tupvalue = tuple[i]
            if type(tupvalue) is not str: # check if it is a float or integer
                current_row = tuple[0] # get the current row which is the first item in the tuple
                header = tuple._fields[i] # the name of the field is the label of the namedtuple
                tupvalue = tupvalue * tupvalue # square the tupvalue
                dataframesqr.at[(current_row), header] = tupvalue
    return dataframesqr

def generatedveclen(twmatrix):
    """
    Generates the document vector length for every document when given the term-weight matrix as `twmatrix`. Supplies a list.
    """
    header = list(twmatrix) # get the header of the matrix
    headerlen = len(header)
    totals = list()
    for i in range(1, headerlen): # for every entry in the list, starting from the first until the last digit, do the loop
        total = twmatrix[header[i]].sum() # get the sum of the complete column with the header corresponding to the current loop-ID
        total_sqrt = mth.sqrt(total) # get the square root of the total
        totals.append(total_sqrt) # add the total to the list
    return totals

def getdotprod(query, dataframe):
    """
    Calculates the dot product for the `document` provided. The `query` is provided as a list and uses the dataframe to calculate the dot product for this document.
    """
    df = dataframe[0] # get the first entry from the tuple and name it df
    length = dataframe[1] + 1 # get the amount of documents and add one so the for loop works
    headers = list(dataframe[0])
    dotproducts = dict()
    for i in range(1, length):
        currentframe = df[['Unnamed: 0', headers[i]]].copy() # copy the existing dataframe to a new dataframe called currentframe
        totalscore = 0
        for tuple in currentframe.itertuples(): # create a tuple from every line in the dataframe
            if tuple[1] in query: # if the term is in the query, add the frequency to the totalscore
                totalscore += tuple[2]
        dotproducts[headers[i]] = totalscore # add the totalscore to a dictionary
        del currentframe # delete the copied dataframe to save on memory
    return dotproducts

def sim(dotproducts, query, veclen):
    """Calculate the cosine similarity for the `dotproducts` and `query` provided with the previously calculated `veclen` as vector length."""
    counter = -1 # create a counter which will be zero on the first iteration
    similarities = dict() # create a dictionary for the results per word
    for item in dotproducts: # go through every document
        counter += 1 # increase the counter
        vectorlength = veclen[counter] # get the vectorlength for the current word
        dotproduct = dotproducts[item] # get the result of the dot product function for the current word
        querylength = len(query)
        sqrtquerylength = mth.sqrt(querylength) # get the square root of the query length
        calculation = (dotproduct / (vectorlength * sqrtquerylength)) # calculate the cosine similarity
        similarities[item] = calculation # add the result to the dictionary for the current word
    return similarities

def rank(similarities):
    """Rank the supplied similarities and convert it to a listed list."""
    dfSimi = pd.DataFrame(list(similarities.items())) # get the dictionary into a dataframe
    dfSimi.sort_values(by=[1], inplace=True, ascending=False) # sort the matrix in descending order in the first column
    ranks = dfSimi.values.tolist()
    return ranks

def reformquery(query):
    """Remove the stopwords and apply stemming"""
    reformedquery = ps.stem(query) # apply stemming to the reformedquery
    stop = set(stopwords.words('english'))
    words = reformedquery.split()
    cleanedquery = list()
    for word in words:
        if word not in stop:
            cleanedquery.append(word)
    return cleanedquery