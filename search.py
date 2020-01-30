import math as mth

import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

ps = PorterStemmer()


def opendoc(doc):
    """
    Opens the provided `doc` as a csv readable file with pandas. All data is automatically an integer and can be made a float later.
    The data is returned in a tuple containing the dataframe and the amount of documents. Other functions require the dataframe produced by this function.
    """
    csv = pd.read_csv(doc, delimiter=";")
    # the amount of documents in the dataframe is returned. One is subtracted since the first cell is empty
    docamount = csv.shape[1] - 1
    return (csv, docamount)


def generatesqrmatrix(dataframe):
    """Generates a squared weighted term matrix from a `dataframe`. Returns the updated weighted term matrix."""
    dataframe = dataframe[0]  # get the first entry from the tuple
    dataframesqr = dataframe.copy()
    for (tuple) in dataframesqr.itertuples(
    ):  # create a tuple from every line in the dataframe
        tuplen = len(tuple)  # get the length of the tuple
        for i in range(
                2, tuplen
        ):  # for every digit in the tuple (starting from 2), do the loop
            tupvalue = tuple[i]
            if type(tupvalue) is not str:  # check if it is a float or integer
                # get the current row which is the first item in the tuple
                current_row = tuple[0]
                # the name of the field is the label of the namedtuple
                header = tuple._fields[i]
                tupvalue = tupvalue * tupvalue  # square the tupvalue
                dataframesqr.at[(current_row), header] = tupvalue
    return dataframesqr


def generatedveclen(twmatrix):
    """
    Generates the document vector length for every document when given the term-weight matrix as `twmatrix`. Supplies a list.
    """
    header = list(twmatrix)  # get the header of the matrix
    headerlen = len(header)
    totals = list()
    # for every entry in the list, starting from the first until the last digit, do the loop
    for i in range(1, headerlen):
        # get the sum of the complete column with the header corresponding to the current loop-ID
        total = twmatrix[header[i]].sum()
        total_sqrt = mth.sqrt(total)  # get the square root of the total
        totals.append(total_sqrt)  # add the total to the list
    return totals


def getdotprod(query, dataframe):
    """
    Calculates the dot product for the `document` provided. The `query` is provided as a list and uses the dataframe to calculate the dot product for this document.
    """
    df = dataframe[0]  # get the first entry from the tuple and name it df
    # get the amount of documents and add one so the for loop works
    length = dataframe[1] + 1
    headers = list(dataframe[0])
    dotproducts = dict()
    for i in range(1, length):
        # copy the existing dataframe to a new dataframe called currentframe
        currentframe = df[["Unnamed: 0", headers[i]]].copy()
        totalscore = 0
        for (tuple) in (currentframe.itertuples()
                        ):  # create a tuple from every line in the dataframe
            if (
                    tuple[1] in query
            ):  # if the term is in the query, add the frequency to the totalscore
                totalscore += tuple[2]
        # add the totalscore to a dictionary
        dotproducts[headers[i]] = totalscore
        del currentframe  # delete the copied dataframe to save on memory
    return dotproducts


def sim(dotproducts, query, veclen):
    """Calculate the cosine similarity for the `dotproducts` and `query` provided with the previously calculated `veclen` as vector length."""
    counter = -1  # create a counter which will be zero on the first iteration
    similarities = dict()  # create a dictionary for the results per word
    for item in dotproducts:  # go through every document
        counter += 1  # increase the counter
        # get the vectorlength for the current word
        vectorlength = veclen[counter]
        # get the result of the dot product function for the current word
        dotproduct = dotproducts[item]
        querylength = len(query)
        # get the square root of the query length
        sqrtquerylength = mth.sqrt(querylength)
        # calculate the cosine similarity
        calculation = dotproduct / (vectorlength * sqrtquerylength)
        # add the result to the dictionary for the current word
        similarities[item] = calculation
    return similarities


def rank(similarities):
    """Rank the supplied similarities and convert it to a listed list."""
    dfSimi = pd.DataFrame(list(
        similarities.items()))  # get the dictionary into a dataframe
    # sort the matrix in descending order in the first column
    dfSimi.sort_values(by=[1], inplace=True, ascending=False)
    ranks = dfSimi.values.tolist()
    return ranks


def reformquery(query):
    """Remove the stopwords and apply stemming"""
    reformedquery = ps.stem(query)  # apply stemming to the reformedquery
    stop = set(stopwords.words("english"))
    words = reformedquery.split()
    cleanedquery = list()
    for word in words:
        if word not in stop:
            cleanedquery.append(word)
    return cleanedquery


def getsniplocation(query, results, path):
    """
    Returns the snippet location for all documents, based on the query and
    the ranked results. The path to the documents also needs to be provided in
    the format `data/`. The location `0, 0` is returned when the document
    does not contain the query term.
    """
    # We only look for the first word in the query
    query = query.split()
    firstword = query[0]
    firstword = firstword.lower()
    firstword = ps.stem(firstword)
    sniplocation = dict()
    # The following part loops through all documents and
    # captures the position of the first occurance.
    for document in results:
        docname = document[0]
        filename = path + docname
        file = open(filename)
        words = file.read()
        words = words.lower()
        splitwords = words.split()
        stemmedwords = list()
        for word in splitwords:
            # Applying stemming to every word in the document
            stem = ps.stem(word)
            stemmedwords.append(stem)
        # An except is used in case the document does not contain the word
        try:
            # find the place of the query
            index = stemmedwords.index(firstword)
            if index > 20:
                indexstart = index - 20
                indexend = index + 20
                # It is often easier to get some context from the snippet
                # this is only possible if the first occurance is not at the
                # start of the document.
            else:
                indexstart = index
                indexend = index + 25
            sniplocation[docname] = [indexstart, indexend]
        except:
            sniplocation[docname] = [0, 0]
        file.close()
    return sniplocation


def getsnippet(sniplocation, path):
    """
    Returns a snippet for all documents in dict-form, based on the
    snippets location provided with the getsniplocation() function.
    """
    snippets = dict()
    unaval = "There was no exact match with your query in this document, however it may contain similair words"
    for document in sniplocation:
        snippettext = ""  # reset variable
        positions = sniplocation[document]
        filename = path + document
        file = open(filename)
        words = file.read()
        splitwords = words.split()
        indexstart = positions[0]
        indexend = positions[1]
        if indexend > 0:
            # If the doc did not contain the query, the indexend variable
            # is zero.
            for i in range(indexstart, indexend):
                # Attach the snippet word to the previous snippet words
                snippettext = snippettext + " " + splitwords[i]
        elif indexend == 0:
            # Add a placeholder text to the doc without the query.
            snippettext = unaval
        # Add the snippets to the dictionary under the correct file name
        snippets[document] = snippettext
    file.close()
    return snippets
