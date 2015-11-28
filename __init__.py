from __future__ import print_function

# Call vendor to add the dependencies to the classpath
import vendor
vendor.add('lib')


# Import the Flask Framework
from flask import Flask, render_template, request
app = Flask(__name__)

import random

from regex_generator import RegexCrosswordGenerator


@app.route('/')
def index():
    w = max(min(int(request.args.get("w") or random.randint(2, 10)), 10), 2)
    h = max(min(int(request.args.get("h") or random.randint(2, 10)), 10), 2)
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
