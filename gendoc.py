import csv
import math as mth


def cleantext(text):
    """This function cleans the supplied text from illegal characters, such as interpunction,
    upper case letters and numbers. It also generates the document term frequencies."""
    # TO DO ADD STEMMING
    # Remove illegal characters from the text
    cleanedtext = ""
    illegal_chars = [",", ".", "'"]
    stopwords = ['ben', 'hebben', 'zal', 'geen', 'eens', 'men', 'je', 'niets', 'hoe', 'zou', 'iemand', 'zich', 'over', 'ook', 'heb', 'nu', 'werd', 'mijn', 'doen', 'hier', 'wezen', 'doch', 'kan', 'hij', 'deze', 'tot', 'toen', 'dus', 'er', 'bij', 'door', 'mij', 'op', 'moet', 'geweest', 'tegen', 'de', 'ze', 'dan', 'iets', 'ik', 'uw', 'der', 'had', 'nog', 'een', 'zo', 'dat', 'maar', 'die', 'om', 'of', 'van', 'naar', 'andere', 'hem', 'u', 'daar', 'kunnen',
                 'met', 'ge', 'zonder', 'dit', 'na', 'al', 'zelf', 'onder', 'altijd', 'omdat', 'in', 'ja', 'want', 'veel', 'ons', 'me', 'te', 'niet', 'hun', 'het', 'als', 'waren', 'kon', 'haar', 'reeds', 'is', 'was', 'wat', 'heeft', 'en', 'zijn', 'wil', 'uit', 'wordt', 'toch', 'aan', 'meer', 'alles', 'wie', 'zij', 'voor', 'worden']
    for i in text:
        i = i.lower()  # make text lower case
        # check if the variable is in the illegal chars list or a number
        if i not in illegal_chars and not i.isnumeric():
            cleanedtext += i
    words = cleanedtext.split()  # splits the cleaned text into words

    word_frequencies = dict()  # create a new empty dictionary
    for i in words:  # check for every word if it is in the dictionary
        if i in word_frequencies:  # if in dictionary, add 1 to the total
            word_frequencies[i] += 1
        else:
            if i not in stopwords:
                word_frequencies[i] = 1  # if not, add entry to dict
    return word_frequencies


def gentermfreq(doclist, folderpath):
    """
    Function generates a term frequency matrix for the documents provided in the list
    `doclist`. The `folderpath` to the folder containing the documents needs to be provided.
    """
    wordcounts = dict()
    for document in doclist:
        path = folderpath + "/" + document
        file = open(path)
        txt = file.read()
        cleanedtxt = cleantext(txt)  # returns the document term frequency
        wordcounts[document] = cleanedtxt
    return wordcounts


def generatematrix(wordcounts):
    """Generate a term frequency matrix from the `wordcount` dictionary provided."""
    wordlist = list()  # generate several lists to be filled later
    header = list()
    matrix = list()
    for document in wordcounts:
        # for every txt file, add the file name to a list called headers
        header.append(document)
        # create a unique list containing all terms once
        for term in wordcounts[document]:
            if term not in wordlist:
                wordlist.append(term)
    matrix.append(header)  # add the generated header to the matrix
    for (word) in (
            wordlist
    ):  # for every unique word, check the frequency of the word in every doc
        row = list()  # reset the list called row
        row.append(word)  # put the unique word in front of the row
        for document in header:  # for every document check if it contains the term
            if word in wordcounts[document]:
                # get the frequency from the key from the assoc. dictionary
                frequency = wordcounts[document].get(word)
                row.append(frequency)
            else:
                # insert 0 for the current document if it does not contain the word
                row.append(0)
        matrix.append(row)
    header.insert(0, "")
    return matrix


def calcdf(matrix):
    """
    Calculates the document frequency for every term in the matrix supplied. Returns
    a tuple containing a dictionary with the terms and `df` value, as well as the amount of documents.
    """
    docamount = len(matrix[0])  # get the amount of documents
    df = dict()  # create a new dictionary
    for line in range(1, docamount):  # get every line from the matrix
        current_line = matrix[line]  # get the current line from the matrix
        term = current_line[0]
        worddf = 0
        for word in range(1, docamount):
            current_word = current_line[word]
            if (
                    current_word > 0
            ):  # if the value of the term is above zero, add this for the df
                worddf += 1
        df[term] = worddf  # save the df for the current term in a dictionary
    return df, docamount


def calcidf(df):
    """
    Generates the inverted document frequency for the document frequency supplied.
    Returns a dictionary containing all terms and idf value.
    """
    docamount = df[1] - 1  # subtract
    docfreq = df[0]
    idf = dict()  # create a new dictionary
    for term in docfreq:  # for every entry in the df, calculate the idf
        frequency = docfreq.get(term)
        multiplication = docamount / frequency
        answer = mth.log2(multiplication)
        idf[term] = answer  # save the idf in the dictionary for the current term
    return idf


def generatetfmatrix(matrix, idf):
    """
    Generate a new term weight matrix when supplied with the current `matrix` and
    the weighing factors `idf`. Returns a new matrix using lists.
    """
    docamount = len(matrix[0])  # get the amount of documents
    updatedmatrix = list()  # create a new empty matrix
    updatedmatrix.append(matrix[0])  # set the header in the new matrix
    for i in range(
            1, docamount
    ):  # do the loop for all documents, excluding the term itself
        newrow = list()  # create a new row for the matrix
        currentrow = matrix[i]  # get the current row from the old matrix
        # from this current row, get the current word
        currentword = currentrow[0]
        # from the idf dictionary, get the value corresp. with the current term
        wordweight = idf.get(currentword)
        newrow.append(currentword)  # add the current term to the new row
        for y in range(1, docamount):
            # get the current value of the term we are calculating
            currentvalue = currentrow[y]
            # calculate the new value with the weighing applied
            updatedvalue = currentvalue * wordweight
            newrow.append(updatedvalue)  # save this new value in the new row
        # append the filled row to the updated matrix
        updatedmatrix.append(newrow)
    return updatedmatrix


def saveastxt(document, name="data/database.csv"):
    """
    Saves the supplied variable as csv txt file called `database.csv` by default in the folder data.
    The file name can be changed. The file path needs to be supplied in the `name` variable.
    """
    with open(name, "w", newline="") as output:
        writer = csv.writer(output, delimiter=";")
        writer.writerows(document)


# EXAMPLE
doclist = ["test1.txt", "test2.txt", "test3.txt", "test4.txt"]
folderpath = "test_data"
dictionary = gentermfreq(doclist, folderpath)
# print(dict)
matrix = generatematrix(dictionary)
df = calcdf(matrix)
idf = calcidf(df)
b = generatetfmatrix(matrix, idf)
print(b)
saveastxt(b)
