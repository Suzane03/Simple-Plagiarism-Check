from flask import Flask, request, render_template
import re
import math
import os

app = Flask(__name__)

@app.route("/")
def loadPage():
    return render_template("index.html", query="")

@app.route("/", methods=['POST'])
def cosineSimilarity():
    try:
        universalSetOfUniqueWords = []
        matchPercentage = 0

        inputQuery = request.form['query']
        lowercaseQuery = inputQuery.lower()

        queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()

        for word in queryWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        with open(os.path.join(os.path.dirname(__file__), "database1.txt"), "r") as fd:
            database1 = fd.read().lower()

        databaseWordList = re.sub("[^\w]", " ", database1).split()

        for word in databaseWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        queryTF = [queryWordList.count(word) for word in universalSetOfUniqueWords]
        databaseTF = [databaseWordList.count(word) for word in universalSetOfUniqueWords]

        dotProduct = sum(query * database for query, database in zip(queryTF, databaseTF))

        queryVectorMagnitude = math.sqrt(sum(tf**2 for tf in queryTF))
        databaseVectorMagnitude = math.sqrt(sum(tf**2 for tf in databaseTF))

        if queryVectorMagnitude != 0 and databaseVectorMagnitude != 0:
            matchPercentage = (dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

        output = "Input query text matches %0.02f%% with database." % matchPercentage
        return render_template('index.html', query=inputQuery, output=output)
    except Exception as e:
        output = "Please Enter Valid Data"
        return render_template('index.html', query=inputQuery, output=output)

if __name__ == "__main__":
    app.run()
