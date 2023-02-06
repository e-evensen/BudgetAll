# Nick Warren Git comment

import os
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
