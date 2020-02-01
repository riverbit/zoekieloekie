from flask import Flask
from flask import render_template
from flask import request
import ast

from search import *

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/results", methods=["POST"])
def results():
    rawquery = request.form["query"]
    query = reformquery(rawquery)
    if not query:  # if the adjusted query is empty, do not continue
        return render_template("error.html",
                               reason="your query did not return any results")
    else:
        dataframe = opendoc("data/database.csv")
        twmatrix = generatesqrmatrix(dataframe)
        vectorlength = generatedveclen(twmatrix)
        dotproducts = getdotprod(query, dataframe)
        similarities = sim(dotproducts, query, vectorlength)
        results = rank(similarities)
        amountofresults = len(results)
        firstresult = results[0]
        sniplocks = getsniplocation(rawquery, results, "test_data/")
        snippets = getsnippet(sniplocks, "test_data/")
        fiveresults = list()
        for i in range(0, 5):
            fiveresults.append(results[i])
        if firstresult[1] == 0.0:
            return render_template(
                "error.html",
                reason='your query did not return any results. If in doubt, search "Boeing"',
            )
        else:
            return render_template("return.html",
                                   query=rawquery,
                                   results=fiveresults,
                                   snippet=snippets, resultno=5, completeresults=results, amountofresults=amountofresults)


@app.route("/encore", methods=["POST"])
def encore():
    seenallresults = False
    # retrieve all form fields
    query = request.form["query"]
    results = request.form["results"]  # represents the last rank returned
    resultno = int(request.form["resultno"])  # by def. stored as string
    amountofresults = int(request.form["amountofresults"])
    # The dictionaries and lists are returned as a string rather than as a list
    # or dict. The ast.literal_eval()-function converts this to an actual
    # function instead of a string.
    listedresults = ast.literal_eval(results)
    snippet = request.form["snippet"]
    dictsnippets = ast.literal_eval(snippet)
    fiveresults = list()
    resultlimit = resultno + 5  # by default, docs are listed in the range 0-5
    if resultlimit >= amountofresults:
        # if the amount of documents exceeds the standard range, adjust the
        # range here
        resultlimit = amountofresults
        seenallresults = True  # check to see if there can be more results seen
    for i in range(resultno, resultlimit):
        fiveresults.append(listedresults[i])
    return render_template("encore.html",
                           query=query,
                           results=fiveresults,
                           snippet=dictsnippets, resultno=resultlimit, completeresults=results, amountofresults=amountofresults, seenallresults=seenallresults)


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["DEBUG"] = True
    # app.config["SERVER_NAME"] = "127.0.0.1:5000"
    app.run()
