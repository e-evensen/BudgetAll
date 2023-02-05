import os
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/index')
def index():
    creator = {"name": "Elijah Evensen"}

    return render_template("index.html", user = creator)

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)