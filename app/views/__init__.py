from flask import Blueprint

blueprints = {
    "home": Blueprint("home", __name__),
}

from . import home
