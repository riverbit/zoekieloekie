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

def gentermfreqmtx(doclist, folderpath):
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

# EXAMPLE
doclist = ["test1.txt", "test2.txt", "test3.txt"]
folderpath = "test_data"
print(gentermfreqmtx(doclist, folderpath))