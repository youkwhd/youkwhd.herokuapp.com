from . import blueprints
from flask import render_template

@blueprints["home"].route("/")
def home():
    return render_template("home/index.html")
