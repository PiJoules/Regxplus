from __future__ import print_function

# Call vendor to add the dependencies to the classpath
import vendor
vendor.add('lib')


# Import the Flask Framework
from flask import Flask, render_template, request
app = Flask(__name__)

import random
import json

from regex_generator import RegexCrosswordGenerator


@app.route("/")
def index_route():
    return render_template("home.html")


@app.route("/puzzle/")
def puzzle_route():
    with open('subheaders.json') as f:
        subheader = random.choice(json.load(f))
    w = request.args.get("w")
    h = request.args.get("h")
    w = max(min(int(w or random.randint(2, 10)), 10), 2)
    h = max(min(int(h or random.randint(2, 10)), 10), 2)
    x = RegexCrosswordGenerator(w, h)
    return render_template(
        "index.html",
        header="Custom",
        subheader=subheader,
        rows=zip(x.rows, x.rows2),
        cols=zip(x.cols, x.cols2),
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


@app.route("/puzzle/double/")
def puzzle_double_route():
    with open('subheaders.json') as f:
        subheader = random.choice(json.load(f))
        w = random.randint(2, 10)
        h = random.randint(2, 10)
    x = RegexCrosswordGenerator(w, h)
    return render_template(
        "index.html",
        header="Double Trouble",
        subheader=subheader,
        rows=zip(x.rows, x.rows2),
        cols=zip(x.cols, x.cols2),
        filler_row="0" * x.width,
        filler_col="0" * x.height,
        double=True
    )


@app.route("/puzzle/more_expert/")
def puzzle_guru_route():
    with open('subheaders.json') as f:
        subheader = random.choice(json.load(f))
    x = RegexCrosswordGenerator(12, 12)
    return render_template(
        "index.html",
        header="More Expert",
        subheader=subheader,
        rows=zip(x.rows, x.rows2),
        cols=zip(x.cols, x.cols2),
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


@app.route("/puzzle/alice/")
def puzzle_alice_route():
    with open('subheaders.json') as f:
        subheader = random.choice(json.load(f))
    w = random.randint(2, 10)
    h = random.randint(2, 10)
    x = RegexCrosswordGenerator(
        w, h, use_real_words=True, textfile="texts/Alice.txt")
    return render_template(
        "index.html",
        header="Alice",
        subheader=subheader,
        rows=zip(x.rows, x.rows2),
        cols=zip(x.cols, x.cols2),
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


@app.route("/puzzle/shakespeare/")
def puzzle_shakespeare_route():
    with open('subheaders.json') as f:
        subheader = random.choice(json.load(f))
    w = random.randint(2, 10)
    h = random.randint(2, 10)
    x = RegexCrosswordGenerator(
        w, h, use_real_words=True, textfile="texts/Shakespeare.txt")
    return render_template(
        "index.html",
        header="Shakespeare",
        subheader=subheader,
        rows=zip(x.rows, x.rows2),
        cols=zip(x.cols, x.cols2),
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


@app.route("/puzzle/huck/")
def puzzle_huck_route():
    with open('subheaders.json') as f:
        subheader = random.choice(json.load(f))
    w = random.randint(2, 10)
    h = random.randint(2, 10)
    x = RegexCrosswordGenerator(
        w, h, use_real_words=True, textfile="texts/Huck.txt")
    return render_template(
        "index.html",
        header="Huck",
        subheader=subheader,
        rows=zip(x.rows, x.rows2),
        cols=zip(x.cols, x.cols2),
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


@app.route("/puzzle/<difficulty>/")
def puzzle_route_difficulty(difficulty=None):
    with open('subheaders.json') as f:
        subheader = random.choice(json.load(f))
    if difficulty == "beginner":
        w = random.randint(2, 4)
        h = random.randint(2, 4)
        use_real_words = True
        header = "Beginner"
    elif difficulty == "intermediate":
        w = random.randint(5, 7)
        h = random.randint(5, 7)
        use_real_words = True
        header = "Intermediate"
    elif difficulty == "expert":
        w = random.randint(8, 10)
        h = random.randint(8, 10)
        use_real_words = True
        header = "Expert"
    else:
        # Anything else or random
        # If you're wondering why I set the limit to 10,
        # this is the number of columns I could fit on my
        # phone screen before I had to scroll to see the
        # last column.
        w = random.randint(2, 10)
        h = random.randint(2, 10)
        use_real_words = False
        header = "Random"
    x = RegexCrosswordGenerator(w, h, use_real_words=use_real_words)
    return render_template(
        "index.html",
        header=header,
        subheader=subheader,
        rows=zip(x.rows, x.rows2),
        cols=zip(x.cols, x.cols2),
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


if __name__ == '__main__':
    app.run()
