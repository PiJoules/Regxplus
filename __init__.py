from __future__ import print_function

# Call vendor to add the dependencies to the classpath
import vendor
vendor.add('lib')


# Import the Flask Framework
from flask import Flask, render_template
app = Flask(__name__)

import random

from regex_generator import RegexCrosswordGenerator


@app.route('/')
def index():
    x = RegexCrosswordGenerator(random.randint(2, 4), random.randint(2, 4))
    return render_template(
        "index.html",
        rows=x.rows,
        cols=x.cols,
        filler_row="0" * x.width,
        filler_col="0" * x.height
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0")
