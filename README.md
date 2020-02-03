# zoekieloekie
The ultimate aim of the project—which we have dubbed as the ‘ZoekieLoekie’ system—is to provide a ranked overview of document relevance based on word-based querying of users. The system utilises the vector-space model to calculate the relevance of a document provided.

## Description of the project
This system is part of a Python assignment as part of the Information Science course. The goal of the assignment was to create a search engine using the vector-space model. Our document collection consists of documents regarding the Boeing 737-MAX fiasco. We are not affiliated with Airbus.

## Implementation
### Document generation: `docgen.py`
Documents can be preprocessed with the `gendoc.py` code. Non-text characters are removed, and stemming is applied using the `NLTK` toolkit. This process makes it possible for the user to search for words in a different form in the text compared to their query. A query for ‘crashing’ also returns documents containing ‘crashed’ or ‘crashes’.  

In the next stage, the system generates a term-frequency matrix showing which term occurs how often in a document. After this process, the document frequency is calculated for all terms. The system now knows how often every term occurs. The document frequency is stored in the memory for later reference. A term is only of importance if it is unique. In our document set, the occurrence of the word ‘plane’ should not make the document stand out. However, the occurrence of the word ‘monkey’ should make the document stand out. The system calculates the perceived importance of a term by calculating the inverted document frequency (idf). After this, a term-weight frequency is generated, which is stored as a csv file.

### Search: `search.py`
To start, our system opens the file created during the pre-processing part and squares all entries in the file. After this, the document vector length is calculated for every individual document.

The next step in the process is the calculation of the similarity between the query and a document. This is done with by calculating the cosine similarity. The dot product (the upper part of the equation) is calculated first and subsequently divided by the bottom of the equation. The system divides the dot product by the product of the vector length of the document and the vector length of the query. The results are then ranked by vector length, with the highest score being put first. 

Before the query is used in the search system, the same stemming and stopword removal technologies are applied to the query. A snippet is also generated to be displayed to the user. The system searches for the first occurrence of the term entered first by the user, and returns a snippet of the document to web server. The snippet contains context for the user, as it shows a part before and after the occurrence of the keyword (where possible). 
### Web server `application.py`
A `flask` is used to display the results to the user. The user enters the website on the landing page, which shows a large search box inviting the user to try the search engine. When a query is entered by the user, the query is first put through an algorithm that removes the stem and stopwords. After this step, the system uses the functions in the search part to establish the most relevant documents for the user. 

If no documents are found, the user is given a user-readable error with the option to immediately try again with a different search query. If relevant documents have been found, the user is presented with a top five, showing the relevance score, document name and snippet. If the user would like to view additional documents beyond the standard top five, the user can use the ‘more results’ button to view additional results. This button is displayed until all documents have been presented to the user.
