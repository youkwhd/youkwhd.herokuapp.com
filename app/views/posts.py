from . import blueprints
from .. import posts as _posts
from flask import render_template

@blueprints["posts"].route("/posts/")
def posts():
    return render_template("posts/index.html", posts=_posts)

@blueprints["posts"].route("/posts/<slug>/")
def post(slug):
    post = _posts.get_or_404(slug)
    return render_template("posts/slug.html", post=post)
