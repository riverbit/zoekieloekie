import pandas as pd
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
    wordlist = list()
    header = list()
    matrix = list()
    for document in wordcounts:
        header.append(document)
        for term in wordcounts[document]:
            if term not in wordlist:
                wordlist.append(term)
    matrix.append(header)
    for word in wordlist:
        row = list()
        row.append(word)
        for document in header:
            if word in wordcounts[document]:
                frequency = wordcounts[document].get(word) # get the frequency from the key from the assoc. dictionary
                row.append(frequency)
            else:
                row.append(0)
        matrix.append(row)
    header.insert(0, "")
    return matrix

# EXAMPLE
doclist = ["test1.txt", "test2.txt", "test3.txt", "test4.txt"]
folderpath = "test_data"
dict = gentermfreq(doclist, folderpath)
#print(dict)
print(generatematrix(dict))