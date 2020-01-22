import math as mth
def cleantext(text):
    """This function cleans the supplied text from illegal characters, such as interpunction,
    upper case letters and numbers. It also generates the document term frequencies."""
    # TO DO ADD STEMMING
    # Remove illegal characters from the text
    cleanedtext = ""
    illegal_chars = [",", ".", "'"]
    for i in text:
        i = i.lower() # make text lower case
        if i not in illegal_chars and not i.isnumeric(): # check if the variable is in the illegal chars list or a number
            cleanedtext += i
    words = cleanedtext.split() # splits the cleaned text into words

    word_frequencies = dict()
    for i in words:
        if i in word_frequencies:
            word_frequencies[i] += 1
        else:
            word_frequencies[i] = 1
    return word_frequencies

def gentermfreq(doclist, folderpath):
    """
    Function generates a term frequency matrix for the documents provided in the list 
    `doclist`. The `folderpath` to the folder containing the documents needs to be provided.
    """  
    wordcounts = dict()
    for document in doclist:
        path = folderpath+"/"+document
        file = open(path)
        txt = file.read()
        cleanedtxt = cleantext(txt) # returns the document term frequency
        wordcounts[document] = cleanedtxt
    return wordcounts

def generatematrix(wordcounts):
    """Generate a term frequency matrix from the `wordcount` dictionary provided."""
    wordlist = list() # generate several lists to be filled later
    header = list()
    matrix = list()
    for document in wordcounts: 
        header.append(document) # for every txt file, add the file name to a list called headers
        for term in wordcounts[document]: # create a unique list containing all terms once
            if term not in wordlist:
                wordlist.append(term)
    matrix.append(header) # add the generated header to the matrix
    for word in wordlist: # for every unique word, check the frequency of the word in every doc
        row = list() # reset the list called row
        row.append(word) # put the unique word in front of the row
        for document in header: # for every document check if it contains the term
            if word in wordcounts[document]:
                frequency = wordcounts[document].get(word) # get the frequency from the key from the assoc. dictionary
                row.append(frequency)
            else:
                row.append(0) # insert 0 for the current document if it does not contain the word
        matrix.append(row)
    header.insert(0, "")
    return matrix

def calcdf(matrix):
    wordamount = len(matrix[0])
    df = dict()
    for line in range(1, wordamount): # get every line from the matrix
        current_line = matrix[line]
        term = current_line[0]
        worddf = 0
        for word in range(1, wordamount):
            current_word = current_line[word]
            if current_word > 0:
                worddf += 1
        df[term] = worddf
    return df

# EXAMPLE
doclist = ["test1.txt", "test2.txt", "test3.txt", "test4.txt"]
folderpath = "test_data"
dictionary = gentermfreq(doclist, folderpath)
#print(dict)
matrix = generatematrix(dictionary)
print(calcdf(matrix))