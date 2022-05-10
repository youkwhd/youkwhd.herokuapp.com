from flask import Blueprint

blueprints = {
    "home": Blueprint("home", __name__),
    "posts": Blueprint("posts", __name__),
}

from . import home
from . import posts
