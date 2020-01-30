from flask import Flask
from flask import render_template
from flask import request

from search import *

app = Flask(__name__)

app = Flask(__name__)


@app.route("/test")
def test():
    return render_template("index.html")


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
        firstresult = results[0]
        sniplocks = getsniplocation(rawquery, results, "test_data/")
        snippets = getsnippet(sniplocks, "test_data/")
        if firstresult[1] == 0.0:
            return render_template(
                "error.html",
                reason=
                'your query did not return any results. If in doubt, search "Boeing"',
            )
        else:
            return render_template("return.html",
                                   query=rawquery,
                                   results=results,
                                   snippet=snippets)


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["DEBUG"] = True
    app.config["SERVER_NAME"] = "127.0.0.1:5000"
    app.run()
