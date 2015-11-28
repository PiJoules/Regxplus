from __future__ import print_function

# Call vendor to add the dependencies to the classpath
import vendor
vendor.add('lib')


# Import the Flask Framework
from flask import Flask, render_template, request
app = Flask(__name__)

import random

from regex_generator import RegexCrosswordGenerator


@app.route("/")
def index_route():
    return render_template("home.html")


@app.route("/puzzle/")
def puzzle_route():
    w = request.args.get("w")
    h = request.args.get("h")
    w = max(min(int(w or random.randint(2, 10)), 10), 2)
    h = max(min(int(h or random.randint(2, 10)), 10), 2)
    x = RegexCrosswordGenerator(w, h)
    return render_template(
        "index.html",
        rows=x.rows,
        cols=x.cols,
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


@app.route("/puzzle/<difficulty>/")
def puzzle_route_difficulty(difficulty=None):
    if difficulty == "beginner":
        w = random.randint(2, 4)
        h = random.randint(2, 4)
    elif difficulty == "intermediate":
        w = random.randint(5, 7)
        h = random.randint(5, 7)
    elif difficulty == "expert":
        w = random.randint(8, 12)
        h = random.randint(8, 10)
    else:
        # Anything else or random
        # If you're wondering why I set the limit to 10,
        # this is the number of columns I could fit on my
        # phone screen before I had to scroll to see the
        # last column.
        w = random.randint(2, 10)
        h = random.randint(2, 10)
    x = RegexCrosswordGenerator(w, h)
    return render_template(
        "index.html",
        rows=x.rows,
        cols=x.cols,
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0")
